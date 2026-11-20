#!/bin/sh
set -eu

show_file() {
    path=$1
    lines=${2:-20}
    if [ -r "$path" ]; then
        printf '\n== %s ==\n' "$path"
        head -n "$lines" "$path"
    fi
}

show_file /proc/buddyinfo 20
show_file /proc/pagetypeinfo 40
show_file /proc/slabinfo 25
show_file /proc/pressure/memory 20

if [ -r /proc/vmstat ]; then
    printf '\n== reclaim and allocation counters ==\n'
    grep -E '^(pgscan|pgsteal|pgfault|pgmajfault|allocstall|compact)' /proc/vmstat | head -n 80
fi

for file in /sys/fs/cgroup/memory.current /sys/fs/cgroup/memory.events /sys/fs/cgroup/memory.pressure; do
    if [ -r "$file" ]; then
        printf '\n== %s ==\n' "$file"
        cat "$file"
    fi
done
