%define		_kernel_ver	%(grep UTS_RELEASE %{_kernelsrcdir}/include/linux/version.h 2>/dev/null | cut -d'"' -f2)
%define		_kernel24	%(echo %{_kernel_ver} | grep -q '2\.[012]\.' ; echo $?)

%define		rel		1

Summary:	drbd is a block device designed to build high availibility clusters
Summary(pl):	drbd jest urz±dzeniem blokowym dla klastrów o wysokiej niezawodno¶ci
Name:		drbd
Version:	0.5.8
Release:	%{rel}
License:	GPL
Group:		Base/Kernel
Group(de):	Grundsätzlich/Kern
Group(pl):	Podstawowe/J±dro
Source0:	http://www.complang.tuwien.ac.at/reisner/drbd/download/%{name}-%{version}.tar.gz
Patch0:		%{name}-kernel24.patch
URL:		http://www.complang.tuwien.ac.at/reisner/drbd/
Conflicts:	kernel < %{_kernel_ver}, kernel > %{_kernel_ver}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
drbd is a block device which is designed to build high availability
clusters. This is done by mirroring a whole block device via (a
dedicated) network. You could see it as a network RAID1.

%description -l pl
drbd jest urz±dzeniem blokowym zaprojektowanym dla klastrów o wysokiej
niezawodno¶ci. drbd dzia³a jako mirroring ca³ego urz±dzenia blokowego
przez (dedykowan±) sieæ. Mo¿e byæ widoczny jako sieciowy RAID1.

%package -n drbdsetup
Summary:	Setup tool and scripts for DRBD
Summary(es):	Utilities to manage DRBD devices
Summary(pl):	Narzêdzie konfiguracyjne i skrypty dla DRBD
Summary(pt_BR):	Utilitários para gerenciar dispositivos DRBD
Group:		Applications/System
Group(de):	Applikationen/System
Group(pl):	Aplikacje/System
Prereq:		rc-scripts
Requires:	%{name} = %{version}

%description -n drbdsetup
Setup tool and init scripts for DRBD.

%description -l pl -n drbdsetup
Narzêdzie konfiguracyjne i skrypty startowe dla DRBD.

%description -l pt_BR
O DRBD é um dispositivo de bloco que é projetado para construir
clusters de Alta Disponibilidade. Isto é feito espelhando um
dispositivo de bloco inteiro via rede (dedicada ou não). Pode ser
visto como um RAID 1 via rede. Este pacote contém utilitários para
gerenciar dispositivos DRBD.

%description -l es
DRBD is a block device which is designed to build High Availability
clusters. This is done by mirroring a whole block device via (maybe
dedicated) network. You could see it as a network RAID 1. This package
contains the utils to manage DRBD devices.

%package -n kernel-block-drbd
Summary:	kernel module with drbd - a block device designed to build high availibility clusters
Summary(pl):	Modu³ kernela do drbd - urz±dzenia blokowego dla klastrów o wysokiej niezawodno¶ci
Release:	%{rel}@%{_kernel_ver}
Group:		Base/Kernel
Group(de):	Grundsätzlich/Kern
Group(pl):	Podstawowe/J±dro
Prereq:		/sbin/depmod
Requires:	drbdsetup
Conflicts:	kernel-smp-block-drbd
Conflicts:	kernel < %{_kernel_ver}
Conflicts:	kernel > %{_kernel_ver}

%description -n kernel-block-drbd
drbd is a block device which is designed to build high availability
clusters. This is done by mirroring a whole block device via (a
dedicated) network. You could see it as a network RAID1.

%description -l pl -n kernel-block-drbd
drbd jest urz±dzeniem blokowym zaprojektowanym dla klastrów o wysokiej
niezawodno¶ci. drbd dzia³a jako mirroring ca³ego urz±dzenia blokowego
przez (dedykowan±) sieæ. Mo¿e byæ widoczny jako sieciowy RAID1.

%package -n kernel-smp-block-drbd
Summary:	SMP kernel module with drbd - a block device designed to build high availibility clusters
Summary(pl):	Modu³ kernela SMP do drbd - urz±dzenia blokowego dla klastrów o wysokiej niezawodno¶ci
Release:	%{rel}@%{_kernel_ver}
Group:		Base/Kernel
Group(de):	Grundsätzlich/Kern
Group(pl):	Podstawowe/J±dro
Prereq:		/sbin/depmod
Requires:	drbdsetup
Conflicts:	kernel-block-drbd
Conflicts:	kernel < %{_kernel_ver}
Conflicts:	kernel > %{_kernel_ver}

