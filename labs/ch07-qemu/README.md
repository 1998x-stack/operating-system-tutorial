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

## 预期结果

QEMU 启动后 Guest CPU 保持暂停，GDB 显示远程目标已连接；设置 `start_kernel` 断点后执行 continue，若符号和镜像匹配，应在内核启动路径命中断点。若 Guest 继续运行但未命中，检查 `vmlinux` 与 `bzImage` 是否来自同一构建、调试符号是否保留，以及架构和 KASLR 设置。

## 清理

在 GDB 中执行 `detach` 后退出 GDB；在 QEMU 终端按 `Ctrl-C` 结束 Guest。确认 QEMU 进程退出并释放本地 1234 端口。实验生成的内核、initramfs 与构建目录按需删除；不要删除共享或宿主机正在使用的镜像。
