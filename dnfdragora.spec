Summary:	DNF package-manager based on libYui abstraction
Name:		dnfdragora
Version:	2.1.1
Release:	1
License:	GPL v3+
Source0:	https://github.com/manatools/dnfdragora/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	addda76c7ff2695a6b5f6138bf6a3fe3
Patch0:		install.patch
URL:		https://github.com/manatools/dnfdragora
BuildRequires:	appstream-glib
BuildRequires:	cmake >= 3.4.0
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	pkgconfig
BuildRequires:	python3-devel >= 3.4.0
Requires:	comps-extras
Requires:	dnf >= 1.0.9
Requires:	filesystem
Requires:	hicolor-icon-theme
Requires:	libyui-mga-ncurses
Requires:	python3-PyYAML
Requires:	python3-dnfdaemon >= 0.3.20
Requires:	python3-manatools >= 0.0.3
Requires:	python3-yui >= 1.1.1-10
Recommends:	libyui-mga-qt
Recommends:	libyui-mga-gtk
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
dnfdragora is a DNF frontend, based on rpmdragora from Mageia
(originally rpmdrake) Perl code.

dnfdragora is written in Python 3 and uses libYui, the widget
abstraction library written by SUSE, so that it can be run using Qt 5,
GTK+ 3, or ncurses interfaces.

%package updater
Summary:	Update notifier applet for dnfdragora
Requires:	%{name} = %{version}-%{release}
Requires:	libnotify
Requires:	python3-cairosvg
Requires:	python3-pillow
Requires:	python3-pystray >= 0.16
Requires:	python3-pyxdg

%description updater
dnfdragora is a DNF frontend, based on rpmdragora from Mageia
(originally rpmdrake) Perl code.

dnfdragora is written in Python 3 and uses libYui, the widget
abstraction library written by SUSE, so that it can be run using Qt 5,
GTK+ 3, or ncurses interfaces.

This package provides the update notifier applet for dnfdragora.

%prep
%setup -q
%patch0 -p1

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+python3(\s|$),#!%{__python3}\1,' \
      bin/dnfdragora \
      bin/dnfdragora-updater

mkdir -p build

%build
cd build
%cmake ../ \
	-DPYTHON_INSTALL_DIR:PATH=%{py3_sitescriptdir} \
	-DCHECK_RUNTIME_DEPENDENCIES:BOOL=OFF \
	-DENABLE_COMPS:BOOL=ON

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%py3_ocomp $RPM_BUILD_ROOT%{py3_sitescriptdir}
%py3_comp $RPM_BUILD_ROOT%{py3_sitescriptdir}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README.md %{name}.yaml*.example
%doc AUTHORS LICENSE
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.yaml
%attr(755,root,root) %{_bindir}/%{name}
%dir %{py3_sitescriptdir}/%{name}
%{py3_sitescriptdir}/%{name}/*
%exclude %{py3_sitescriptdir}/%{name}/updater.py
%exclude %{py3_sitescriptdir}/%{name}/__pycache__/updater.cpython*.py?
%{_datadir}/%{name}
%{_datadir}/appdata/*%{name}.appdata.xml
%{_desktopdir}/*%{name}.desktop
%{_desktopdir}/*%{name}-localinstall.desktop
%{_iconsdir}/hicolor/*/apps/%{name}*
%{_mandir}/man5/%{name}*.5*
%{_mandir}/man8/%{name}*.8*

%files updater
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}-updater
%{py3_sitescriptdir}/%{name}/updater.py
%{py3_sitescriptdir}/%{name}/__pycache__/updater.cpython*.py?
%{_desktopdir}/*%{name}-updater.desktop
%{_sysconfdir}/xdg/autostart/*%{name}*.desktop
