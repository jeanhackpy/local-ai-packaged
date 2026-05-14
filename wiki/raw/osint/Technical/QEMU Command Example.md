### QEMU Command Example

```bash
qemu-system-aarch64 \
  -machine virt \
  -cpu cortex-a53 \
  -m 1024M \
  -drive file=your_bootable_image.iso,media=cdrom,if=none,id=cdrom0 \
  -device usb-ehci,id=ehci \
  -device usb-storage,bus=ehci.0,drive=cdrom0 \
  -bios /usr/share/qemu-efi-aarch64/QEMU_EFI.fd \
  -nographic
```