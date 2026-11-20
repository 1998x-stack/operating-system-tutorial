# 第 07 章实验：QEMU + GDB 调试 Linux 内核

本实验假设你已有同一次构建产生的 `vmlinux`、`arch/x86/boot/bzImage` 和一个含有可执行 `/init` 的 initramfs。

## QEMU 启动命令

```bash
qemu-system-x86_64 \
  -machine q35 -m 2G -smp 2 \
  -kernel ./arch/x86/boot/bzImage \
  -initrd ./rootfs.cpio.gz \
  -append "console=ttyS0 rdinit=/init nokaslr" \
  -display none -serial stdio -monitor none \
  -gdb tcp:127.0.0.1:1234 -S
```

- `-S`：Guest CPU 启动时暂停。
- `-gdb tcp:127.0.0.1:1234`：将调试端口限制在本机回环接口。
- `nokaslr`：仅为便于地址/符号对应而关闭这个 Guest 的 KASLR；不要用于生产系统。
- QEMU GDB stub 不要求内核启用 KGDB；两者是不同调试路径。

## GDB 连接

```gdb
gdb ./vmlinux
(gdb) target remote 127.0.0.1:1234
(gdb) break start_kernel
(gdb) continue
```

如果断点未命中，确认符号文件与启动镜像来自同一次构建、调试信息已保留、架构匹配，且 KASLR/重定位状态符合预期。

## 安全边界

不要把 GDB stub 暴露到公网或不可信网络。优先使用本机回环地址或 Unix socket；实验 Guest 与宿主机共享目录时，也要将 Guest 视为可能执行任意内核代码的环境。
