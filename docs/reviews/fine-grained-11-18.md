# 第 11–18 章逐篇精细化复核

更新日期：2026-11-25

## 范围与方法

延续 [第 01–05 章](fine-grained-01-05.md) 与 [第 06–10 章](fine-grained-06-10.md) 的做法，按章节顺序逐篇提交，不批量重写已有内容。每篇新增一个围绕具体问题展开的 **机制追踪**、一个明确环境/步骤/预期/清理要求的 **只读微实验**，并为原先缺图的章节补一张原创解释图。新增段落全部落在既有 `11.html`–`18.html` 的章节目录、锚点、前后导航与图示范围内。

新增内容不声称对某一 Linux 版本给出完整调用栈，也不把只读观察实验写成已经实测的内核运行时结论。

| 章节 | 机制追踪 | 只读微实验 | 本次技术校准 |
| --- | --- | --- | --- |
| 11 · 同步与互斥 | 争用中的 `mutex_lock()`：快速路径 → 乐观自旋 → 睡眠 → 释放唤醒 → futex 边界 | `strace -e trace=futex` 观察用户态互斥锁何时落到 futex | 用户态 mutex 无竞争时不进入内核；锁释放不保证先到先得 |
| 12 · 虚拟内存 | 从 TLB miss（硬件）到 page fault（内核）的分界与缺页分流 | `getrusage()` 缺页计数与 THP 开关，观察按需分配 | TLB miss 不是异常；minor fault 数量不能换算成物理内存用量 |
| 13 · 物理内存管理 | 一次 `kmalloc()` 小对象分配：选缓存 → per-CPU slab → 向伙伴系统补页 | `/proc/buddyinfo`、`/proc/meminfo`、sysfs 观察分层供给 | Slab 用量 ≠ 应用内存；buddyinfo 只反映页粒度空闲块 |
| 14 · 文件系统 | `open()` 返回的 fd 与 dentry、inode、`struct file` 的关系 | `stat`/`ls -li`/`/proc/<pid>/fd` 观察 inode 与 fd | 删除文件名不等于删除数据；偏移在 `struct file` 上 |
| 15 · I/O 模型与 io_uring | `io_uring_submit()` 后内核如何发现请求并写回 CQE | `strace` 追踪 epoll，对比就绪通知与完成通知 | epoll 只是就绪通知；完成可能乱序，需用 `user_data` 匹配 |
| 16 · 设备驱动 | 一次字符设备 `read()` 从设备号到驱动回调 | `/proc/devices`、`/dev`、sysfs 观察主设备号与设备模型 | 设备节点是接口，不等于硬件寄存器；必须用 `copy_to_user` |
| 17 · 中断与异常处理 | 一次网卡收包中断的上半部/下半部分工 | `/proc/interrupts`、`/proc/softirqs`、`threadirqs` 只读观察 | 计数值不代表处理耗时；软中断/线程化边界因配置而异 |
| 18 · 时间管理 | 一个 `hrtimer` 到期：红黑树 → 时钟事件编程 → 中断 → 回调 | `current_clocksource` 与 REALTIME/MONOTONIC 对比 | HZ 不等于定时器精度上限；测时长应用 MONOTONIC |

## 新增图示

- `assets/diagrams/lock-contention.svg`（11）：自旋锁忙等与互斥锁睡眠唤醒两条路径对比。
- `assets/diagrams/buddy-split-merge.svg`（13）：伙伴系统 order 2 块的分裂与合并规则。
- `assets/diagrams/vfs-lookup.svg`（14）：应用 → VFS → 页缓存 → 块设备的分层数据流。
- `assets/diagrams/io-uring-rings.svg`（15）：SQ/CQ 环形队列与 head/tail 指针关系。
- `assets/diagrams/chardev-path.svg`（16）：字符设备 `read()` 的分层调用路径。
- `assets/diagrams/irq-top-bottom.svg`（17）：中断上半部/下半部拆分原则。
- `assets/diagrams/time-bases.svg`（18）：两种时间基准与底层时钟源、jiffies/hrtimer 的关系。

各图均为本项目新绘制的解释性概念图，图注已注明是简化示意，不代表某一内核版本的具体实现。第 12 章沿用既有 `assets/diagrams/virtual-memory.svg`。

## 前端与自动化验收

- 新增复用组件沿用 `.deep-dive`、`.practice-card`、`.causal-steps`，保留手机端滚动代码、键盘可打开的 `details`、语义标签与章节目录。
- Playwright 冒烟测试的机制追踪/实验卡片断言从第 01–10 章扩展到第 01–18 章。
- 本批以本地 `http.server` + 浏览器检查在 1440/390/360 px 下抽查：无横向溢出、无 JS 报错、无断图，每页恰有一个机制追踪与一个实验卡片，`details` 可展开。

## 验证边界

本轮更新的是静态 HTML、新增 SVG、证据 JSON、共享样式与浏览器检查。新增实验均为只读观察，**未**在真实硬件或隔离 VM 上完成内核模块加载、io_uring 高并发压测、中断延迟测量或时钟源精度对比；也未宣称所有只读命令都在某个特定主机与内核版本上执行成功。

## 下一批顺序

按同样标准依次精修第 19–23 章：网络协议栈、eBPF 可观测性、虚拟化技术、容器与命名空间、内核调试技术。每篇先核对版本敏感的接口与数据结构，再补因果路径与可复现的只读练习，最后更新 CI 覆盖。
