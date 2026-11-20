# 配套实验

本目录提供围绕系统调用、进程、线程、调度、同步、虚拟内存、物理内存和文件系统的最小实验。优先在可丢弃的虚拟机或容器中运行；所有内存/文件系统观测示例尽量保持只读。

## 第 01–07 章

- [第 04 章：观察一次 write 系统调用](ch04-syscall/README.md)
- [第 06 章：构建一个最小外部内核模块](ch06-hello-module/README.md)
- [第 07 章：QEMU + GDB 内核调试](ch07-qemu/README.md)
- [第 07 章：MIT xv6-RISC-V](ch07-xv6/README.md)

## 第 08–14 章

- [第 08 章：fork、COW 与 exec](ch08-process/README.md)
- [第 09 章：pthread 与互斥锁](ch09-threads/README.md)
- [第 10 章：观察调度策略与 CPU 亲和性](ch10-scheduler/README.md)
- [第 11 章：竞态、互斥锁与 ThreadSanitizer](ch11-sync/README.md)
- [第 12 章：匿名映射与 fork COW](ch12-vm/README.md)
- [第 13 章：buddy、slab、PSI 与 cgroup 只读观测](ch13-memory/README.md)
- [第 14 章：write、fsync 与 rename 持久性路径](ch14-filesystem/README.md)

这些实验验证的是特定接口路径，不是对整套 Linux 内核或任何性能指标的完整复现。除明确写明外，示例没有承诺在所有发行版、内核版本和 CPU 架构上得到相同输出。
