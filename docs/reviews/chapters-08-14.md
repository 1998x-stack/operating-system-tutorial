# 第 08–14 章技术内容复核记录

本轮按 Olah-style Paper Posts 的证据、因果叙事、SVG 机制图与可复现实验要求审阅。课程内容采用“问题 → 机制 → 观察 → 边界”的组织方式；不虚构个人经历、性能数字或实验输出。

## 本轮重点修正

| 章节 | 主要修正 |
| --- | --- |
| 08 进程管理 | 将 task_struct 明确为每个可调度 task 的内部描述；区分 state 与 exit_state；修正 D 状态、COW、fork 成本和 execve 映像切换描述 |
| 09 线程与协程 | 纠正 CLONE_SIGHAND 对应 sighand_struct；去掉 pthread/Goroutine 固定切换数字；说明 goroutine 栈大小随运行时调整；澄清 await 的 I/O 仍依赖内核 |
| 10 CPU 调度 | 更新 EEVDF 的过渡描述；纠正 sched_ext 的 BPF 内核执行边界；修正实时优先级、SCHED_DEADLINE 与 PREEMPT_RT 的适用范围 |
| 11 同步与互斥 | 移除 Mars Climate Orbiter 竞态错误归因和无来源 TCP 案例；区分竞态条件与数据竞争；补充 PREEMPT_RT 锁语义、RCU 宽限期与 lockdep 覆盖边界 |
| 12 虚拟内存 | 区分 TLB miss 与 page fault；修正 LA57 地址位数检测命令；移除固定 TLB 周期数和大页性能提升；澄清 major fault 不等于 swap |
| 13 物理内存管理 | 修正基础页大小与 order 定义；更新 SLUB Sheaves/Barns 到 Linux 7.0 开发线；修正 MGLRU、direct reclaim 与 memory.low 的语义 |
| 14 文件系统 | 更新 VFS folio/read_folio 接口；纠正路径查找和 dentry 解释；区分 write()、writeback、fsync 与持久性；更新 Btrfs 自修复和 Bcachefs 上游状态 |

## 证据与图示

- 新增 `evidence/08.json` 至 `evidence/14.json`，记录 36 条本批关键技术论断。
- 新增 7 张原创 SVG：进程生命周期、线程模型、EEVDF 选择、同步原语/RCU、虚拟地址翻译、物理内存层次、VFS 写回路径。
- 每章延伸阅读区链接到内核官方文档、man-pages、语言文档或上游源码，并可直接打开对应证据清单。

## 配套实验

- `labs/ch08-process/`：fork、COW 与 exec
- `labs/ch09-threads/`：pthread 与互斥锁
- `labs/ch10-scheduler/`：只读观察调度策略与 CPU 亲和性
- `labs/ch11-sync/`：线程竞态与 ThreadSanitizer
- `labs/ch12-vm/`：匿名映射与 fork COW
- `labs/ch13-memory/`：buddy、slab、PSI 与 cgroup 只读观测
- `labs/ch14-filesystem/`：write、fsync 与 rename 持久性路径

## 验证边界

- 本轮对章节内容、命令和接口按官方文档/上游源码进行静态复核；新增示例以可复制、低风险为目标。
- 尚未在实际 Linux VM 中编译运行全部 C 实验、执行 ThreadSanitizer 或进行 cgroup 压力测试；不得将其标记为运行时已验证。
- 尚未完成 Chromium/Playwright 的 1440px、768px、390px、360px、打印、键盘与离线浏览器验收。
- 文章中的性能差异不作通用数值承诺；应在具体 CPU、内核、发行版与工作负载下测量。
