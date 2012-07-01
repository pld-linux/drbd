# TODO:
#  - trigger to update drbd-8.2 config
#  - warning: Installed (but unpackaged) file(s) found:
#     /etc/xen/scripts/block-drbd
#  - add some provides/requires to keep in sync with kernel releases
#    Linux 3.0.8 got drbd module version 8.3.11
#

Summary:	drbd is a block device designed to build high availibility clusters
Summary(pl.UTF-8):	drbd jest urządzeniem blokowym dla klastrów o wysokiej niezawodności
Name:		drbd
Version:	8.4.1
Release:	1
License:	GPL v2+
Group:		Base/Kernel
Source0:	http://oss.linbit.com/drbd/8.4/%{name}-%{version}.tar.gz
# Source0-md5:	3af0cc49ee0b5005ea108c5ba92aa755
URL:		http://www.drbd.org/
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	rpmbuild(macros) >= 1.379
BuildRequires:	udev-core
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
Obsoletes:	drbdsetup8
Conflicts:	drbdsetup24

%description -n drbdsetup
Setup tool and init scripts for DRBD.

%description -n drbdsetup -l pl.UTF-8
Narzędzie konfiguracyjne i skrypty startowe dla DRBD.

%package -n resource-agents-drbd
Summary:	DRBD resource agents for a cluster setup
Group:		Daemons
Requires:	resource-agents

%description -n resource-agents-drbd
DRBD resource agents for a cluster setup.

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
%configure \
	--with-initdir=/etc/rc.d/init.d

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

%{__make} install \
	DRBD_ENABLE_UDEV=1 \
	DESTDIR=$RPM_BUILD_ROOT

# let's keep legacy utils in /sbin
mv $RPM_BUILD_ROOT/lib/drbd/drbd{adm,setup}-83 $RPM_BUILD_ROOT/sbin

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
%attr(4754,root,haclient) /sbin/drbdsetup
%attr(4754,root,haclient) /sbin/drbdmeta
%attr(755,root,root) /sbin/drbdadm-83
%attr(755,root,root) /sbin/drbdsetup-83
%attr(754,root,root) /etc/rc.d/init.d/drbd
%dir %{_sysconfdir}/drbd.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/drbd.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/drbd.d/global_common.conf
%{_mandir}/man[58]/*
%dir /usr/lib/drbd
%attr(755,root,root) /usr/lib/drbd/*
%attr(755,root,root) %{_sbindir}/drbd-overview
%attr(750,root,root) %dir /var/lib/drbd

%files -n resource-agents-drbd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sysconfdir}/ha.d/resource.d/drbddisk
%attr(755,root,root) %{_sysconfdir}/ha.d/resource.d/drbdupper
%dir /usr/lib/ocf/resource.d/linbit
%attr(755,root,root) /usr/lib/ocf/resource.d/linbit/*

%files -n bash-completion-drbd
%defattr(644,root,root,755)
/etc/bash_completion.d/drbdadm

%files -n drbd-udev
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/udev/rules.d/65-drbd.rules
