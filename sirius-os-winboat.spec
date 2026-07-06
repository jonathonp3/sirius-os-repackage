Name:           sirius-os-winboat
Version:        1.1.0
Release:        1%{?dist}
Summary:        Repackaged Winboat optimized for Sirius-OS (Bazzite-based)
License:        GPLv3
URL:            https://github.com/jonathonp3/sirius-os-repackage
BuildArch:      x86_64

# This tells COPR to download the original binary RPM directly from GitHub
Source0:        https://github.com/TibixDev/winboat/releases/latest/download/winboat-x86_64.rpm

# --- DEPENDENCIES ---
# Tools needed to unpack the Source0 RPM during the build process
BuildRequires:  cpio
BuildRequires:  rpm2cpio

# System libraries required for Winboat to run
Requires:       freerdp
Requires:       libwinpr
Requires:       libXScrnSaver

# Disables automatic dependency checking for internal Electron/Chrome shared libs
# that aren't provided by standard Fedora RPMs (it prevents dnf install failures).
AutoReqProv:    no

%description
Repackaged Winboat optimized for Sirius-OS and Wolf-OS. 
Places the immutable application 'truth' in /usr/libexec/winboat 
to comply with Fedora Atomic standards and manages the legacy 
/opt/winboat link via tmpfiles.d.

%prep
# Extract the original binary RPM into the build directory
# This happens in the COPR environment, keeping your GitHub repo tiny.
rpm2cpio %{SOURCE0} | cpio -idmv

%install
# 1. Create the necessary directory structure
mkdir -p %{buildroot}%{_libexecdir}/winboat
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_prefix}/lib/tmpfiles.d

# 2. Copy the files from the extracted 'opt/winboat' folder
cp -rp opt/winboat/* %{buildroot}%{_libexecdir}/winboat/

# 3. Create the standard binary link in /usr/bin
ln -sf %{_libexecdir}/winboat/winboat %{buildroot}%{_bindir}/winboat

# 4. Create the Desktop Entry for the app menu
cat <<EOF > %{buildroot}%{_datadir}/applications/winboat.desktop
[Desktop Entry]
Name=Winboat
Comment=Cloud Gaming via Winboat
Exec=%{_bindir}/winboat
Icon=winboat
Terminal=false
Type=Application
Categories=Utility;Game;
EOF

# 5. Create the tmpfiles.d entry INSIDE the RPM
cat <<EOF > %{buildroot}%{_prefix}/lib/tmpfiles.d/sirius-os-winboat.conf
# Winboat legacy compatibility for Bazzite/Sirius-OS
L+ /opt/winboat - - - - %{_libexecdir}/winboat
EOF

%files
# Set the SUID bit on the chrome-sandbox correctly at the package level
%attr(4755, root, root) %{_libexecdir}/winboat/chrome-sandbox
%{_libexecdir}/winboat/
%{_bindir}/winboat
%{_datadir}/applications/winboat.desktop
%{_prefix}/lib/tmpfiles.d/sirius-os-winboat.conf

%changelog
* Mon Jul 06 2026 Jonathon <jonathon@sirius-os> - 1.1.0-1
- Initial Sirius-OS release
- Switch to remote source fetching to bypass GitHub file size limits
- Integrated dependencies: freerdp, libwinpr, libXScrnSaver
- Integrated tmpfiles.d management for /opt/winboat
- Fixed /usr/libexec/ placement for Atomic/Silverblue compatibility

