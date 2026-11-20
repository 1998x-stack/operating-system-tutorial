# 第 09 章实验：pthread 与互斥锁

## 构建与运行

~~~bash
make
./counter
~~~

4 个线程分别执行固定次数的递增操作，所有递增都由 pthread mutex 保护。预期最终计数为 1,000,000；如果创建/连接线程失败，程序会报错退出。

## 观察线程

在另一个终端运行程序时，可用：

~~~bash
ps -eLf -p <PID>
getconf GNU_LIBPTHREAD_VERSION
~~~

不同系统的线程实现和命令输出会不同。本实验展示 Linux 用户态线程库与 OS 线程的协作，不代表所有 POSIX 平台都使用 NPTL。
