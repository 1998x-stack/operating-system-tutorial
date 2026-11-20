# 第 06 章实验：最小外部内核模块

**仅在可回滚的虚拟机或专用实验机中加载。** 内核模块运行在内核特权域，错误可能导致系统崩溃。

## 前置条件

- 正在运行的 Linux 内核及其匹配的 headers/build tree
- 与该内核匹配的编译器和 Kbuild 工具
- 允许加载此模块的签名与安全策略

## 构建

```bash
make
modinfo ./hello.ko
```

默认 KDIR 指向 `/lib/modules/$(uname -r)/build`。如果使用不同的目标内核，请显式设置 KDIR。

## 加载、观察与卸载

```bash
sudo insmod ./hello.ko
lsmod | grep '^hello'
sudo dmesg | tail
sudo rmmod hello
sudo dmesg | tail
```

如果加载失败，先检查 dmesg：可能原因包括 vermagic 不匹配、符号未导出、内核未启用模块支持或模块签名策略拒绝加载。启用强制签名验证的系统需要受信任密钥签名。

## 清理

```bash
make clean
```
