#!/usr/bin/env bash
# Locate the pip-provided CUDA toolkit (nvcc + headers) inside the venv and
# print values suitable for CUDA_HOME, so flashinfer/torch JIT can compile.
set -uo pipefail
VENV="$HOME/agent_learning/.venv"
SP="$VENV/lib/python3.12/site-packages"

echo "=== nvcc binaries found ==="
find "$SP" -name nvcc -type f 2>/dev/null

echo "=== nvidia cuda_nvcc package dir ==="
ls -d "$SP"/nvidia/cuda_nvcc 2>/dev/null || echo "no nvidia/cuda_nvcc"
ls "$SP"/nvidia/cuda_nvcc/bin 2>/dev/null || true

echo "=== cuda runtime headers (cuda_runtime.h) ==="
find "$SP/nvidia" -name "cuda_runtime.h" 2>/dev/null | head -3

echo "=== candidate CUDA_HOME (cuda_nvcc) contents ==="
CH="$SP/nvidia/cuda_nvcc"
if [ -d "$CH" ]; then
  echo "CUDA_HOME=$CH"
  ls "$CH"
fi
echo "PROBE_DONE"
