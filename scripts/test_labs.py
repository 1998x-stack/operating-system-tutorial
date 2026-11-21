#!/usr/bin/env python3
"""Compile and execute safe, deterministic userspace labs.

Do not run privileged kernel modules, QEMU images, network or destructive labs
here. Those require explicitly configured, isolated integration environments.
"""
from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def run(argv: list[str], *, timeout: int = 30) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(argv, check=True, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, timeout=timeout)


def test_write_syscall() -> None:
    source = ROOT / "labs/ch04-syscall/hello.c"
    if not source.is_file():
        raise AssertionError(f"missing source: {source}")
    compiler = shutil.which(os.environ.get("CC", "cc"))
    if not compiler:
        raise AssertionError("C compiler missing (set CC to an installed compiler)")

    with tempfile.TemporaryDirectory(prefix="os-tutorial-lab-") as work:
        executable = Path(work) / "hello"
        run([compiler, "-std=c11", "-Wall", "-Wextra", "-Werror", "-O0", "-g",
             str(source), "-o", str(executable)])
        completed = run([str(executable)], timeout=5)
        assert completed.returncode == 0, "hello returned nonzero"
        assert completed.stdout == b"hello\n", (
            f"unexpected stdout: {completed.stdout!r}")
        assert completed.stderr == b"", (
            f"unexpected stderr: {completed.stderr!r}")


def main() -> int:
    if not sys.platform.startswith("linux"):
        print("SKIP: userspace lab execution requires Linux", file=sys.stderr)
        return 2
    try:
        test_write_syscall()
    except (AssertionError, OSError, subprocess.CalledProcessError,
            subprocess.TimeoutExpired) as error:
        print(f"FAIL: ch04 write() userspace lab: {error}", file=sys.stderr)
        return 1
    print("PASS: ch04 write() userspace lab compiles cleanly and prints hello\\n")
    print("NOTE: privileged kernel/QEMU/xv6 exercises were not run")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
