# 操作系统中文实践教程

> 28 章从硬件基础、内核机制到 Linux 工具链与综合项目的中文学习资料。**这是独立教学项目，不是 Linux 内核官方文档。**

**[阅读课程首页](index.html)** · **[从第 01 章开始](01.html)** · [学习路线](docs/guides/learning-path.md) · [内容规范](docs/guides/content-guide.md) · [08–14 章复核记录](docs/reviews/chapters-08-14.md) · [15–21 章复核记录](docs/reviews/chapters-15-21.md) · [22–28 章复核记录](docs/reviews/chapters-22-28.md) · [实验规范](docs/guides/experiment-standard.md) · [浏览器测试](tests/site.spec.mjs) · [贡献指南](CONTRIBUTING.md)

这套教程围绕三个问题组织每一章：**为什么需要这个机制 → 它如何工作 → 怎样观察或验证它**。网页采用静态 HTML，章节之间可直接前后跳转，保留原有 `01.html` 至 `28.html` 链接以便引用与分享。

## 第二轮工程升级

- [实验可复现规范](docs/guides/experiment-standard.md) 与 [实验报告模板](labs/EXPERIMENT_TEMPLATE.md)
- [第二轮质量审计记录](docs/reviews/round-2-platform-upgrade.md)
- [第 01–07 章技术审计](docs/reviews/chapters-01-07.md) · [08–14 章](docs/reviews/chapters-08-14.md) · [15–21 章](docs/reviews/chapters-15-21.md) · [22–28 章](docs/reviews/chapters-22-28.md)
- GitHub Actions 运行静态结构检查、Playwright 浏览器冒烟测试（360 / 390 / 1440 px）及第 04 章用户态 write() 示例的编译/执行测试。
- [第三轮实验验收与覆盖范围](docs/reviews/round-3-lab-validation.md)：区分已实测项目、仅静态复核项目和仍需隔离 VM/硬件的项目。

## 第 01–05 章逐篇精细化（2026-11）

- [逐篇改造记录](docs/reviews/fine-grained-01-05.md)：从“概念解释”深化为“因果机制追踪 + 明确验证边界的微实验”，逐篇提交、逐篇检查。
- [第 01 章](01.html)：文件描述符、内核资源抽象与 procfs 观察。
- [第 02 章](02.html)：TLB miss / CPU cache miss / page fault 的区别及 perf 事件。
- [第 03 章](03.html)：宏内核与微内核的保护域、服务崩溃和重启条件。
- [第 04 章](04.html)：x86-64 write() ABI、errno/短写与 strace 复现。
- [第 05 章](05.html)：固件、initramfs 与 PID 1 交接的故障定位和只读 systemd 观察。

新增机制讲解与实验卡片在手机端可读；Playwright 额外断言前五篇的组件存在并可展开。真实硬件性能和有权限限制的命令仍需根据目标系统单独复现。

## 第 06–10 章逐篇精细化（2026-11）

- [逐篇复核记录](docs/reviews/fine-grained-06-10.md)：沿用 01–05 的“机制追踪 + 只读微实验”标准，逐篇提交、逐篇检查。
- [第 06 章](06.html)：Kconfig/Kbuild 选项到运行时代码的链路，以及只读核对内核构建树。
- [第 07 章](07.html)：QEMU gdbstub 的 `-S`/`-gdb`/断点握手，以及只读核对实验工具链。
- [第 08 章](08.html)：fork 后父子进程共享什么（含新增 COW 图示），以及只读观察写时复制计数。
- [第 09 章](09.html)：`clone()` 共享标志与线程组（含新增线程模型图示），以及只读观察 LWP/tgid。
- [第 10 章](10.html)：EEVDF 的两步选择与实时带宽，以及只读观察调度类与 sysctl。

新增图示为 `assets/diagrams/fork-cow.svg` 与 `assets/diagrams/thread-models.svg`；Playwright 冒烟测试的组件断言扩展到前 10 篇。

## 第 11–18 章逐篇精细化（2026-11）

- [逐篇复核记录](docs/reviews/fine-grained-11-18.md)：沿用 01–10 的“机制追踪 + 只读微实验”标准，逐篇提交、逐篇检查，并为原先缺图的章节补一张原创解释图。
- [第 11 章](11.html)：争用 mutex 的快速/慢路径与 futex 边界，以及只读 futex 追踪。
- [第 12 章](12.html)：区分 TLB miss 与 page fault，以及按需分配的缺页计数观察。
- [第 13 章](13.html)：`kmalloc()` 经 Slub 向伙伴系统补页的分层供给，以及 buddyinfo/slab 只读观察。
- [第 14 章](14.html)：`open()` 返回的 fd 与 dentry、inode、`struct file` 的关系。
- [第 15 章](15.html)：io_uring 提交/完成路径，以及 epoll 就绪通知与完成通知的对比。
- [第 16 章](16.html)：字符设备 `read()` 从设备号到驱动回调的路径。
- [第 17 章](17.html)：中断上半部/下半部分工，以及 `/proc/interrupts`、`/proc/softirqs` 只读观察。
- [第 18 章](18.html)：`hrtimer` 到期路径与 REALTIME/MONOTONIC 时间基准。

新增图示包括 `assets/diagrams/lock-contention.svg`、`buddy-split-merge.svg`、`vfs-lookup.svg`、`io-uring-rings.svg`、`chardev-path.svg`、`irq-top-bottom.svg` 与 `time-bases.svg`；Playwright 冒烟测试的组件断言扩展到前 18 篇。

