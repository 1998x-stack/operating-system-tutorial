# 第 15–21 章技术内容复核记录

本批遵循 Olah-style Paper Posts 的叙事原则：以具体问题引入机制，沿控制流与数据结构逐步展开，并将实现细节链接到官方文档、规范或上游项目资料。操作系统教学文章不虚构作者经历；性能结论不提供无来源的固定百分比或保证性描述。

## 本轮逐章优化

| 章节 | 优化重点 |
| --- | --- |
| 15 · I/O模型与io_uring | 区分 readiness 与 completion；解释 io_uring SQ/CQ；明确零拷贝是减少特定路径的数据拷贝，不代表完全无复制。 |
| 16 · 设备驱动 | 从设备/总线/驱动匹配、probe 生命周期和用户数据访问展开；说明设备树、uaccess 与 Rust for Linux 的版本边界。 |
| 17 · 中断与异常处理 | 区分硬中断、softirq、tasklet、workqueue 与线程化中断；强调上下文约束和 PREEMPT_RT 语义差异。 |
| 18 · 时间管理 | 区分 clocksource、clockevent、jiffies、hrtimer 与用户可见时钟；校准单调时钟和墙上时钟的用途。 |
| 19 · 网络协议栈 | 沿发送/接收路径拆解 socket、传输层、NAPI、Netfilter、XDP 和 DPDK；指出实际路径依赖驱动与配置。 |
| 20 · eBPF可观测性 | 解释 verifier、BPF Map、kprobe 与 tracepoint；强调 verifier 不等于逻辑正确，也不消除追踪开销。 |
| 21 · 虚拟化技术 | 区分 KVM、QEMU、vCPU 与 virtio；纠正“虚拟机就是一个进程”的过度简化。 |

## 证据清单

新增 `evidence/15.json` 至 `evidence/21.json`，覆盖 epoll、io_uring、sendfile、Linux 设备模型、uaccess、设备树、Rust for Linux、generic IRQ、PREEMPT_RT、timekeeping、NAPI、Netfilter、XDP、BPF verifier、KVM API、QEMU 与 virtio 等关键论断。

## 验证边界

- 已通过 GitHub 文件接口逐章更新 15–21 HTML。
- 已新增 7 份章节证据台账，并扩展静态检查覆盖 01–21 章。
- 未在真实硬件上加载驱动、测试中断风暴或测量 I/O/网络性能。
- 未执行 eBPF 程序、KVM 虚拟机或 DPDK 的实际负载测试。
- 未完成 Chromium 多视口、键盘可访问性与打印样式人工验收；这些不应被视为已通过。
- GitHub Actions 和 Pages 部署状态以最新提交对应的 workflow 运行结果为准。

## 第二轮版本敏感事实复核（2026-11）

对照当前上游文档与接口后，追加修正：

| 章节 | 本次追加修正 |
| --- | --- |
| 15 | 纠正 IORING_SETUP_SQE_MIXED 的真实含义（64/128-byte SQE 混合）；收紧 ZC Rx 的硬件前提与 kernel-to-user payload copy 边界；将 DMA-BUF read/write 限定为文件/设备 opt-in 能力；纠正 io_uring 不保证所有操作均真正异步。 |
| 16 | 将 Rust 主线使用者列表改为当前项目维护的示例清单；移除“Linux 内核 70% 漏洞为内存安全问题”的错误归因；说明 Safe Rust 与 unsafe 边界，避免声称 Rust 自动消除所有数据竞争/UAF。 |
| 17 | 修正 tasklet 作为历史机制的定位；说明 tasklet 串行约束不等于驱动不需要锁；限定 PREEMPT_RT 的线程化中断存在例外；避免将 workqueue worker 数量写成每 CPU 固定一个。 |
| 18 | 修正 jiffies/HZ 与 NO_HZ 的关系；明确 HZ 不构成 hrtimer、clock_nanosleep 等接口的精度上限；修正 tickless 与用户态睡眠语义。 |
| 19 | 修正 SYN backlog 为 per-listener 语义；补充 syncookies 是 backlog 溢出时的后备机制而非容量调优；移除将 tcp_tw_reuse=1 当作通用 TIME_WAIT 优化的命令；补充 DMA/网卡发送路径中的 CPU 参与。 |
| 20 | 区分 perf event array 与 BPF ringbuf；修正 BPF map 样例的 PID/TID 取值和计数器注释；说明 verifier 对有界循环、复杂度与程序状态的约束。 |
| 21 | 移除 KVM 是 Type-2 Hypervisor 的绝对分类；限定 VMX root/non-root 为 Intel VT-x 术语；区分 KVM 内核 API、QEMU 用户态设备模型和架构相关 VM exit 行为。 |

本批追加证据已写入 `evidence/15.json` 至 `evidence/21.json`，新增上游链接覆盖 io_uring ZC Rx、SQE mixed、Rust for Linux 当前主线使用者、NO_HZ、TCP sysctl、BPF verifier/map 与 KVM API。

### 验证边界

- 本轮完成了文档/接口层面的事实修订与证据登记。
- 未在真实 NIC 上配置 ZC Rx、未执行 io_uring DMA-BUF NVMe I/O、未加载驱动、未运行 PREEMPT_RT 压测、未实际运行 KVM/DPDK/eBPF 性能实验。
- 设备树、DMA、中断、网络 offload 和 KVM 代码示例仍需在明确指定的架构、内核配置、驱动和硬件上进行编译/运行验收。
