#
# TODO:
#  - trigger to update drbd-8.2 config
#  - warning: Installed (but unpackaged) file(s) found:
#     /etc/xen/scripts/block-drbd
#     /usr/lib/ocf/resource.d/linbit/drbd
#

Summary:	drbd is a block device designed to build high availibility clusters
Summary(pl.UTF-8):	drbd jest urządzeniem blokowym dla klastrów o wysokiej niezawodności
Name:		drbd
Version:	8.3.9
Release:	3
License:	GPL
Group:		Base/Kernel
Source0:	http://oss.linbit.com/drbd/8.3/%{name}-%{version}.tar.gz
# Source0-md5:	fda3bc1f3f42f3066df33dcb0aa14f2a
URL:		http://www.drbd.org/
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	rpmbuild(macros) >= 1.379
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
drbd is a block device which is designed to build high availability
clusters. This is done by mirroring a whole block device via (a
dedicated) network. You could see it as a network RAID1.

%description -l pl.UTF-8
drbd jest urządzeniem blokowym zaprojektowanym dla klastrów o wysokiej
niezawodności. drbd działa jako mirroring całego urządzenia blokowego
przez (dedykowaną) sieć. Może być widoczny jako sieciowy RAID1.

%description -l pt_BR.UTF-8
O DRBD é um dispositivo de bloco que é projetado para construir
clusters de Alta Disponibilidade. Isto é feito espelhando um
dispositivo de bloco inteiro via rede (dedicada ou não). Pode ser
visto como um RAID 1 via rede. Este pacote contém utilitários para
gerenciar dispositivos DRBD.

%package -n drbdsetup
Summary:	Setup tool and scripts for DRBD
Summary(pl.UTF-8):	Narzędzie konfiguracyjne i skrypty dla DRBD
Summary(pt_BR.UTF-8):	Utilitários para gerenciar dispositivos DRBD
Group:		Applications/System
Requires(post,preun):	/sbin/chkconfig
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(postun):	/usr/sbin/groupdel
Requires:	rc-scripts
Provides:	group(haclient)
Conflicts:	drbdsetup24
Obsoletes:	drbdsetup8

%description -n drbdsetup
Setup tool and init scripts for DRBD.

%description -n drbdsetup -l pl.UTF-8
Narzędzie konfiguracyjne i skrypty startowe dla DRBD.

%package -n bash-completion-drbd
Summary:	bash-completion for drbd
Summary(pl.UTF-8):	Bashowe uzupełnianie poleceń dla drbd
Group:		Applications/Shells
Requires:	bash-completion

%description -n bash-completion-drbd
This package provides bash-completion for drbd.

%description -n bash-completion-drbd -l pl.UTF-8
Ten pakiet dostarcza bashowe uzupełnianie poleceń dla drbd.

%package -n drbd-udev
Summary:	udev rules for drbd kernel module
Summary(pl.UTF-8):	Reguły udev dla modułów jądra Linuksa dla drbd
Group:		Base/Kernel
Requires:	udev-core

%description -n drbd-udev
udev rules for drbd kernel module.

%description -n drbd-udev -l pl.UTF-8
Reguły udev dla modułu jądra Linuksa dla drbd.

%prep
%setup -q

%build
%configure
%{__make} tools \
	KVER=dummy \
	CC="%{__cc}" \
	OPTCFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/sbin,%{_mandir}/man{5,8},%{_sysconfdir}} \
	$RPM_BUILD_ROOT{/etc/rc.d/init.d,/etc/ha.d/resource.d} \
	$RPM_BUILD_ROOT/var/lib/drbd

%{__make} install -C scripts \
	DRBD_ENABLE_UDEV=1 \
	DESTDIR=$RPM_BUILD_ROOT

install scripts/drbd $RPM_BUILD_ROOT/etc/rc.d/init.d
rm -rf $RPM_BUILD_ROOT/etc/init.d
install user/{drbdadm,drbdmeta,drbdsetup} $RPM_BUILD_ROOT/sbin

install documentation/*.5 $RPM_BUILD_ROOT%{_mandir}/man5
install documentation/*.8 $RPM_BUILD_ROOT%{_mandir}/man8

%clean
rm -rf $RPM_BUILD_ROOT

%pre -n drbdsetup
%groupadd -g 60 haclient

%post -n drbdsetup
/sbin/chkconfig --add drbd
%service drbd restart

%preun -n drbdsetup
if [ "$1" = "0" ]; then
	%service drbd stop
	/sbin/chkconfig --del drbd
fi

%postun -n drbdsetup
if [ "$1" = "0" ]; then
	%groupremove haclient
fi

%files -n drbdsetup
%defattr(644,root,root,755)
%attr(755,root,root) /sbin/drbdadm
%attr(2754,root,haclient) /sbin/drbdsetup
%attr(2754,root,haclient) /sbin/drbdmeta
%attr(754,root,root) /etc/rc.d/init.d/drbd
%dir %{_sysconfdir}/ha.d
%dir %{_sysconfdir}/ha.d/resource.d
%attr(755,root,root) %{_sysconfdir}/ha.d/resource.d/drbddisk
%attr(755,root,root) %{_sysconfdir}/ha.d/resource.d/drbdupper
%dir %{_sysconfdir}/drbd.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/drbd.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/drbd.d/global_common.conf
%{_mandir}/man[58]/*
%dir /usr/lib/drbd
%attr(755,root,root) /usr/lib/drbd/*
%attr(755,root,root) %{_sbindir}/drbd-overview
%attr(750,root,root) %dir /var/lib/drbd

%files -n bash-completion-drbd
%defattr(644,root,root,755)
/etc/bash_completion.d/drbdadm

%files -n drbd-udev
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/udev/rules.d/65-drbd.rules