## 第 19–26 章逐篇精细化（2026-11）

- [逐篇复核记录](docs/reviews/fine-grained-19-26.md)：沿用“机制追踪 + 只读微实验”标准，逐篇提交、逐篇检查，并为缺图章节补原创解释图。
- [第 19 章](19.html)：一次 `send()` 的分层加头路径与 Netfilter 钩子；`ss`/`nstat` 只读观察连接队列。
- [第 20 章](20.html)：一条 `bpftrace` 从编译、验证到挂载与 Map 读取；BTF 与权限只读核对。
- [第 21 章](21.html)：一次 `KVM_RUN` 到 VM-Exit 的循环与 vCPU steal；`systemd-detect-virt`/`/proc/stat` 只读观察。
- [第 22 章](22.html)：容器隔离的叠放顺序；`/proc/self/ns` 与 cgroup 只读观察。
- [第 23 章](23.html)：kdump/vmcore 证据链；`kexec_loaded`/`crashkernel` 只读核对。
- [第 24 章](24.html)：`perf record` 到火焰图的采样路径；PSI 与 `vmstat` 基线只读观察。
- [第 25 章](25.html)：一次 `iret` 到 Ring 3 的前置条件；引导扇区 512 字节/`55aa` 只读核对。
- [第 26 章](26.html)：前沿说法的证据分层核对；本机能力只读观察。

新增图示包括 `net-path.svg`、`ebpf-lifecycle.svg`、`kvm-vcpu.svg`、`crash-analysis.svg`、`perf-workflow.svg`、`boot-to-user.svg` 与 `frontier-map.svg`；Playwright 冒烟测试的组件断言扩展到前 26 篇。

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
| [10 · CPU调度](10.html) | O(n)→CFS→EEVDF、vruntime红黑树、sched_ext BPF 可扩展调度、PREEMPT_RT实时 |
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
| [22 · 容器与命名空间](22.html) | 八种Namespace、cgroup v2层级、OverlayFS分层、从chroot到Docker |
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
├── evidence/                      # 第 01–28 章逐条论断与来源证据
├── labs/                          # 系统调用、模块与 QEMU/xv6 实验
├── docs/
│   ├── guides/                   # 学习路线与内容规范
│   └── reviews/                  # 分批技术复核记录（01–07、08–14、15–21、22–28）
├── theme.css                      # 旧样式路径的兼容入口
├── scripts/check_site.py          # 静态 HTML、章节索引、证据和链接校验
├── scripts/test_labs.py           # 安全的用户态实验编译/运行冒烟测试
└── .github/workflows/ci.yml      # 提交与 PR 的静态质量检查
```

**为什么章节仍在仓库根目录？** 已被引用的 `/01.html` … `/28.html` 和 `/index.html` 是公开 URL；将其迁入 `chapters/` 会破坏书签及 GitHub Pages 链接。将可扩展内容放入 `assets/`、`docs/`、`scripts/`，是兼顾清晰结构与向后兼容的选择。

## 技术复核与实验

第 01–28 章已有分批技术内容审计与逐章证据台账，修正了过时 API、版本敏感说法和过度绝对化的结论。查看 [本批复核报告](docs/reviews/chapters-01-07.md)、[证据清单目录](evidence/README.md) 和 [配套实验](labs/README.md)。

注意：静态结构检查、自动化浏览器冒烟测试及第 04 章用户态示例验收是不同测试层级。尚未在专门的隔离 VM/硬件上完成内核模块加载、完整 QEMU 启动、xv6 COW、eBPF/驱动及相关硬件实验；不能把源码级审阅等同于运行时验证。

## 静态校验

静态检查仅需 **Python 3.10+**；用户态实验执行还需要 Linux 和 C 编译器：

```bash
python3 scripts/check_site.py
python3 scripts/test_labs.py  # Linux + C 编译器，编译并运行 ch04 用户态实验
python3 -m http.server 8000
```

脚本检查课程 JSON、28 个章节、单一 H1、主要语义标签、章节前后导航、目录内锚点、相对链接和必要图示。它**不能替代**浏览器的桌面/移动端截图检查，也不能证明文章中的内核实验已在真实环境运行。详见 [内容规范](docs/guides/content-guide.md)。

## 内容来源与边界

概念学习可交叉参考 [Linux 内核官方文档](https://docs.kernel.org/)、[Linux man-pages](https://man7.org/linux/man-pages/)、[xv6 课程资源](https://pdos.csail.mit.edu/6.1810/) 和 [QEMU 文档](https://www.qemu.org/docs/master/)。章节中的命令和机制描述可能受发行版、CPU 架构或内核版本影响，不能把教学示例视作生产环境的操作指令。

本次结构与阅读体验改造遵循 [Olah-style Paper Posts](https://github.com/1998x-stack/Olah-style-posts) 所倡导的“先提出问题、逐步展开、可验证机制”原则；但本仓库是**操作系统课程**，不是论文复现，引用规则和验证范围需按内容调整。所有示意图均为本项目新绘制的解释性图，不代表 Linux 某一版本的逐行实现。

欢迎在 Issue 中指出事实、版本适用范围、实验复现与可访问性问题，修改请参见 [CONTRIBUTING.md](CONTRIBUTING.md)。