%description -n kernel-smp-block-drbd
drbd is a block device which is designed to build high availability
clusters. This is done by mirroring a whole block device via (a
dedicated) network. You could see it as a network RAID1.

%description -l pl -n kernel-smp-block-drbd
drbd jest urz±dzeniem blokowym zaprojektowanym dla klastrów o wysokiej
niezawodno¶ci. drbd dzia³a jako mirroring ca³ego urz±dzenia blokowego
przez (dedykowan±) sieæ. Mo¿e byæ widoczny jako sieciowy RAID1.

%prep
%setup -q -n %{name}
%if %{_kernel24}
%patch -p1
%endif

%build
%if 0
%{__make} \
%ifarch %{ix86}
	KAF_i386="%{rpmcflags} -malign-loops=2 -malign-jumps=2 -malign-functions=2 -fomit-frame-pointer" \
%else
%ifarch %{alpha}
	KAF_alpha="%{rpmcfalgs} -ffixed8 -mno-fp-regs" \
%endif
%endif
	SMPFLAG="-D__SMP__" \
	KERNVER="%{_kernel_ver}" \
	INCLUDE="-I%{_kernelsrcdir}/include" \
	DEBUGFLAGS="%{rpmcflags} %{?debug:-DDBG}"

mv drbd/drbd.o drbd-smp.o
%endif

%{__make} \
%ifarch %{ix86}
	KAF_i386="%{rpmcflags} -malign-loops=2 -malign-jumps=2 -malign-functions=2 -fomit-frame-pointer" \
%else
%ifarch %{alpha}
	KAF_alpha="%{rpmcfalgs} -ffixed8 -mno-fp-regs" \
%endif
%endif
	SMPFLAG="" \
	KERNVER="%{_kernel_ver}" \
	INCLUDE="-I%{_kernelsrcdir}/include" \
	DEBUGFLAGS="%{rpmcflags} %{?debug:-DDBG}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man{5,8},%{_sysconfdir}} \
	$RPM_BUILD_ROOT{/etc/rc.d/init.d,/etc/ha.d/resource.d}

%if %{_kernel24}
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc
install drbd/drbd.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/drbd.o
%if 0
install drbd-smp.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/drbd.o
%endif
%else
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/block
install drbd/drbd.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/block
%if 0
install drbd-smp.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/block/drbd.o
%endif
%endif

install user/drbdsetup $RPM_BUILD_ROOT%{_sbindir}
install scripts/drbd.conf $RPM_BUILD_ROOT%{_sysconfdir}
install scripts/drbd $RPM_BUILD_ROOT/etc/rc.d/init.d
ln -sf /etc/rc.d/init.d/drbd $RPM_BUILD_ROOT/etc/ha.d/resource.d/datadisk

install documentation/drbd.conf.5 $RPM_BUILD_ROOT%{_mandir}/man5
install documentation/drbdsetup.8 $RPM_BUILD_ROOT%{_mandir}/man8

gzip -9nf ChangeLog README TODO

%clean
rm -rf $RPM_BUILD_ROOT

%post   -n kernel-block-drbd
/sbin/depmod -a

%postun -n kernel-block-drbd
/sbin/depmod -a

%post   -n kernel-smp-block-drbd
/sbin/depmod -a

%postun -n kernel-smp-block-drbd
/sbin/depmod -a

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

%files -n drbdsetup
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/drbdsetup
%attr(755,root,root) /etc/rc.d/init.d/drbd
%attr(755,root,root) %{_sysconfdir}/ha.d/resource.d/datadisk
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/drbd.conf
%{_mandir}/man[58]/*

%files -n kernel-block-drbd
%defattr(644,root,root,755)
%doc *.gz
%if %{_kernel24}
/lib/modules/%{_kernel_ver}/misc/drbd.o
%else
/lib/modules/%{_kernel_ver}/block/drbd.o
%endif

%if 0
%files -n kernel-smp-block-drbd
%defattr(644,root,root,755)
%doc *.gz
%if %{_kernel24}
/lib/modules/%{_kernel_ver}smp/misc/drbd.o
%else
/lib/modules/%{_kernel_ver}smp/block/drbd.o
%endif
%endif
