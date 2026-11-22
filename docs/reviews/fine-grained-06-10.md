# 第 06–10 章逐篇精细化复核

更新日期：2026-11-22

## 范围与方法

延续 [第 01–05 章逐篇精细化](fine-grained-01-05.md) 的做法，按章节顺序逐篇提交，不批量重写已有内容。每篇新增一个围绕具体问题展开的 **机制追踪**，以及一个明确环境、步骤、预期与清理要求的 **只读微实验**。新增段落全部落在既有 `06.html`–`10.html` 章节目录、锚点、前后导航与图示范围内。

新增内容不声称对某一 Linux 版本给出完整调用栈，也不把只读观察实验写成已经实测的内核运行时结论。

| 章节 | 机制追踪 | 只读微实验 | 本次技术校准 |
| --- | --- | --- | --- |
| 06 · OS内核源码初探 | Kconfig 选项 → `.config` → Kbuild `obj-$()` → 构建产物 → 运行时校验后加载 | 核对目标内核的配置与构建树（`uname -r`、`/lib/modules/*/build`、`CONFIG_MODULES`、`modinfo`） | 修改 `.config` 不会自动让模块出现；`build` 目录缺失或版本不匹配会导致外部模块构建失败 |
| 07 · OS实验环境搭建 | `-S` → `-gdb` 打开回环 gdbstub → `target remote` 绑定符号 → 断点由 QEMU 执行 → 继续/单步 | 只读核对 QEMU/GDB/裸机 RISC-V 工具链是否存在及其版本 | QEMU gdbstub 不依赖 `CONFIG_KGDB`；`riscv64-linux-gnu-gcc` 不能替代 xv6 的 newlib 工具链 |
| 08 · 进程管理 | `copy_process()`：任务身份独立 → `copy_mm()` 共享页表 → 打开文件对象共享 → 写入触发 COW 缺页 → 僵尸与 `wait()` 回收 | 只读观察 `Pid/PPid/Threads`、`smaps_rollup` 共享/私有计数与 `sh -c` 的父子 PID | 内存页写时复制与文件描述符共享内核对象是两类行为；内存计数不能直接换算成 COW 次数 |
| 09 · 线程与协程 | `clone()` 的 `CLONE_*` 标志：`CLONE_VM` 共享地址空间 → `CLONE_FILES/FS` 共享文件上下文 → `CLONE_SIGHAND/THREAD` 组成线程组 → 执行上下文仍独立 | 只读观察 `Pid/Tgid/Threads`、`/proc/self/task` 与 `ps -eLf` 的 LWP 列 | 共享地址空间不保证访问顺序；内核按任务而非按进程调度 |
| 10 · CPU调度 | EEVDF 两步选择：先判 eligibility（`lag` 非负），再在合格实体中取最早 virtual deadline → 运行后回插红黑树 | 只读观察 `/proc/self/sched`、`ps -cls` 与 `sched_rt_period_us`/`sched_rt_runtime_us` | “总选 vruntime 最小者”是简化；实时类与截止时间类不随 EEVDF 改变 |

## 新增图示

- 第 08 章新增 `assets/diagrams/fork-cow.svg`：父/子页表先只读共享同一物理页，写入触发缺页后子进程获得私有可写页。
- 第 09 章新增 `assets/diagrams/thread-models.svg`：M:1、1:1、M:N 三种用户态线程到内核可调度实体的映射。

两图均为本项目新绘制的解释性概念图，图注已注明是简化示意，不代表某一内核版本的具体实现。其余章节沿用既有图示。

## 前端与自动化验收

- 新增复用组件沿用 `.deep-dive`、`.practice-card`、`.causal-steps`，保留手机端滚动代码、键盘可打开的 `details`、语义标签与章节目录。
- Playwright 冒烟测试的机制追踪/实验卡片断言从第 01–05 章扩展到第 01–10 章。
- 本批使用本地 `http.server` + Playwright 在 1440/390/360 px 下检查：无横向溢出、无 JS 报错、无断图，每页恰有一个机制追踪与一个实验卡片，`details` 可展开。

## 验证边界

本轮更新的是静态 HTML、新增 SVG、证据 JSON、共享样式与浏览器检查。新增实验均为只读观察，**未**在真实硬件或隔离 VM 上完成模块加载、QEMU Guest 启动、xv6 运行或实时延迟测量；也未宣称所有只读命令都在某个特定主机与内核版本上执行成功。

## 下一批顺序

按同样标准依次精修第 11–15 章：同步与互斥、虚拟内存、物理内存管理、文件系统、I/O 模型与 io_uring。每篇先核对版本敏感的接口与数据结构，再补因果路径与可复现的只读练习，最后更新 CI 覆盖。
