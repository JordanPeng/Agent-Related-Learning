#!/usr/bin/env bash
# Install system build dependencies needed for on-the-fly kernel compilation
# (Triton JIT needs Python.h; cmake/ninja help other CUDA extensions).
# Run as root:  sudo bash 07_build_deps.sh
set -uo pipefail

# WSL often runs `unattended-upgrades` on first boot, which holds the dpkg lock.
# Wait for the actual lock files to be released. NOTE: we deliberately do NOT
# check for the `unattended-upgr` process name, because the harmless
# `unattended-upgrade-shutdown --wait-for-signal` helper lingers for the whole
# session and would make us wait forever. The lock files are the real signal.
wait_for_apt() {
  for i in $(seq 1 60); do
    if ! fuser /var/lib/dpkg/lock-frontend >/dev/null 2>&1 \
       && ! fuser /var/lib/dpkg/lock >/dev/null 2>&1 \
       && ! fuser /var/lib/apt/lists/lock >/dev/null 2>&1; then
      return 0
    fi
    echo "   apt is locked (another process is installing); waiting... ($i)"
    sleep 5
  done
  echo "   timed out waiting for apt lock; trying anyway"
}

echo "==> Waiting for any background apt/unattended-upgrades to finish"
wait_for_apt

echo "==> apt-get update"
apt-get update -qq

echo "==> Installing build deps: python3-dev, build-essential, ninja-build, cmake, pybind11"
wait_for_apt
DEBIAN_FRONTEND=noninteractive apt-get install -y -qq \
  python3-dev python3.12-dev build-essential ninja-build cmake pkg-config

echo "==> Verify Python.h is present"
ls -l /usr/include/python3.12/Python.h 2>/dev/null && echo "PYTHON_H_OK" || echo "PYTHON_H_MISSING"

echo "==> Versions"
gcc --version | head -1
make --version | head -1
cmake --version | head -1 || true
ninja --version 2>/dev/null || true

echo "BUILD_DEPS_DONE"
