# 第三轮：实验可复现性与代码级验收

更新日期：2026-11-21

## 验收层级

| 层级 | 验证内容 | 当前状态 |
| --- | --- | --- |
| 静态站点 | 28 章文件存在、导航、锚点、证据 JSON 与必要实验文档 | GitHub Actions 自动执行 |
| 浏览器冒烟 | 章节页面在手机与桌面视口上的基本布局、链接与可访问性 | Playwright 自动执行；并不代表完整人工视觉验收 |
| 用户态运行 | 第 04 章最小 write() C 程序的实际编译、执行与输出断言 | `scripts/test_labs.py` 在 Linux CI 中执行 |
| 内核构建 | 第 06 章内核模块构建、模块版本与编译器兼容性 | 未纳入 CI；需固定 Linux 内核与 headers |
| 虚拟机集成 | 第 07 章 QEMU/GDB、xv6 构建与启动 | 未纳入 CI；需要独立 VM 测试镜像/工具链 |
| 硬件/权限实验 | eBPF、sched_ext、PREEMPT_RT、io_uring ZC Rx、DMA、驱动、KVM 等 | 未运行；需要特定版本、内核配置和隔离环境 |
| 综合项目 | 第 28 章 runqlat、字符设备、xv6 COW 与火焰图 | 仅教学骨架/实现清单；尚未完成端到端运行验收 |

## 新增的可执行测试

`python3 scripts/test_labs.py` 要求 Linux、Python 3.10+ 和可用的 C 编译器（可通过 `CC` 指定）。

测试在独立临时目录中执行以下步骤：

1. 用 `-std=c11 -Wall -Wextra -Werror -O0 -g` 编译 `labs/ch04-syscall/hello.c`。
2. 在 5 秒超时限制下运行生成的程序。
3. 验证退出码为 0、stdout 恰好为 `hello\n`、stderr 为空。
4. 自动删除临时编译产物，不更改系统配置、不调用 sudo。

失败时返回非零退出码并使 CI 失败。该验证检查的是程序的实际用户态行为，不等于验证 `strace` 的跟踪能力、时延或内核内部执行路径。

## 下一批实验提升的优先级

- 第 06 章：在固定 Linux kernel headers 的隔离 VM 中构建 hello module，拆分“编译成功”与“加载成功”两项验收；默认不在 GitHub hosted runner 上加载第三方教学模块。
- 第 07 章：固定 MIT xv6 课程 commit 与 QEMU / RISC-V 工具链版本，增加无图形控制台启动和有超时的交互测试。
- 第 20/28 章：固定 clang/libbpf/bpftool/kernel BTF，补全用户态 loader 和 BPF map 读取，对 verifier/attach/输出三个阶段分别报告状态。
- 第 28 章：为 xv6 COW 增加可独立套用的源码补丁及 `cowtest`、`usertests` 测试，失败回滚、引用计数和 `copyout()` 路径必须覆盖。

## 安全与可复现性边界

- 自动化运行的实验仅限非特权用户态代码，禁止在普通 CI 上直接修改宿主内核、网卡、sysctl、cgroup 配置或加载内核模块。
- 标记为 `verified` 的文献证据指来源/文档层面的核验，不代表程序已编译/加载。
- 不能声称所有 28 章实验已通过：当前可执行门禁仅覆盖第 04 章最小用户态示例。
- 每次真实实验都需保存 OS/架构、内核版本与配置、工具链、源码 commit、命令、退出码、关键输出、清理步骤与测试日期。
