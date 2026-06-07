#!/usr/bin/env bash
# Install Docker Engine in WSL2 Ubuntu and start the daemon.
# Run as root:  sudo bash 03_docker.sh <your-linux-username>
# Idempotent: safe to re-run.
set -uo pipefail

TARGET_USER="${1:-${SUDO_USER:-$(whoami)}}"
echo "==> Installing Docker for user: $TARGET_USER"

if command -v docker >/dev/null 2>&1; then
  echo "docker already installed: $(docker --version)"
else
  echo "==> Running official Docker convenience script"
  curl -fsSL https://get.docker.com -o /tmp/get-docker.sh
  sh /tmp/get-docker.sh
fi

echo "==> Add $TARGET_USER to docker group (use docker without sudo)"
groupadd -f docker
usermod -aG docker "$TARGET_USER"

echo "==> Start the Docker daemon"
started=""
# Try systemd first (WSL2 supports systemd when enabled in /etc/wsl.conf)
if pidof systemd >/dev/null 2>&1 || [ -d /run/systemd/system ]; then
  systemctl enable docker >/dev/null 2>&1 || true
  if systemctl start docker 2>/dev/null; then started="systemd"; fi
fi
# Fall back to the sysvinit service script
if [ -z "$started" ]; then
  if service docker start 2>/dev/null; then started="service"; fi
fi
# Last resort: launch dockerd directly in the background
if [ -z "$started" ]; then
  if ! pidof dockerd >/dev/null 2>&1; then
    nohup dockerd >/var/log/dockerd.log 2>&1 &
    sleep 5
  fi
  started="dockerd-direct"
fi
echo "daemon start method: $started"

echo "==> Wait for the daemon socket"
for i in $(seq 1 20); do
  if docker info >/dev/null 2>&1; then break; fi
  sleep 1
done

echo "==> Versions"
docker --version || true
docker compose version 2>/dev/null || true

echo "==> Smoke test: docker run hello-world"
if docker run --rm hello-world >/tmp/hello.log 2>&1; then
  echo "DOCKER_HELLO_OK"
else
  echo "hello-world failed (tail):"; tail -15 /tmp/hello.log || true
  echo "DOCKER_HELLO_FAILED"
fi

# Enable systemd persistently so docker autostarts on future WSL launches.
if [ ! -f /etc/wsl.conf ] || ! grep -q "systemd=true" /etc/wsl.conf 2>/dev/null; then
  echo "==> Enabling systemd in /etc/wsl.conf (takes effect after 'wsl --shutdown')"
  {
    echo "[boot]"
    echo "systemd=true"
  } >> /etc/wsl.conf
fi

echo "DOCKER_SETUP_DONE"
