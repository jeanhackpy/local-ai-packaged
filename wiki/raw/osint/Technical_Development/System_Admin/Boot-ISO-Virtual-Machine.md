---
tags: [qemu, virtual-machine, uefi, bios, iso, technical-development]
---
### Boot the ISO in a Virtual Machine
You can try booting the ISO in a virtual machine with UEFI enabled and then with UEFI disabled (legacy BIOS mode). Here’s how you can do it using QEMU:

#### Boot with UEFI
```bash
qemu-system-aarch64 \
  -machine virt \
  -cpu cortex-a53 \
  -m 512M \
  -drive file=your_bootable_image.iso,media=cdrom,if=none,id=cdrom0 \
  -device usb-ehci,id=ehci \
  -device usb-storage,bus=ehci.0,drive=cdrom0 \
  -bios /usr/share/qemu-efi-aarch64/QEMU_EFI.fd \
  -nographic
```

#### Boot with BIOS (Legacy)
```bash
qemu-system-aarch64 \
  -machine virt \
  -cpu cortex-a53 \
  -m 512M \
  -drive file=your_bootable_image.iso,media=cdrom,if=none,id=cdrom0 \
  -device usb-ehci,id=ehci \
  -device usb-storage,bus=ehci.0,drive=cdrom0 \
  -nographic
```
Note: For aarch64 systems, the default BIOS might not be available, and UEFI is more commonly used.
