#!/bin/sh
set -eu

pid=${1:-$$}

printf '%s\n' "== scheduling policy (read-only) =="
chrt -p "$pid" 2>/dev/null || true

printf '%s\n' "== task state and scheduler fields =="
ps -o pid,cls,rtprio,ni,psr,stat,comm -p "$pid" 2>/dev/null || true

printf '%s\n' "== CPU affinity =="
taskset -cp "$pid" 2>/dev/null || true

printf '%s\n' "== current kernel =="
uname -a
