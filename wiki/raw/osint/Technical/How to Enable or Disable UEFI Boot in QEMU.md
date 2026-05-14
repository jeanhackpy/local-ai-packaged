### How to Enable or Disable UEFI Boot in QEMU

#### To Enable UEFI Boot

Make sure you include the UEFI firmware file in your QEMU command, like this:

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

This command specifies that QEMU should use the UEFI firmware file `QEMU_EFI.fd`.

#### To Disable UEFI Boot

Remove the `-bios` option from your QEMU command to use the default BIOS firmware:

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

This command uses the default BIOS firmware provided by QEMU.