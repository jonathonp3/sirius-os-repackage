# Disable debug packages because we are repackaging a binary
%define debug_package %{nil}

Name:           sirius-os-winboat
Version:        0.9.0
Release:        1%{?dist}
Summary:        Repackaged Winboat optimized for Sirius-OS (Bazzite-based)
License:        GPLv3
URL:            https://github.com/jonathonp3/sirius-os-repackage
ExclusiveArch:  x86_64

Source0:        https://github.com/TibixDev/winboat/releases/download/v0.9.0/winboat-0.9.0-x86_64.rpm

BuildRequires:  cpio
BuildRequires:  rpm2cpio

Requires:       freerdp
Requires:       libwinpr
Requires:       libXScrnSaver

AutoReqProv:    no

%description
Repackaged Winboat optimized for Sirius-OS and Wolf-OS.

%prep
# Create a build directory and extract the RPM into it
%setup -c -T
rpm2cpio %{SOURCE0} | cpio -idmv

%install
# 1. Create the necessary directory structure
mkdir -p %{buildroot}%{_libexecdir}/winboat
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_prefix}/lib/tmpfiles.d

# 2. Copy the files from the extracted 'opt/winboat' folder
# The %setup -c above ensures we are in the right spot
cp -rp opt/winboat/* %{buildroot}%{_libexecdir}/winboat/

# 3. Create the standard binary link
ln -sf %{_libexecdir}/winboat/winboat %{buildroot}%{_bindir}/winboat

# 4. Create the Desktop Entry
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

# 5. Create the tmpfiles.d entry
cat <<EOF > %{buildroot}%{_prefix}/lib/tmpfiles.d/sirius-os-winboat.conf
# Winboat legacy compatibility for Bazzite/Sirius-OS
L+ /opt/winboat - - - - %{_libexecdir}/winboat
EOF

%files
%attr(4755, root, root) %{_libexecdir}/winboat/chrome-sandbox
%{_libexecdir}/winboat/
%{_bindir}/winboat
%{_datadir}/applications/winboat.desktop
%{_prefix}/lib/tmpfiles.d/sirius-os-winboat.conf

%changelog
* Mon Jul 06 2026 Jonathon <jonathon@sirius-os> - 0.9.0-1
- Initial release of repackaged winboat

