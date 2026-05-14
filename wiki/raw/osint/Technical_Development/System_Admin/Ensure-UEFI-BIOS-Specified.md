---
tags: [qemu, uefi, bios, technical-development, system-admin]
---
### Ensure UEFI BIOS is Specified
If you are using UEFI, make sure you have specified the correct UEFI BIOS file. You can usually find this file as part of your QEMU installation or download it separately. For example:

```bash
-bios /usr/share/qemu-efi-aarch64/QEMU_EFI.fd
```