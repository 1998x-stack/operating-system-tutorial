# 第 08 章实验：fork、COW 与 exec

## 环境

Linux、C 编译器和 POSIX 系统调用。建议在普通用户权限下运行。

## 构建

~~~bash
cc -Wall -Wextra -O0 -g cow.c -o cow
cc -Wall -Wextra -O0 -g exec_demo.c -o exec_demo
~~~

## 观察 COW

~~~bash
./cow
perf stat -e minor-faults,major-faults ./cow
~~~

父进程在 fork 前写入匿名私有映射。子进程修改自己的映射后，父进程仍应看到原值。perf 的 fault 计数包含进程启动和运行时其他缺页，不能把总数直接解释为单次 COW fault 的精确成本。

## 观察 exec

~~~bash
./exec_demo
strace -f -e trace=clone,fork,vfork,execve,wait4 ./exec_demo
~~~

exec 成功后不返回到原调用点，而是在同一进程中运行新程序映像。系统调用跟踪输出依 libc、架构与 strace 版本变化。

## 边界

这是用户态语义实验，不直接观察内核页表项，也不测量跨机器可比较的 fork/exec 延迟。
