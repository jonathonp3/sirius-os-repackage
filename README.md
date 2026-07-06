# Sirius-OS Repackaging Source

This repository contains the RPM source files and SPEC configurations used to build system-level components for the **Sirius-OS** and **Wolf-OS** Atomic distributions. 

These packages are specifically optimized to work on immutable filesystems (Fedora Silverblue, Bazzite, Aurora) by adhering to `/usr/libexec` standards and managing legacy paths via `tmpfiles.d`.

## 📦 Included Packages

### [sirius-os-winboat](sirius-os-winboat.spec)
A repackaged version of Winboat that:
- Moves the application "truth" to `/usr/libexec/winboat`.
- Correctly sets SUID permissions for `chrome-sandbox`.
- Provides a native Desktop Entry in `/usr/share/applications`.
- Manages the legacy `/opt/winboat` symlink automatically via `tmpfiles.d`.

## 🚀 Build Pipeline

This repository is linked to the [Sirius-OS COPR Project](https://copr.fedorainfracloud.org/coprs/jonathonp3/sirius-os/). 

### How it builds:
1. Changes are pushed to this GitHub repository.
2. Fedora COPR triggers a build using the `rpkg` method.
3. The resulting RPM is hosted on the Fedora Community mirrors.
4. Sirius-OS builds pull the RPM during the `rpm-ostree` phase.

## 🛠 Maintenance

To update a package:
1. Replace the files in the corresponding `_files` folder (e.g., `winboat_files/`).
2. Update the `Version` and `Changelog` in the `.spec` file.
3. Push to GitHub.
4. (Optional) Manually trigger a build in the COPR dashboard if webhooks are not enabled.

## 📜 License
This packaging source is licensed under **GPL-3.0**. The software being packaged remains under its original upstream license.
