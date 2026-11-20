# 第 04 章实验：观察 write() 系统调用

## 环境

Linux、C 编译器和 strace。不同发行版安装包名称可能不同。

## 构建与观察

```bash
cc -Wall -Wextra -O0 -g -o hello hello.c
strace -e trace=write ./hello
strace -c ./hello
```

关键观察：程序会调用一次面向文件描述符 1（标准输出）的 write。strace 输出中的启动阶段系统调用、耗时和格式会因 libc、动态链接器、内核及环境而异。

## 解释边界

- 这个程序使用 write()，不是 printf()，避免 stdio 缓冲混淆。
- strace 主要依赖 ptrace 等跟踪机制，会改变执行时序。
- 观察到一次系统调用不意味着发生了一次进程上下文切换。
