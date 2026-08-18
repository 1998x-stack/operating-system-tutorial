# 🖥️ 操作系统

> 🖥️ 28章 实战体系

一套完整的 **操作系统** 全中文实战课程体系，共 **28 章**。本课程以 HTML 可视化的形式呈现，从基础原理到工程实践循序渐进，适合系统性学习与复习。

## 🚀 快速开始

无需安装任何依赖，直接用浏览器打开 `index.html` 即可在线阅读全部章节：

```bash
open index.html   # macOS
# 或在浏览器中直接打开 index.html
```

## 📖 章节目录

| # | 章节 | 核心主题 |
|---|------|----------|
| 01 | 什么是操作系统 | 操作系统定义、发展历史、OS分类与设计哲学 |
| 02 | 硬件架构基础 | 冯·诺依曼架构、x86/ARM/RISC-V、存储金字塔、中断与异常 |
| 03 | OS内核架构 | 宏内核、微内核、混合内核、Unikernel |
| 04 | 用户态与内核态 | 特权级别、系统调用全流程、strace实战、上下文切换成本 |
| 05 | 引导与初始化 | BIOS/UEFI、GRUB/systemd-boot、initramfs、systemd启动编排 |
| 06 | OS内核源码初探 | Linux内核源码目录树、编码风格、内核模块、Kconfig/Kbuild |
| 07 | OS实验环境搭建 | QEMU虚拟平台、GDB远程调试、xv6教学内核、perf/bpftrace/ftrace |
| 08 | 进程管理 | task_struct、进程五状态模型、fork写时拷贝、execve加载程序 |
| 09 | 线程与协程 | 内核线程、1:1 vs M:N模型、clone系统调用、协程与async/await |
| 10 | CPU调度 | O(n)→CFS→EEVDF、vruntime红黑树、sched_ext用户态调度、PREEMPT_RT实时 |
| 11 | 同步与互斥 | 自旋锁vs互斥锁、信号量PV操作、RCU读多写少、死锁与lockdep |
| 12 | 虚拟内存 | 四级页表遍历、TLB加速器、缺页中断全流程、大页与mTHP |
| 13 | 物理内存管理 | Buddy System、Slab/Slub分配器、页面回收与swap、MGLRU多代LRU |
| 14 | 文件系统 | VFS统一接口、inode与dentry、ext4区段树、Btrfs写时复制 |
| 15 | I/O模型与io_uring | 五种I/O模型、epoll事件驱动、io_uring环形队列、零拷贝技术矩阵 |
| 16 | 设备驱动 | Linux设备模型、字符设备驱动、设备树Device Tree、Rust驱动开发 |
| 17 | 中断与异常处理 | 上半部/下半部、软中断→tasklet→workqueue、中断亲和性、PREEMPT_RT中断线程化 |
| 18 | 时间管理 | jiffies与HZ、hrtimer高精度定时器、TSC/HPET/PIT时钟源、时钟漂移与闰秒 |
| 19 | 网络协议栈 | 数据包内核路径、三次握手实现、Netfilter五链四表、XDP可编程数据路径 |
| 20 | eBPF可观测性 | eBPF架构全景、bpftrace单行追踪、kprobe vs tracepoint、BPF Map类型 |
| 21 | 虚拟化技术 | KVM Hypervisor、vCPU调度、virtio半虚拟化、Popek-Goldberg定理 |
| 22 | 容器与命名空间 | 六种Namespace、cgroup v2层级、OverlayFS分层、从chroot到Docker |
| 23 | 内核调试技术 | printk动态调试、kdump+crash分析、KASAN/UBSAN检测、kgdb源码级调试 |
| 24 | 性能分析与调优 | perf全景、火焰图生成、内存泄漏排查、I/O延迟分析 |
| 25 | 动手写一个小OS | 实模式Bootloader、GDT/IDT设置、物理页分配器、Ring 0→Ring 3切换 |
| 26 | 现代OS前沿趋势 | Rust for Linux、LDOS AI驱动OS、seL4微内核复兴、RISC-V+Rust生态 |
| 27 | OS内核设计决策 | 宏内核vs微内核之争、不破坏用户空间铁律、ABI稳定性权衡、关键设计取舍 |
| 28 | 综合项目 | eBPF分析调度延迟、字符设备驱动、xv6添加COW fork、内核火焰图 |

## 📂 项目结构

```text
operating-system-tutorial/
├── index.html      # 课程主入口（在线阅读全部章节）
├── 01.html ~ 28.html   # 各章节正文
├── courses.json    # 课程元数据（标题/章节/主题）
└── theme.css       # 统一主题样式
```

## ✨ 课程特色

- **全中文实战体系**：面向中文读者，由浅入深，覆盖原理与工程实践
- **28 章完整内容**：系统化章节编排，形成完整知识闭环
- **可视化呈现**：HTML 图文并茂，适合快速浏览与重点回顾
- **即开即用**：无需构建、无需服务器，纯静态页面随开随看

---
*本课程由 `operating-system-tutorial/` 项目维护。*