#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	smp		# don't build SMP module
%bcond_without	userspace	# don't build userspace module
%bcond_with	verbose		# verbose build (V=1)
#
Summary:	drbd is a block device designed to build high availibility clusters
Summary(pl):	drbd jest urz±dzeniem blokowym dla klastrów o wysokiej niezawodno¶ci
Name:		drbd
Version:	0.7.13
%define	rel	1
Release:	%{rel}
License:	GPL
Group:		Base/Kernel
Source0:	http://oss.linbit.com/drbd/0.7/%{name}-%{version}.tar.gz
# Source0-md5:	bd25ec57d91b39705217f196fc7c8561
URL:		http://www.drbd.org/
BuildRequires:	bison
BuildRequires:	flex
%{?with_dist_kernel:BuildRequires:	kernel-module-build}
BuildRequires:	rpmbuild(macros) >= 1.118
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
drbd is a block device which is designed to build high availability
clusters. This is done by mirroring a whole block device via (a
dedicated) network. You could see it as a network RAID1.

%description -l pl
drbd jest urz±dzeniem blokowym zaprojektowanym dla klastrów o wysokiej
niezawodno¶ci. drbd dzia³a jako mirroring ca³ego urz±dzenia blokowego
przez (dedykowan±) sieæ. Mo¿e byæ widoczny jako sieciowy RAID1.

%description -l pt_BR
O DRBD é um dispositivo de bloco que é projetado para construir
clusters de Alta Disponibilidade. Isto é feito espelhando um
dispositivo de bloco inteiro via rede (dedicada ou não). Pode ser
visto como um RAID 1 via rede. Este pacote contém utilitários para
gerenciar dispositivos DRBD.

%package -n drbdsetup
Summary:	Setup tool and scripts for DRBD
Summary(pl):	Narzêdzie konfiguracyjne i skrypty dla DRBD
Summary(pt_BR):	Utilitários para gerenciar dispositivos DRBD
Group:		Applications/System
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Conflicts:	drbdsetup24

%description -n drbdsetup
Setup tool and init scripts for DRBD.

%description -n drbdsetup -l pl
Narzêdzie konfiguracyjne i skrypty startowe dla DRBD.

%package -n kernel-block-drbd
Summary:	Kernel module with drbd - a block device designed to build high availibility clusters
Summary(pl):	Modu³ j±dra do drbd - urz±dzenia blokowego dla klastrów o wysokiej niezawodno¶ci
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Requires:	drbdsetup

%description -n kernel-block-drbd
drbd is a block device which is designed to build high availability
clusters. This is done by mirroring a whole block device via (a
dedicated) network. You could see it as a network RAID1.

%description -n kernel-block-drbd -l pl
drbd jest urz±dzeniem blokowym zaprojektowanym dla klastrów o wysokiej
niezawodno¶ci. drbd dzia³a jako mirroring ca³ego urz±dzenia blokowego
przez (dedykowan±) sieæ. Mo¿e byæ widoczny jako sieciowy RAID1.

%package -n kernel-smp-block-drbd
Summary:	SMP kernel module with drbd - a block device designed to build high availibility clusters
Summary(pl):	Wersja SMP Modu³u j±dra do drbd - urz±dzenia blokowego dla klastrów o wysokiej niezawodno¶ci
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
Requires:	drbdsetup

%description -n kernel-smp-block-drbd
drbd is a block device which is designed to build high availability
clusters. This is done by mirroring a whole block device via (a
dedicated) network. You could see it as a network RAID1.

%description -n kernel-smp-block-drbd -l pl
drbd jest urz±dzeniem blokowym zaprojektowanym dla klastrów o wysokiej
niezawodno¶ci. drbd dzia³a jako mirroring ca³ego urz±dzenia blokowego
przez (dedykowan±) sieæ. Mo¿e byæ widoczny jako sieciowy RAID1.

%prep
%setup -q

%build
%if %{with userspace}
%{__make} tools \
	CC="%{__cc}"
%endif

%if %{with kernel}
cd drbd
sed -i -e 's#$(CONFIG_BLK_DEV_DRBD)#m#g' Makefile-2.6
ln -sf Makefile-2.6 Makefile
# kernel module(s)
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	rm -rf include
	install -d include/{linux,config}
	ln -sf %{_kernelsrcdir}/config-$cfg .config
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h include/linux/autoconf.h
	ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} include/asm
	ln -sf %{_kernelsrcdir}/Module.symvers-$cfg Module.symvers
	touch include/config/MARKER
	%{__make} -C %{_kernelsrcdir} clean \
		RCS_FIND_IGNORE="-name '*.ko' -o" \
		M=$PWD O=$PWD \
		%{?with_verbose:V=1}
	%{__make} -C %{_kernelsrcdir} modules \
		CC="%{__cc}" CPP="%{__cpp}" \
		M=$PWD O=$PWD \
		%{?with_verbose:V=1}
	mv drbd{,-$cfg}.ko
done
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/sbin,%{_mandir}/man{5,8},%{_sysconfdir}} \
	$RPM_BUILD_ROOT{/etc/rc.d/init.d,/etc/ha.d/resource.d}

%if %{with kernel}
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc
install drbd/drbd-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
		$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/drbd.ko
%if %{with smp} && %{with dist_kernel}
install drbd/drbd-smp.ko \
		$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/drbd.ko
%endif
%endif

%if %{with userspace}
install user/{drbdadm,drbdsetup} $RPM_BUILD_ROOT/sbin
install scripts/drbd.conf $RPM_BUILD_ROOT%{_sysconfdir}
install scripts/drbd $RPM_BUILD_ROOT/etc/rc.d/init.d

ln -sf /etc/rc.d/init.d/drbd $RPM_BUILD_ROOT/etc/ha.d/resource.d/datadisk

install documentation/*.5 $RPM_BUILD_ROOT%{_mandir}/man5
install documentation/*.8 $RPM_BUILD_ROOT%{_mandir}/man8
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post -n kernel-block-drbd
%depmod %{_kernel_ver}

%postun -n kernel-block-drbd
%depmod %{_kernel_ver}

%post -n kernel-smp-block-drbd
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-block-drbd
%depmod %{_kernel_ver}smp

%post -n drbdsetup
/sbin/chkconfig --add drbd
if [ -f /var/lock/subsys/drbd ]; then
	/etc/rc.d/init.d/drbd restart >&2
else
	echo "Run \"/etc/rc.d/init.d/drbd start\" to start drbd service." >&2
fi

%preun -n drbdsetup
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/drbd ]; then
		/etc/rc.d/init.d/drbd stop
	fi
	/sbin/chkconfig --del drbd
fi

%if %{with userspace}
%files -n drbdsetup
%defattr(644,root,root,755)
%doc documentation/*.txt
%attr(755,root,root) /sbin/*
%attr(754,root,root) /etc/rc.d/init.d/drbd
%attr(755,root,root) %{_sysconfdir}/ha.d/resource.d/datadisk
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/drbd.conf
%{_mandir}/man[58]/*
%endif

%if %{with kernel}
%files -n kernel-block-drbd
%defattr(644,root,root,755)
%doc ChangeLog README
/lib/modules/%{_kernel_ver}/misc/*

%if %{with smp} && %{with dist_kernel}
%files -n kernel-smp-block-drbd
%defattr(644,root,root,755)
%doc ChangeLog README
/lib/modules/%{_kernel_ver}smp/misc/*
%endif
%endif
