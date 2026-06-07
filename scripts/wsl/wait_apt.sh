#!/usr/bin/env bash
# Wait until Ubuntu's background unattended-upgrades finishes and the dpkg lock
# is free, so a subsequent `sudo apt install` won't be blocked. No sudo needed.
set -uo pipefail

for i in $(seq 1 120); do
  if ! pgrep -x unattended-upgr >/dev/null 2>&1 \
     && ! fuser /var/lib/dpkg/lock-frontend >/dev/null 2>&1 \
     && ! fuser /var/lib/dpkg/lock >/dev/null 2>&1; then
    echo "LOCK_CLEAR_READY after ~$((i*5))s"
    exit 0
  fi
  echo "waiting for unattended-upgrades / dpkg lock... ($((i*5))s)"
  sleep 5
done

echo "STILL_LOCKED after ~10min"
exit 1
