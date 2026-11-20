# 操作系统中文实践教程

> 28 章从硬件基础、内核机制到 Linux 工具链与综合项目的中文学习资料。**这是独立教学项目，不是 Linux 内核官方文档。**

**[阅读课程首页](index.html)** · **[从第 01 章开始](01.html)** · [学习路线](docs/guides/learning-path.md) · [内容规范](docs/guides/content-guide.md) · [贡献指南](CONTRIBUTING.md)

这套教程围绕三个问题组织每一章：**为什么需要这个机制 → 它如何工作 → 怎样观察或验证它**。网页采用静态 HTML，章节之间可直接前后跳转，保留原有 `01.html` 至 `28.html` 链接以便引用与分享。

## 如何阅读

1. **本地即开即用：**克隆仓库后双击 `index.html`，或用浏览器打开任意章节 HTML。新版目录不再依赖 `fetch()`，因此在 `file://` 下也可以浏览。
2. **通过本地服务器阅读：**在项目根目录执行 `python3 -m http.server 8000`，然后访问 `http://localhost:8000/`。
3. **动手验证：**优先使用虚拟机或容器实验环境；执行内核模块、调试器、eBPF、系统配置修改相关命令前，请核对权限、内核版本与设备架构。
4. **自测与复盘：**章节顶部提供问题地图和段落目录，结尾提供自测提示。先尝试回答，再展开提示。

> GitHub Pages 的部署状态需以仓库 Pages 设置和 Actions 运行结果为准；本地 HTML 不依赖站点上线。

## 学习路径

| 阶段 | 章节 | 学习目标 |
| --- | --- | --- |
| 基础认知与实验平台 | 01–07 | 理解 OS 的角色、硬件、内核边界和实验环境 |
| 资源管理的核心机制 | 08–14 | 建立进程、调度、并发、内存、文件系统的心智模型 |
| I/O 与系统可观测性 | 15–20 | 连接设备、中断、时间、网络和 eBPF |
| 虚拟化、内核工程与项目 | 21–28 | 理解隔离、调试、优化和设计取舍，完成实践 |

### 一 · 基础认知与实验平台

| 章节 | 关键主题 |
| --- | --- |
| [01 · 什么是操作系统](01.html) | 操作系统定义、发展历史、OS分类与设计哲学 |
| [02 · 硬件架构基础](02.html) | 冯·诺依曼架构、x86/ARM/RISC-V、存储金字塔、中断与异常 |
| [03 · OS内核架构](03.html) | 宏内核、微内核、混合内核、Unikernel |
| [04 · 用户态与内核态](04.html) | 特权级别、系统调用全流程、strace实战、上下文切换成本 |
| [05 · 引导与初始化](05.html) | BIOS/UEFI、GRUB/systemd-boot、initramfs、systemd启动编排 |
| [06 · OS内核源码初探](06.html) | Linux内核源码目录树、编码风格、内核模块、Kconfig/Kbuild |
| [07 · OS实验环境搭建](07.html) | QEMU虚拟平台、GDB远程调试、xv6教学内核、perf/bpftrace/ftrace |

### 二 · 资源管理的核心机制

| 章节 | 关键主题 |
| --- | --- |
| [08 · 进程管理](08.html) | task_struct、进程五状态模型、fork写时拷贝、execve加载程序 |
| [09 · 线程与协程](09.html) | 内核线程、1:1 vs M:N模型、clone系统调用、协程与async/await |
| [10 · CPU调度](10.html) | O(n)→CFS→EEVDF、vruntime红黑树、sched_ext用户态调度、PREEMPT_RT实时 |
| [11 · 同步与互斥](11.html) | 自旋锁vs互斥锁、信号量PV操作、RCU读多写少、死锁与lockdep |
| [12 · 虚拟内存](12.html) | 四级页表遍历、TLB加速器、缺页中断全流程、大页与mTHP |
| [13 · 物理内存管理](13.html) | Buddy System、Slab/Slub分配器、页面回收与swap、MGLRU多代LRU |
| [14 · 文件系统](14.html) | VFS统一接口、inode与dentry、ext4区段树、Btrfs写时复制 |

### 三 · I/O 与系统可观测性

