# 第 08–14 章技术内容复核记录

本批沿用 Olah-style Paper Posts 的工作方法：先提出读者可感知的问题，再沿数据结构与控制流解释机制；关键实现结论映射到官方手册、Linux 内核文档或上游源码。操作系统章节不机械套用论文 benchmark 要求，性能数字和个人经历若无可核对证据则删除。

## 本轮逐章优化

| 章节 | 核心问题与修正 |
| --- | --- |
| 08 · 进程管理 | 以 fork/exec 生命周期开篇；明确 task_struct 随版本和配置变化；将进程状态图标为教学抽象；补充 fork、execve、wait 的边界。 |
| 09 · 线程与协程 | 去除未经验证的游戏服务器性能故事；纠正线程切换必然不刷新 TLB、cache 必然保温的绝对化说法；区分 Linux 可调度任务、pthread 与用户态协程运行时。 |
| 10 · CPU 调度 | 删除无来源的调度器 CPU 百分比；校准 CFS/EEVDF 的关系与版本边界；区分公平调度类与实时/截止期限等其他调度类。 |
| 11 · 同步与互斥 | 删除未经证实的线上事故和 TCP 影响范围；纠正 Mars Climate Orbiter 事故归因（单位混用，不是竞态条件）；区分竞态条件与语言内存模型中的数据竞争。 |
| 12 · 虚拟内存 | 以 MMU、页表、TLB、缺页处理的地址翻译路径开篇；明确虚拟内存不等于 swap；强调地址宽度与页表层级依赖架构和配置。 |
| 13 · 物理内存管理 | 以分配与回收两条路径组织内容；明确 Buddy 分配受 NUMA/zone/GFP 等约束；校准 swappiness 不是 swap 启停开关。 |
| 14 · 文件系统 | 以路径解析与数据读取链路开篇；区分 VFS 抽象与底层对象；校准 ext4 ordered 模式、unlink 生命周期、O_DIRECT 与持久化语义。 |

## 证据清单

新增 `evidence/08.json` 至 `evidence/14.json`，覆盖进程系统调用、线程模型、EEVDF、公平调度、数据竞争、内核锁、页表、TLB、Buddy/SLUB、MGLRU、VFS、ext4、Btrfs 与 fsync 等关键论断。证据状态分为 verified、derived、illustrative 和 unverified；来源定位记录在各 JSON 文件中。

## 验证边界

- 已通过 GitHub 文件接口逐项更新章节，并为本批建立证据台账。
- 已扩展 `scripts/check_site.py`，使静态校验覆盖第 01–14 章证据文件。
- 本轮没有在本地 Linux VM 中执行 fork/clone、调度、内存压力或文件系统实验；没有编译内核代码。
- 本轮没有执行 Chromium/Playwright 的桌面/移动端截图、键盘交互和打印验收；不能据此声称浏览器 QA 通过。
- GitHub Actions 是否通过，以本批最新提交触发的 workflow 结果为准；GitHub Pages 是否部署成功也需单独检查。

## 第二轮版本敏感事实复核（2026-11）

再次逐段检查后，发现既有复核记录未完全反映在正文中的残留问题，已直接修正：

| 章节 | 本次追加修正 |
| --- | --- |
| 08 | 移除“Linux 5.x 后内核栈统一使用 vmalloc”的概括；说明 VMAP_STACK 依赖配置/架构；避免将 COW fork 复杂度简化成固定 O(页表大小)。 |
| 09 | 修正 fork/clone 的 libc 包装层描述；删除 pthread/Goroutine 固定耗时和固定栈大小对比；补充 Go goroutine 初始栈策略及协程可被底层线程抢占的边界。 |
| 10 | 将 sched_ext 说明为内核可扩展调度类与 BPF scheduler 协作，而非“用户态调度器”；移除伪造的 sched_ops 结构体；限定 PREEMPT_RT 6.12 合入不等于发行版默认启用，并删除无测试依据的延迟数字。 |
| 11 | 移除手写 x86 LOCK CMPXCHG 自旋锁示例；补充 PREEMPT_RT 下 spinlock_t/raw_spinlock_t 语义差异；删除无来源的 RCU 使用数量；限定 lockdep 的运行路径覆盖范围。 |
| 12 | 移除固定 TLB 周期表；将旧 do_page_fault 名称改为架构/版本相关入口；纠正 major fault 不等于 swap-in；删除无证据的 Redis 故事和大页固定性能收益；说明 mTHP 尺寸取决于系统。 |
| 13 | 纠正 memory.low/high/max 语义；把 cgroup v2 写入值改为字节数；说明 controller 启用与委派前提；删除“每个容器自动拥有 memcg”的绝对化说法。 |
| 14 | 将旧 readpage/read_ext4_readpage 路径更新为 read_folio/readahead 概念接口；纠正 Bcachefs 在 Linux 6.17/6.18 的维护状态变化；将 EROFS 容器集成限定到 containerd snapshotter/differ。 |

本次追加证据写入各章 `evidence/08.json` 至 `evidence/14.json`。其中 sched_ext、PREEMPT_RT、mTHP、cgroup v2、VFS read_folio、Bcachefs 和 EROFS 的论断增加了当前上游文档/源码入口。

### 本次验证边界

- 已对照上游 Linux 文档、man-pages、Go runtime 源码和 containerd 文档修正版本敏感描述。
- 这是一轮文档与接口事实核验，不代表所有示例都已在真实 Linux VM 上编译运行。
- 没有执行 fork/clone 压测、sched_ext BPF 加载、PREEMPT_RT 延迟测试、内存压力实验或真实文件系统故障注入。
- 需要执行这些实验时，必须固定内核版本、架构、配置和工具链，并记录实测环境与输出。
