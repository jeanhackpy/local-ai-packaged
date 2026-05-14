### Corrected QEMU Command:

```bash
qemu-system-aarch64 \
  -machine virt \
  -cpu cortex-a57 \
  -m 512M \
  -drive if=none,media=disk,id=drive0,file=/Users/Jeanphil/Library/Containers/com.utmapp.UTM/Data/Documents/CSI.utm/Data/CSI.qcow2,discard=unmap,detect-zeroes=unmap \
  -device usb-ehci,id=ehci \
  -device usb-storage,bus=ehci.0,drive=drive0 \
  -bios /usr/share/qemu-efi-aarch64/QEMU_EFI.fd \
  -nographic
```