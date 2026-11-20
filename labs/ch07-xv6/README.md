# 第 07 章实验：MIT xv6-RISC-V

xv6 是 MIT 课程使用的教学操作系统，不是生产 Linux 发行版。请按当前课程和仓库版本安装 RISC-V newlib 工具链与支持 `riscv64-softmmu` 的 QEMU。

## 获取源码与构建

```bash
git clone https://github.com/mit-pdos/xv6-riscv.git
cd xv6-riscv
make
make qemu
```

工具链常见的裸机编译器名称是 `riscv64-unknown-elf-gcc`。发行版包名可能不同；不要把面向 Linux 用户空间的 `riscv64-linux-gnu-gcc` 自动当成等价替代品。

## 观察点

- `kernel/proc.c`：进程与调度相关路径
- `kernel/vm.c`：页表和地址空间
- `kernel/syscall.c`：系统调用分派
- `kernel/trap.c`：异常和中断入口
- `kernel/fs.c`：文件系统实现

进入 shell 后可运行 `ls`、`cat README`、`echo hello`。具体输出与实验分支可能变化，以所检出的 MIT 源码版本为准。
