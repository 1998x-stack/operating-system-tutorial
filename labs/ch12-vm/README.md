# 第 12 章实验：匿名映射与 fork COW

## 构建与运行

~~~bash
cc -Wall -Wextra -O0 -g cow_mmap.c -o cow_mmap
./cow_mmap
perf stat -e page-faults,minor-faults,major-faults ./cow_mmap
~~~

父进程先写入一个匿名私有映射页，再 fork。子进程修改自己的映射后，父进程仍应看到原字节。子进程的 minor-fault delta 只是辅助观察：getrusage 本身、运行时和其他访问也可能影响计数。

## 进一步观察

- 查看当前系统基础页大小：`getconf PAGESIZE`
- 查看内核是否报告 THP：`cat /sys/kernel/mm/transparent_hugepage/enabled`
- 查看当前 THP 统计：`grep -E 'AnonHugePages|ShmemHugePages|FileHugePages' /proc/meminfo`

这些接口提供系统状态线索，不表示本程序一定分配了 THP，也不暴露物理地址。
