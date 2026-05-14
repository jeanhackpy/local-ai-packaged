### Manual Booting Steps in UEFI Shell

1. **List the devices**:
   ```shell
   map -r
   ```

2. **Select the USB device**:
   ```shell
   fs0:
   ```

3. **Navigate to the boot directory**:
   ```shell
   cd EFI\boot
   ```

4. **Run the boot loader**:
   ```shell
   bootx64.efi
   ```

Using these steps, you should be able to configure QEMU to boot from a USB-attached ISO image. If you encounter any further issues, providing more details about your specific setup will help in diagnosing the problem.

User

QEMU error: QEMU exited from an error: qemu-aarch64-softmmu: VCPU supports less PA bits (36) than requested by the memory map (40)

ChatGPT

The error you're encountering, "VCPU supports less PA bits (36) than requested by the memory map (40)," indicates a mismatch between the physical address space supported by the virtual CPU and the memory configuration requested.