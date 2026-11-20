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
