# 第 11 章实验：数据竞争与互斥锁

## 安全版本

~~~bash
make safe
./counter-safe
~~~

两个线程共享一个计数器，所有递增操作都由 mutex 保护，最终结果应为 1,000,000。

## ThreadSanitizer 版本

~~~bash
make tsan
./counter-tsan
~~~

该目标通过 `UNSAFE` 宏移除互斥锁，并启用 ThreadSanitizer。若工具链支持，运行时应报告共享计数器上的数据竞争。数据竞争程序具有未定义行为，不能把某次错误计数当成稳定输出或性能基准。

## 边界

ThreadSanitizer 只能检测被执行并被检测器观察到的路径；它不是对并发程序正确性的形式化证明。部分平台或容器环境可能不支持 TSAN 运行时。
