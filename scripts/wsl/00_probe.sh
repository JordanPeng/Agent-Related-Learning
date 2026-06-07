#!/usr/bin/env bash
# Probe the WSL2 environment: user, tools, resources, GPU, mounts.
set -u

echo "USER=$(whoami)"
echo "HOME=$HOME"
echo "DISTRO=$(. /etc/os-release; echo "$PRETTY_NAME")"

echo "--- tools ---"
for t in uv python3 pip3 gcc g++ make cmake ninja git curl ldconfig; do
  printf '%-10s ' "$t"
  if command -v "$t" >/dev/null 2>&1; then
    "$t" --version 2>/dev/null | head -1
  else
    echo "MISSING"
  fi
done

echo "--- python venv module ---"
python3 -c 'import venv; print("venv module: ok")' 2>/dev/null || echo "venv module: MISSING (apt install python3-venv)"

echo "--- resources ---"
free -h | head -2
echo "nproc=$(nproc)"

echo "--- disk (linux home fs) ---"
df -h "$HOME" | tail -1

echo "--- GPU (nvidia-smi in WSL) ---"
if command -v nvidia-smi >/dev/null 2>&1; then
  nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader
else
  echo "nvidia-smi MISSING"
fi
echo "--- CUDA libs visible to WSL (/usr/lib/wsl/lib) ---"
ls /usr/lib/wsl/lib/libcuda* 2>/dev/null || echo "no libcuda in /usr/lib/wsl/lib"

echo "--- workspace mount ---"
if [ -d /mnt/f/agent_learning ]; then
  echo "/mnt/f/agent_learning OK"
  ls -d /mnt/f/agent_learning/LLM_model_weights/* 2>/dev/null
else
  echo "F: not mounted"
fi

echo "--- docker ---"
command -v docker >/dev/null 2>&1 && docker --version || echo "docker MISSING"
echo "PROBE DONE"
