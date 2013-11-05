Summary:	MATE media programs
Name:		mate-media
Version:	1.6.0
Release:	1
License:	GPL v2+/LGPL v2+
Group:		X11/Applications/Multimedia
Source0:	http://pub.mate-desktop.org/releases/1.6/%{name}-%{version}.tar.xz
# Source0-md5:	96a2832f157a5879f62d27fbae89da07
URL:		http://www.mate.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	intltool
BuildRequires:	libcanberra-devel
BuildRequires:	libtool
BuildRequires:	libunique-devel
BuildRequires:	libxml2-devel
BuildRequires:	mate-doc-utils
BuildRequires:	pulseaudio-devel
Requires(post,postun):	rarian
Requires:	libcanberra-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MATE media programs. MATE is the GNU Network Object Model
Environment. That's a fancy name but really MATE is a nice GUI
desktop environment. It makes using your computer easy, powerful, and
easy to configure.

%package volume-control
Summary:	Volume controler
Group:		X11/Applications/Multimedia
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	pulseaudio

%description volume-control
Volume control.

%package volume-control-applet
Summary:	Volume control applet
Group:		X11/Applications/Multimedia
Requires:	%{name}-volume-control = %{epoch}:%{version}-%{release}

%description volume-control-applet
Volume control applet.

%prep
%setup -q

# kill mate common deps
%{__sed} -i -e '/MATE_COMPILE_WARNINGS.*/d'	\
    -i -e '/MATE_MAINTAINER_MODE_DEFINES/d'	\
    -i -e '/MATE_COMMON_INIT/d'			\
    -i -e '/MATE_CXX_WARNINGS/d'		\
    -i -e '/MATE_DEBUG_CHECK/d' configure.ac

%build
%{__intltoolize}
%{__libtoolize}
mate-doc-prepare --copy
%{__aclocal} -I m4
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--disable-schemas-compile	\
	--disable-scrollkeeper		\
	--disable-static		\
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

gtk-update-icon-cache -ft $RPM_BUILD_ROOT%{_datadir}/mate-media/icons/mate

%{__rm} -rf $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,en@shaw,ha,ig,la}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%scrollkeeper_update_post

%postun
%scrollkeeper_update_postun

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README

%dir %{_datadir}/mate-media
%dir %{_datadir}/mate-media/icons
%dir %{_datadir}/mate-media/sounds
%dir %{_datadir}/sounds/mate
%dir %{_datadir}/sounds/mate/default
%dir %{_datadir}/sounds/mate/default/alerts

%{_datadir}/mate-media/icons
%{_datadir}/mate-media/sounds/mate-sounds-default.xml
%{_datadir}/sounds/mate/default/alerts/*.ogg

%files volume-control
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mate-volume-control
%{_desktopdir}/mate-volume-control.desktop

%files volume-control-applet
%defattr(644,root,root,755)
%{_sysconfdir}/xdg/autostart/mate-volume-control-applet.desktop
%attr(755,root,root) %{_bindir}/mate-volume-control-applet

