# Disable debug packages because we are repackaging a binary
%define debug_package %{nil}

Name:           sirius-os-winboat
Version:        0.9.0
Release:        3%{?dist}
Summary:        Repackaged Winboat optimized for Sirius-OS (Bazzite-based)
License:        GPLv3
URL:            https://github.com/jonathonp3/sirius-os-repackage
ExclusiveArch:  x86_64

Source0:        https://github.com/TibixDev/winboat/releases/download/v0.9.0/winboat-0.9.0-x86_64.rpm

BuildRequires:  cpio
BuildRequires:  rpm

Requires:       freerdp
Requires:       libwinpr
Requires:       libXScrnSaver

AutoReqProv:    no

%description
Repackaged Winboat optimized for Sirius-OS and Wolf-OS.

%prep
%setup -c -T
rpm2cpio %{SOURCE0} | cpio -idmv

%install
mkdir -p %{buildroot}%{_libexecdir}/winboat
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/
mkdir -p %{buildroot}%{_prefix}/lib/tmpfiles.d

# Copy binaries
cp -rp opt/winboat/* %{buildroot}%{_libexecdir}/winboat/

# Copy icon (Extracted from the source RPM)
cp -p usr/share/icons/hicolor/scalable/apps/winboat.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/

# Create symlink
ln -sf %{_libexecdir}/winboat/winboat %{buildroot}%{_bindir}/winboat

# Create Desktop Entry
cat <<EOF > %{buildroot}%{_datadir}/applications/winboat.desktop
[Desktop Entry]
Name=Winboat
Exec=%{_bindir}/winboat
Icon=winboat
Type=Application
Categories=Utility;Game;
EOF

# Create tmpfiles.d entry
cat <<EOF > %{buildroot}%{_prefix}/lib/tmpfiles.d/sirius-os-winboat.conf
L+ /opt/winboat - - - - %{_libexecdir}/winboat
EOF

%files
%attr(4755, root, root) %{_libexecdir}/winboat/chrome-sandbox
%{_libexecdir}/winboat/
%{_bindir}/winboat
%{_datadir}/applications/winboat.desktop
# ADDED THIS LINE TO CLAIM THE ICON:
%{_datadir}/icons/hicolor/scalable/apps/winboat.svg
%{_prefix}/lib/tmpfiles.d/sirius-os-winboat.conf

%changelog
* Mon Jul 06 2026 Jonathon <jonathon@sirius-os> - 0.9.0-3
- Fix: Add missing icon file to the %files list

* Mon Jul 06 2026 Jonathon <jonathon@sirius-os> - 0.9.0-2
- Fix: included missing winboat.svg icon

* Mon Jul 06 2026 Jonathon <jonathon@sirius-os> - 0.9.0-1
- Initial release of repackaged winboat

