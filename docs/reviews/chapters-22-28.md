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
