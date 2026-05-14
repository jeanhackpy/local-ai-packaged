---
tags: [uefi, boot, shell, technical-development, system-admin]
---
### Manual Boot from UEFI Shell
If you reach the UEFI shell again, you can manually boot from the image by using the following commands in the UEFI shell:

1. List the available file systems:

   ```shell
   fs0:
   ```

2. Navigate to the directory containing the EFI boot loader:

   ```shell
   cd EFI\boot
   ```

3. Start the boot loader:

   ```shell
   bootx64.efi
   ```