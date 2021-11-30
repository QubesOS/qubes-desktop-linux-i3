%if 0%{?qubes_builder}
%define _sourcedir %(pwd)/i3-settings-qubes
%endif

Name:       i3-settings-qubes
Version:    1.7
Release:    1%{?dist}
Summary:    Default i3 settings for Qubes

Group:      User Interface/Desktops
License:    GPLv2+
URL:        http://www.qubes-os.org/
Source0:    i3.config
Source1:    i3.config.keycodes
Source2:    qubes-i3-sensible-terminal
Source3:    qubes-i3-xdg-autostart
Source4:    qubes-i3status

Requires:   i3
Requires:   xautolock
Requires:   i3lock
Requires:   perl-Data-Dumper 
Requires:   perl-File-Temp 
Requires:   perl-Getopt-Long 
Requires:   perl-open


%description
%{summary}

%prep

%build


%install
install -m 644 -D %{SOURCE0} %{buildroot}%{_sysconfdir}/i3/config.qubes
install -m 644 -D %{SOURCE1} %{buildroot}%{_sysconfdir}/i3/config.keycodes.qubes
install -m 755 -D %{SOURCE2} %{buildroot}%{_bindir}/qubes-i3-sensible-terminal
install -m 755 -D %{SOURCE3} %{buildroot}%{_bindir}/qubes-i3-xdg-autostart
install -m 755 -D %{SOURCE4} %{buildroot}%{_bindir}/qubes-i3status

%define settings_replace() \
origfile="`echo %{1} | sed 's/\.qubes$//'`"\
backupfile="`echo %{1} | sed s/\.qubes$/\.i3/`"\
if [ -r "$origfile" -a ! -r "$backupfile" ]; then\
    mv -f "$origfile" "$backupfile"\
fi\
cp -f "%{1}" "$origfile"\
%{nil}

%triggerin -- i3-settings-qubes
%settings_replace %{_sysconfdir}/i3/config.qubes
%settings_replace %{_sysconfdir}/i3/config.keycodes.qubes

%postun
REPLACEFILE="${REPLACEFILE} %{_sysconfdir}/i3/config.qubes"
REPLACEFILE="${REPLACEFILE} %{_sysconfdir}/i3/config.keycodes.qubes"
if [ $1 -lt 1 ]; then
    for file in ${REPLACEFILE}; do
        origfile="`echo $file | sed 's/\.qubes$//'`"
        backupfile="`echo $file | sed 's/\.qubes$/\.i3/'`"
        mv -f "$backupfile" "$origfile"
    done
fi

%files
%{_sysconfdir}/i3/config.qubes
%{_sysconfdir}/i3/config.keycodes.qubes
%{_bindir}/qubes-i3-sensible-terminal
%{_bindir}/qubes-i3-xdg-autostart
%{_bindir}/qubes-i3status

%changelog
* Tue Nov 30 2021 o- <o@o1o.ch> - 1.7
- Rebased on https://src.fedoraproject.org/rpms/i3/tree/a814cba055571794e3cfeea2fea5ef1635942545
