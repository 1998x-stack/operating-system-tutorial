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
