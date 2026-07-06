Name:           sirius-os-winboat
Version:        1.1.0
Release:        1%{?dist}
Summary:        Repackaged Winboat for Sirius-OS
License:        GPLv3
URL:            https://github.com/jonathonp3/sirius-os-repackage
BuildArch:      x86_64

# URL to the original binary RPM
Source0:        https://github.com/TibixDev/winboat/releases/latest/download/winboat-x86_64.rpm

Requires:       freerdp, libwinpr, libXScrnSaver
BuildRequires:  cpio
AutoReqProv:    no

%description
Repackaged Winboat optimized for Sirius-OS.

%prep
# Extract the original RPM into the build directory
rpm2cpio %{SOURCE0} | cpio -idmv

%install
mkdir -p %{buildroot}%{_libexecdir}/winboat
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_prefix}/lib/tmpfiles.d

# Copy from the extracted 'opt/winboat' (the source RPM structure)
cp -rp opt/winboat/* %{buildroot}%{_libexecdir}/winboat/

ln -sf %{_libexecdir}/winboat/winboat %{buildroot}%{_bindir}/winboat

cat <<EOF > %{buildroot}%{_datadir}/applications/winboat.desktop
[Desktop Entry]
Name=Winboat
Exec=%{_bindir}/winboat
Icon=winboat
Type=Application
Categories=Utility;Game;
EOF

cat <<EOF > %{buildroot}%{_prefix}/lib/tmpfiles.d/sirius-os-winboat.conf
L+ /opt/winboat - - - - %{_libexecdir}/winboat
EOF

%files
%attr(4755, root, root) %{_libexecdir}/winboat/chrome-sandbox
%{_libexecdir}/winboat/
%{_bindir}/winboat
%{_datadir}/applications/winboat.desktop
%{_prefix}/lib/tmpfiles.d/sirius-os-winboat.conf