| 章节 | 关键主题 |
| --- | --- |
| [15 · I/O模型与io_uring](15.html) | 五种I/O模型、epoll事件驱动、io_uring环形队列、零拷贝技术矩阵 |
| [16 · 设备驱动](16.html) | Linux设备模型、字符设备驱动、设备树Device Tree、Rust驱动开发 |
| [17 · 中断与异常处理](17.html) | 上半部/下半部、软中断→tasklet→workqueue、中断亲和性、PREEMPT_RT中断线程化 |
| [18 · 时间管理](18.html) | jiffies与HZ、hrtimer高精度定时器、TSC/HPET/PIT时钟源、时钟漂移与闰秒 |
| [19 · 网络协议栈](19.html) | 数据包内核路径、三次握手实现、Netfilter五链四表、XDP可编程数据路径 |
| [20 · eBPF可观测性](20.html) | eBPF架构全景、bpftrace单行追踪、kprobe vs tracepoint、BPF Map类型 |

### 四 · 虚拟化、内核工程与项目

| 章节 | 关键主题 |
| --- | --- |
| [21 · 虚拟化技术](21.html) | KVM Hypervisor、vCPU调度、virtio半虚拟化、Popek-Goldberg定理 |
| [22 · 容器与命名空间](22.html) | 六种Namespace、cgroup v2层级、OverlayFS分层、从chroot到Docker |
| [23 · 内核调试技术](23.html) | printk动态调试、kdump+crash分析、KASAN/UBSAN检测、kgdb源码级调试 |
| [24 · 性能分析与调优](24.html) | perf全景、火焰图生成、内存泄漏排查、I/O延迟分析 |
| [25 · 动手写一个小OS](25.html) | 实模式Bootloader、GDT/IDT设置、物理页分配器、Ring 0→Ring 3切换 |
| [26 · 现代OS前沿趋势](26.html) | Rust for Linux、LDOS AI驱动OS、seL4微内核复兴、RISC-V+Rust生态 |
| [27 · OS内核设计决策](27.html) | 宏内核vs微内核之争、不破坏用户空间铁律、ABI稳定性权衡、关键设计取舍 |
| [28 · 综合项目](28.html) | eBPF分析调度延迟、字符设备驱动、xv6添加COW fork、内核火焰图 |

## 仓库结构

```text
operating-system-tutorial/
├── index.html                     # 静态课程首页，可直接本地打开
├── 01.html … 28.html             # 章节页：保留稳定 URL
├── courses.json                   # 章节顺序与主题元数据
├── assets/
│   ├── css/site.css              # 统一的阅读设计系统
│   └── diagrams/                 # 原创操作系统机制图
├── theme.css                      # 旧样式路径的兼容入口
├── docs/guides/
│   ├── learning-path.md          # 学习阶段、实践顺序
│   └── content-guide.md          # 内容核对与可访问性规范
├── scripts/check_site.py          # 静态 HTML、章节索引和本地链接校验
└── .github/workflows/ci.yml      # 提交与 PR 的静态质量检查
```

**为什么章节仍在仓库根目录？** 已被引用的 `/01.html` … `/28.html` 和 `/index.html` 是公开 URL；将其迁入 `chapters/` 会破坏书签及 GitHub Pages 链接。将可扩展内容放入 `assets/`、`docs/`、`scripts/`，是兼顾清晰结构与向后兼容的选择。

## 静态校验

仅需 **Python 3.10+**，不依赖第三方包：

```bash
python3 scripts/check_site.py
python3 -m http.server 8000
```

脚本检查课程 JSON、28 个章节、单一 H1、主要语义标签、章节前后导航、目录内锚点、相对链接和必要图示。它**不能替代**浏览器的桌面/移动端截图检查，也不能证明文章中的内核实验已在真实环境运行。详见 [内容规范](docs/guides/content-guide.md)。

## 内容来源与边界

概念学习可交叉参考 [Linux 内核官方文档](https://docs.kernel.org/)、[Linux man-pages](https://man7.org/linux/man-pages/)、[xv6 课程资源](https://pdos.csail.mit.edu/6.1810/) 和 [QEMU 文档](https://www.qemu.org/docs/master/)。章节中的命令和机制描述可能受发行版、CPU 架构或内核版本影响，不能把教学示例视作生产环境的操作指令。

本次结构与阅读体验改造遵循 [Olah-style Paper Posts](https://github.com/1998x-stack/Olah-style-posts) 所倡导的“先提出问题、逐步展开、可验证机制”原则；但本仓库是**操作系统课程**，不是论文复现，引用规则和验证范围需按内容调整。所有示意图均为本项目新绘制的解释性图，不代表 Linux 某一版本的逐行实现。

欢迎在 Issue 中指出事实、版本适用范围、实验复现与可访问性问题，修改请参见 [CONTRIBUTING.md](CONTRIBUTING.md)。
