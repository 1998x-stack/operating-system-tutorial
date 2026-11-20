# 第 10 章实验：只读观察 Linux 调度属性

## 运行

~~~bash
chmod +x observe.sh
./observe.sh
~~~

脚本只读取当前 shell（或指定 PID）的调度策略、nice/RT priority、CPU 亲和性与内核版本，不修改调度策略。

## 可选：记录一个短任务

若安装了 perf 且当前用户有权限：

~~~bash
perf sched record -- sleep 1
perf sched timehist
~~~

权限可能受 perf_event_paranoid、CAP_PERFMON、容器限制和发行版策略影响。采样与跟踪本身会带来观测开销。

## 安全边界

本实验不设置 SCHED_FIFO/SCHED_RR，也不运行高优先级忙循环。不要在远程生产主机上用实时优先级实验；错误配置可能让普通任务长时间得不到 CPU。
