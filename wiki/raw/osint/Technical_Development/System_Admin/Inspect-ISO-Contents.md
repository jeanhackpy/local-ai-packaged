---
tags: [iso, uefi, bios, technical-development, system-admin]
---
### Inspect the ISO Contents
If you have access to the ISO file’s contents, you can look for the presence of certain files that indicate UEFI or BIOS support:

- **UEFI**: Look for the presence of an `EFI` directory at the root of the ISO. This directory typically contains boot files for UEFI systems.
- **BIOS**: Traditional BIOS boot files will usually be located in the root or in a folder named `boot` or similar, and they won't have an `EFI` directory.