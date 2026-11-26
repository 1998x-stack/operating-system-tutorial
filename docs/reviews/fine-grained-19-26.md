# 第 19–26 章逐篇精细化复核

更新日期：2026-11（第四批）

## 范围与方法

延续 [第 11–18 章](fine-grained-11-18.md) 的做法，按章节顺序逐篇提交，不批量重写已有内容。每篇新增一个围绕具体问题展开的 **机制追踪**、一个明确环境/步骤/预期/清理要求的 **只读微实验**，并为原先缺图的章节补一张原创解释图。新增段落全部落在既有 `19.html`–`26.html` 的章节目录、锚点、前后导航与图示范围内。

新增内容不声称对某一 Linux 版本给出完整调用栈，也不把只读观察实验写成已经实测的内核运行时结论。

| 章节 | 机制追踪 | 只读微实验 | 本次技术校准 |
| --- | --- | --- | --- |
| 19 · 网络协议栈 | 一次 `send()` 沿 socket/TCP/IP/链路层的加头与决策路径 | `ss`/`nstat` 观察连接队列与溢出计数 | 区分半连接/全连接队列；`somaxconn` 只约束全连接队列 |
| 20 · eBPF | 一条 `bpftrace` 从编译、验证到挂载与 Map 读取 | BTF、`unprivileged_bpf_disabled`、已加载程序列举 | 程序只能经 Map 交换数据；验证器 + 权限是双重边界 |
| 21 · 虚拟化 | 一次 `KVM_RUN` 到 VM-Exit 的进入/退出循环 | `systemd-detect-virt`、`/proc/stat` steal | vCPU 是宿主线程；`steal` 需两次采样做差 |
| 22 · 容器 | 启动容器时命名空间、挂载、cgroup 与权限的叠放顺序 | `/proc/self/ns`、`/proc/self/cgroup` 对比 | inode 编号只说明是否同一命名空间，不等于隔离强度 |
| 23 · 内核调试 | 内核 panic 后 kdump/vmcore 证据链的形成 | `kexec_loaded`、`crashkernel`、`/var/crash` 核对 | 符号不匹配会误读 `bt`；验证转储会重启系统，未执行 |
| 24 · 性能分析 | 一次 `perf record` 采样到火焰图的聚合与可视化 | PSI、`vmstat` 做差、`perf stat true` | 最宽色块不必然可优化；均值掩盖尾延迟 |
| 25 · 写一个小OS | 一次 `iret` 从 Ring 0 到 Ring 3 的前置条件 | 工具链版本与引导扇区 512 字节/`55aa` 核对 | 长模式下隔离主要靠页表权限而非段 |
| 26 · 前沿趋势 | 判断前沿说法成熟度的证据分层核对 | 本机 Rust 配置与机密计算标记核对 | 本机能力不能外推为生态已采用 |

## 新增图示

- `assets/diagrams/net-path.svg`（19）：TCP 收发分层路径与 Netfilter 钩子位置。
- `assets/diagrams/ebpf-lifecycle.svg`（20）：eBPF 加载、验证、挂载与 Map 通道。
- `assets/diagrams/kvm-vcpu.svg`（21）：KVM/QEMU 组件边界、vCPU 线程与 virtio 数据路径。
- `assets/diagrams/crash-analysis.svg`（23）：kdump 到离线 `crash` 分析的证据链。
- `assets/diagrams/perf-workflow.svg`（24）：诊断流程与各子系统工具、常见陷阱。
- `assets/diagrams/boot-to-user.svg`（25）：从固件到 Ring 3 的最小启动链。
- `assets/diagrams/frontier-map.svg`（26）：前沿方向按成熟度分层核对。

各图均为本项目新绘制的解释性概念图，图注已注明是简化示意，不代表某一内核版本的具体实现。第 22 章沿用既有 `assets/diagrams/container-layers.svg`。

## 前端与自动化验收

- 新增复用组件沿用 `.deep-dive`、`.practice-card`、`.causal-steps`，保留手机端滚动代码、关于代码块内 `&lt;` 的转义、键盘可打开的 `details`、语义标签与章节目录。
- 修正第 23、26 章代码块后多余的字符与第 23 章 `.article-body` 提前闭合的问题。
- Playwright 冒烟测试的机制追踪/实验卡片断言从第 01–18 章扩展到第 01–26 章。
- 本批以本地 `http.server` + 浏览器检查在 1440/390/360 px 下逐页抽查：无横向溢出、无 JS 报错、无断图，每页恰有一个机制追踪与一个实验卡片，`details` 可用键盘聚焦展开。

## 验证边界

本轮更新的是静态 HTML、新增 SVG、证据 JSON 与浏览器检查脚本覆盖。新增实验均为只读观察，**未**在真实硬件或隔离 VM 上完成 kdump 转储验证、KVM/容器隔离压测、Rust 内核模块加载或机密计算部署；也未宣称所有只读命令都在某个特定主机与内核版本上执行成功。

## 下一批顺序

按同样标准可继续精修第 27–28 章（内核设计决策、综合项目），并复核第 01–18 章新增交互在最新内核上的描述是否需要更新。
