# 第 13 章实验：内存分配与回收只读观测

## 运行

~~~bash
chmod +x inspect.sh
./inspect.sh
~~~

脚本只读取以下接口（若存在且当前用户有权限）：

- `/proc/buddyinfo`、`/proc/pagetypeinfo`：伙伴分配器空闲块与迁移类型信息
- `/proc/slabinfo`：slab 缓存统计
- `/proc/vmstat`：缺页、扫描、回收与 compaction 计数
- `/proc/pressure/memory`：内存 PSI
- cgroup v2 的 `memory.current`、`memory.events`、`memory.pressure`

## 解释边界

单次快照不能证明内存泄漏、碎片化故障或回收算法失效。需要结合时间序列、分配请求 order、NUMA/zone、cgroup 层级和工作负载。脚本不写 sysctl、不创建 cgroup，也不施加内存压力。
