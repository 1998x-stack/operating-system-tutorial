# 第 22–28 章技术内容复核记录

本批完成全课程最后七章的导读重构、事实校准与证据台账。沿用 Olah-style Paper Posts 的问题驱动叙事：先明确工程问题，再解释内核机制与取舍；对于动态领域，明确区分上游已实现能力、研究原型与概念性讨论。

## 本轮逐章优化

| 章节 | 复核重点 |
| --- | --- |
| 22 · 容器与命名空间 | 解释 namespaces、cgroup v2、OverlayFS；强调容器隔离不等于完整安全边界，需结合 capabilities、seccomp、LSM 和运行时配置。 |
| 23 · 内核调试技术 | 按日志、崩溃转储、sanitizer、源码调试组织流程；说明 kdump、KASAN、UBSAN 和 kgdb 的配置与观测限制。 |
| 24 · 性能分析与调优 | 以基线和可证伪假设组织 perf、火焰图、fio、kmemleak；删除未经证实的个人压测故事和性能提升数字。 |
| 25 · 动手写一个小 OS | 明确 x86 BIOS/保护模式实验的架构边界；补充 QEMU、固件、交叉编译器、GDT/IDT 和特权级切换前提。 |
| 26 · 现代 OS 前沿趋势 | 去除过时的“当前最新内核版本”叙述；删除未经来源支持的 AI 调度提升比例、IPC 周期对比与 LionsOS 代码行数/吞吐等价结论；限定 seL4 形式化证明的适用范围。 |
| 27 · OS 内核设计决策 | 将宏/微内核比较改为约束与权衡；纠正 XFS 原生快照描述；补充 DKMS 不保证第三方模块兼容性的边界。 |
| 28 · 综合项目 | 统一实验环境、构建、验证和清理要求；补充驱动并发与锁上下文的边界，明确示例不可未经审计部署生产。 |

## 证据清单

新增 `evidence/22.json` 至 `evidence/28.json`，覆盖 namespaces、cgroup v2、OverlayFS、动态调试、kdump、KASAN/UBSAN、perf、fio、kmemleak、QEMU、xv6、Rust for Linux、seL4、RISC-V、机密计算、Linux 用户空间 ABI、BPF verifier 与字符设备等关键论断。

## 全课程工程收尾

- 静态校验扩展至 28 章证据台账。
- README 增加本批复核报告入口，证据索引更新为 01–28 章。
- 原有 `01.html` 至 `28.html` 稳定 URL 保持不变。
- 未在真实硬件/VM 中执行本批所有项目；未完成浏览器多视口人工验收。
- 动态技术趋势需持续按上游版本复核；本报告不声称所有章节示例均已在运行环境通过。

## 验收范围

本批静态检查以 GitHub Actions 为准。QEMU 启动、容器隔离、kdump、KASAN、eBPF、fio、perf、xv6 COW 和驱动并发等运行时测试，仍需在明确版本与可丢弃实验环境中单独完成。

## 第二轮版本敏感事实复核（2026-11）

对照 Linux 上游文档、BIOS/UEFI 规范、MIT xv6 实验说明和项目文档，追加修正：

| 章节 | 本次追加修正 |
| --- | --- |
| 22 | 展开 Linux 全部 8 种 namespace（含 cgroup/time）；纠正 user namespace 并不自动消除宿主机权限的绝对化描述；修正 memory.high/max 的 OOM 语义；说明 OverlayFS 写层在容器 stop/restart 与 remove 之间的生命周期差异；移除容器性能固定百分比。 |
| 23 | 将 KASAN 固定 2–3 倍开销和虚构个人经历改为依赖模式/架构/工作负载的说明；更新 KASAN 配置选项；修复 KGDB/QEMU 串口示例，移除非标准 GDB 命令；把所谓“真实 panic 案例”改为明确标注的假设排查流程。 |
| 24 | 复核 perf、火焰图与采样命令的语义；补充火焰图宽度是聚合采样栈占比而非函数 exclusive CPU 时间。 |
| 25 | E820 示例补充 SMAP 签名、CF、返回长度等检查，并明确代码是 BIOS 调用流程示意；强调内存图必须保留固件、MMIO、内核和引导数据区域。 |
| 26 | 删除随版本快速过期的 Rust 文件数量；纠正 Rust 安全边界、Binder/Nova/Maple Tree 成熟度描述；将 LDOS 限定为研究方向；修正 seL4/LionsOS 证明边界；收紧 PCIe IDE 与 CoCo 的硬件/运行时条件，删除虚构的通用 cococtl 命令。 |
| 27 | 删除 seL4 固定 IPC 周期数、Linux/seL4 代码行数和“驱动故障必然 panic”等不公平比较；改为按服务边界、故障隔离、证明范围和生态适配做定性比较。 |
| 28 | 修复 runqlat 示例中错误的 sched_switch context 读取和 wakeup 计时逻辑；区分 BPF load 与 tracepoint attach；补齐字符设备 cdev 注册/销毁和 sysfs 属性生命周期；将 xv6 COW 示例改为实现清单，补充引用计数、copyout、回滚与 cowtest/usertests 验收条件。 |

### 重要代码边界

- 第 28 章 eBPF 程序现在按 tracepoint raw context 字段建模，但仍是教学骨架；需使用目标内核的 BTF 生成 vmlinux.h，并由用户态 libbpf loader 显式 attach。PERCPU_ARRAY 的直方图需要用户态聚合每 CPU 值。
- 第 28 章字符设备代码补上了 cdev 与 sysfs 的生命周期骨架，class_create() 签名明确限定 Linux 6.4+；这不替代对目标内核版本的模块编译和加载测试。
- 第 28 章 xv6 COW 部分不再提供可能被误认为完整补丁的代码片段，明确要求实现 copyout() COW、引用计数与 kalloc/kfree 协同，并通过 cowtest/usertests。
- 第 25 章 E820 和第 23 章 KGDB 片段也明确区分流程示意与完整可编译实现。

### 本批新增证据

新增来源登记在 `evidence/22.json` 至 `evidence/28.json`，覆盖 namespace、cgroup v2、OverlayFS、KASAN、kdump、perf、BIOS E820、Rust for Linux、SEV-SNP/TDX、PCIe IDE、Confidential Containers、seL4、MIT xv6 COW lab 和 Linux tracepoint 文档。

### 验证边界

- 已完成文档/接口事实核验并修正高风险代码示例。
- 没有在真实 x86 BIOS VM 上执行本章 bootloader，也没有加载 KASAN/UBSAN 内核、配置 kdump 或实际连接 kgdb。
- 没有在真实设备上验证 PCIe IDE、SEV-SNP/TDX、CoCo、OverlayFS 性能或 perf 硬件事件。
- 第 28 章 BPF loader 和 xv6 COW 是明确的实现骨架/检查清单；不能把静态审阅误报为已通过编译与运行测试。
