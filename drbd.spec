Summary:	drbd
Summary(pl):	drbd
Name:		drbd
Version:	0.5.8
Release:	1
License:	GPL
Group:		Utilities
######		Unknown group!
Group(pl):	Narzêdzia
Source0:	%{name}-%{version}.tar.gz
URL:		http://complang.tuwien.ac.at/reisner/drbd/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_kernelversion	2.2.19

%description
heartbeat is a basic heartbeat subsystem for Linux-HA. It will run
scripts at initialization, and when machines go up or down. This
version will also perform IP address takeover using gratuitous ARPs.
It works correctly for a 2-node configuration, and is extensible to
larger configurations.

It implements the following kinds of heartbeats:
 - Bidirectional Serial Rings ("raw" serial ports)
 - UDP/IP broadcast (ethernet, etc)
 - Bidirectional Serial PPP/UDP Rings (using PPP)

%description -l pl
heartbeat jest podstawowym podsystemem dla systemów o podwy¿szonej
dostêpno¶ci budowanych w oparciu o Linuxa. Zajmuje siê uruchamianiem
skryptów podczas startu i zamykania systemu. Ta wersja pakietu pozwala
na przejmowanie adresów IP. Oprogramowanie dzia³a poprawnie dla
konfiguracji sk³adaj±cej siê z 2 hostów, mo¿na je równie¿ stosowaæ do
bardziej skomplikowanych konfiguracji.

%prep
%setup -q -n %{name}

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir}

#%{__make} install PREFIX=$RPM_BUILD_ROOT/
#dir drbd
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernelversion}/block/
install drbd/drbd.o $RPM_BUILD_ROOT/lib/modules/%{_kernelversion}/block/
#dir user
install user/drbdsetup $RPM_BUILD_ROOT%{_sbindir}/
#dir documentation
install -d  $RPM_BUILD_ROOT/%{_defaultdocdir}/%{name}
cd documentation
install drbd.conf.5  drbd.conf.sgml  drbdsetup.8  drbdsetup.sgml  manpage.links  manpage.refs $RPM_BUILD_ROOT/%{_defaultdocdir}/%{name}

%post
/sbin/depmod

%preun
/sbin/depmod

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc %{_defaultdocdir}/%{name}
%attr(755,root,root) %{_sbindir}/drbdsetup
/lib/modules/%{_kernelversion}/block/drbd.o
%{_mandir}/man8/*
%{_mandir}/man5/*
