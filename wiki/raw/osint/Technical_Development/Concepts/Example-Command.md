---
tags: [qemu, arm, ide, technical-development, example]
---
### Example Command
Here's an example command that sets up a QEMU instance with an ARM architecture and an IDE drive:

```bash
qemu-system-aarch64 \
  -machine virt \
  -cpu cortex-a53 \
  -m 1024 \
  -drive if=none,file=disk_image.img,id=drive0 \
  -device ide-hd,drive=drive0,bus=ide.0,unit=0 \
  -nographic
```
