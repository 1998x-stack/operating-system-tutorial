# 第 14 章实验：write、fsync 与 rename

## 在临时目录运行

~~~bash
mkdir -p /tmp/os-fsync-lab
cd /tmp/os-fsync-lab
cc -Wall -Wextra -O0 -g /path/to/operating-system-tutorial/labs/ch14-filesystem/durable_replace.c -o durable_replace
./durable_replace
cat os-tutorial.txt
~~~

程序执行的顺序是：

1. 创建临时文件并写入内容；
2. 对文件描述符调用 fsync；
3. close 后在同一目录中 rename；
4. 打开父目录并 fsync 目录项变更。

可用 `strace -e trace=openat,write,fsync,rename,close ./durable_replace` 观察系统调用顺序。

## 持久性边界

这是常见的原子替换/同步模式示例，不是对掉电恢复的实测，也不保证绕过所有设备固件、写缓存、电源保护与文件系统实现差异。请勿在重要目录或生产数据上做断电测试。
