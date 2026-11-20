# 第 04 章实验：观察 write() 系统调用

## 环境

Linux、C 编译器和 strace。不同发行版安装包名称可能不同。

## 构建与观察

```bash
cc -Wall -Wextra -O0 -g -o hello hello.c
strace -e trace=write ./hello
strace -c ./hello
```

关键观察：程序会调用一次面向文件描述符 1（标准输出）的 write。示例只检查是否完整写入，不处理 EINTR 后重试；它是观察系统调用的最小程序，不是通用 I/O 封装。strace 输出中的启动阶段系统调用、耗时和格式会因 libc、动态链接器、内核及环境而异。

## 解释边界

- 这个程序使用 write()，不是 printf()，避免 stdio 缓冲混淆。
- strace 主要依赖 ptrace 等跟踪机制，会改变执行时序。
- 观察到一次系统调用不意味着发生了一次进程上下文切换。

## 预期结果

第一条命令应显示程序对文件描述符 1 的 `write(1, ...)` 调用及返回字节数；`strace -c` 应汇总系统调用计数。具体启动调用、耗时和输出格式因环境而异。若没有看到 write，确认 strace 安装成功且执行的是本目录刚编译的二进制。

## 清理

```bash
rm -f ./hello
```

## 实验记录

记录 `uname -a`、`cc --version`、`strace --version`，并保存两条命令的关键输出。不要将 strace 测得的耗时当作程序本身的无跟踪性能。
