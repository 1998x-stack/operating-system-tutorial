# 第二轮工程升级 · 第一阶段交付记录

## 目标

在保留 `01.html` 至 `28.html` 稳定链接的前提下，将课程首页、视觉规范、实验说明与自动化验收升级为可维护的平台基线。

## 本轮已落地

### 1. 首页与课程入口

- 重构首页 Hero、站点导航与快速入口。
- 新增四条目标导向学习路线：基础地图、资源管理、系统可观测性、系统工程。
- 新增统一学习方法：提出问题 → 画出路径 → 动手验证。
- 增加实验入口、项目说明、学习指南和页脚导航。
- 保留原有 28 个章节链接与四阶段课程分组。
- 同步修正第 26 章路线卡片中已不再适用的 LDOS 强断言式标签。

### 2. 全站视觉系统

- 在 `assets/css/site.css` 中统一色彩、边框、圆角、焦点态与排版基线。
- 优化首页卡片、学习路线、统计信息与站点导航。
- 增加 900px / 560px 响应式断点。
- 保留 reduced-motion、键盘焦点和打印样式。
- 章节页面继续共享原有 CSS 文件，不改动章节 URL。

### 3. 技术事实审计基线

- 保留 01–28 章 evidence JSON 台账。
- 将第 26 章首页/课程元数据中的研究方向描述与正文校准。
- 静态检查现在核对每章证据文件、状态字段、HTTPS 来源、重复 ID、章节链接和页内导航。
- 本轮没有声称已完成 28 章逐段源码级事实复核；既有证据台账是审计索引，后续仍需按章节核对版本敏感 API、代码路径与原始来源。

### 4. 实验可复现化

新增：
- `docs/guides/experiment-standard.md`
- `labs/EXPERIMENT_TEMPLATE.md`

更新四组已有实验文档：
- 第 04 章系统调用观察
- 第 06 章外部内核模块
- 第 07 章 QEMU + GDB
- 第 07 章 xv6-RISC-V

补充环境、预期结果、失败排查和清理说明。内核模块与调试实验明确要求在可回滚 VM 或专用实验机执行。

### 5. 自动化验收

新增：
- `tests/site.spec.mjs`
- `package.json`

GitHub Actions 现在包含：
- Python 静态站点检查：章节、导航、锚点、证据台账、实验文档结构。
- Playwright Chromium 冒烟测试：首页 360/390/1440px；28 章全部在 360/1440px 检查加载、H1/main/目录和横向溢出；并检查键盘 Skip Link。

## 验证边界

- GitHub Actions 的结果以本次提交对应的 workflow run 为准；提交时可能仍处于排队或运行中。
- Playwright 测试覆盖的是浏览器冒烟与首页多视口，不等于完整视觉回归、屏幕阅读器验收或每个章节的所有交互验收。
- 尚未在此轮执行四组实验的真实内核/硬件运行验证。
- 外部官方链接尚未进行全量在线可用性审计。
- 28 章的逐段 API/代码事实审计仍需分批进行；本轮建立了可持续执行的检查入口和记录规范。

## 下一轮建议顺序

1. 按 01–07、08–14、15–21、22–28 分批做逐段 API 与代码核验。
2. 对章节中的命令块建立架构/发行版/内核版本标签。
3. 扩展浏览器测试到全部章节的移动端与桌面端布局。
4. 为每个代码实验增加可自动运行的 smoke test 或明确标注人工验证。
5. 增加外链检查与链接失效报告，并在发布前人工复核重要上游文档。

## 第二轮逐章技术审计进展（2026-11）

在平台首页/视觉/实验/CI 升级之后，已继续执行 28 章技术事实审计：

- 01–07：保留第一轮逐章复核记录，详见 `docs/reviews/chapters-01-07.md` 与 `evidence/01.json`–`evidence/07.json`。
- 08–14：完成第二次版本敏感复核，修正 fork/clone、Go 栈、sched_ext、PREEMPT_RT、锁/RCU/lockdep、TLB/major fault/mTHP、cgroup v2、read_folio、Bcachefs 与 EROFS。
- 15–21：完成第二次版本敏感复核，修正 io_uring SQE mixed/ZC Rx/DMA-BUF、Rust for Linux、tasklet/threaded IRQ、NO_HZ/HZ、TCP backlog/syncookies、eBPF verifier/map、KVM 架构术语。
- 22–28：完成第二次版本敏感复核，修正 namespace/cgroup/OverlayFS、KASAN/kdump/kgdb、E820、Rust/LDOS/CoCo/PCIe IDE、宏内核/微内核比较、BPF runqlat、字符设备注册和 xv6 COW 实现边界。

每个批次的详细差异分别记录在：
- `docs/reviews/chapters-01-07.md`
- `docs/reviews/chapters-08-14.md`
- `docs/reviews/chapters-15-21.md`
- `docs/reviews/chapters-22-28.md`

各章 evidence ledger 已补充对应的上游文档、man-pages、架构规范、项目说明或课程实验来源。静态质量检查继续验证证据 JSON 结构、HTTPS 来源与页面/导航完整性。

### 本轮审计结论与限制

本次完成的是逐章正文/API/实现语义的文档级复核和代码示例修订，不等于 28 章所有代码都已通过编译、加载和运行。需要真实 VM/硬件才能验证的内容（内核模块、QEMU BIOS boot、KASAN/kdump/kgdb、io_uring ZC Rx、PCIe IDE、CoCo、sched_ext、eBPF loader、xv6 COW）均已明确标注验证边界；不得把“文档已审阅”表述成“实验已跑通”。
