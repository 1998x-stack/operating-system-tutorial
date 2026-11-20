# 第 01–07 章技术内容复核记录

本轮以 Olah-style Paper Posts 的证据清单、因果叙事、原创 SVG 和可复现实验要求为参照。操作系统章节不是论文复现，因此将“实验结果”要求转化为：命令可复现、环境边界明确、输出不伪造、性能结论必须在具体平台测量。

## 本轮重点修正

| 章节 | 修正重点 |
| --- | --- |
| 01 | 删除无来源的 CPU 空闲率、服务器市场占比和个人经历；说明 OS 不是裸机执行的必要条件；区分 OS 职责与产品标签；修正 FreeRTOS、XNU 和 Windows NT 的架构描述 |
| 02 | 区分 ISA 与微架构；修正 ARM/RISC-V 指令编码的绝对化说法；移除无来源的功耗与延迟常数；区分 CPU cache 和 page cache；按架构解释中断/异常 |
| 03 | 将宏内核/微内核比较改为保护域与通信路径分析；删除 seL4“完全没有 bug”、固定 IPC 周期数等过度结论；修正 XNU、Windows 和 Unikernel 描述 |
| 04 | 区分 Ring、EL、RISC-V privilege modes；纠正 VMX root/SMM 与 Ring/EL 的错误对应；移除无来源 syscall/context-switch 纳秒表和生产占比；明确 syscall 不等于任务上下文切换 |
| 05 | 区分 BIOS 与 UEFI 启动接口；修正 Secure Boot 信任链、GPT/MBR 和 systemd-boot 的边界；解释 initramfs /init、rootfs 与 PID 1；纠正 systemd 的 Requires/Wants/After 语义 |
| 06 | 修正内核编码规范的 80 列建议；把 checkpatch 描述为辅助工具；修正外部模块 Kbuild 命令、Kconfig help 语法和 Makefile；移除可能依赖未导出符号的模块示例 |
| 07 | 区分 QEMU GDB stub 与 KGDB；将调试端口绑定 loopback；修正 xv6 的 newlib 工具链说明；删除伪造 perf/ftrace/bpftrace 输出；加入权限与观测开销说明 |

## 证据与来源

每章有独立的 evidence/0N.json，共记录 35 条关键技术论断，状态分为 verified、derived、illustrative 和 unverified。文章中的重要事实在邻近段落附有一手文档或上游项目链接。

## 配套实验

- labs/ch04-syscall/：最小 write() 程序与 strace 观察
- labs/ch06-hello-module/：外部内核模块源码、Kbuild Makefile 和加载步骤
- labs/ch07-qemu/：QEMU + GDB stub 调试流程
- labs/ch07-xv6/：MIT xv6-RISC-V 构建与观察点

## 验证边界

- 已做源码级逐项审阅和链接/文件存在性静态校验。
- 代码示例已按官方接口和文档修正，但**没有在实际 Linux VM 中编译、加载模块或启动 xv6**；这些运行结果不标记为已验证。
- 本轮尚未执行 Chromium/Playwright 的 1440px、768px、390px、360px、打印和键盘浏览器验收。
- 35 条证据清单只覆盖本批关键论断，不等于对文章每句话或所有硬件/内核版本做形式化证明。
