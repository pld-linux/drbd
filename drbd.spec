%define		_kernel_ver	%(grep UTS_RELEASE %{_kernelsrcdir}/include/linux/version.h 2>/dev/null | cut -d'"' -f2)
%define		_kernel24	%(echo %{_kernel_ver} | grep -q '2\.[012]\.' ; echo $?)
%define		smpstr		%{?_with_smp:smp}%{!?_with_smp:up}
%define		smp		%{?_with_smp:1}%{!?_with_smp:0}

%define		rel		1

Summary:	drbd is a block device designed to build high availibility clusters
Summary(pl):	drbd jest urz±dzeniem blokowym dla klastrów o wysokiej niezawodno¶ci
Name:		drbd
Version:	0.5.8
Release:	%{rel}@%{_kernel_ver}%{smpstr}
License:	GPL
Group:		Base/Kernel
Group(de):	Grundsätzlich/Kern
Group(pl):	Podstawowe/J±dro
Source0:	http://www.complang.tuwien.ac.at/reisner/drbd/download/%{name}-%{version}.tar.gz
Patch0:		%{name}-kernel24.patch
URL:		http://www.complang.tuwien.ac.at/reisner/drbd/
Prereq:		/sbin/depmod
Conflicts:	kernel < %{_kernel_ver}, kernel > %{_kernel_ver}
Conflicts:	kernel-%{?_with_smp:up}%{!?_with_smp:smp}
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
Summary(pl):	Narzêdzie konfiguracyjne i skrypty dla DRBD
Release:	%{rel}
Group:		Applications/System
Group(de):	Applikationen/System
Group(pl):	Aplikacje/System
Prereq:		chkconfig
Requires:	%{name} = %{version}

%description -n drbdsetup
Setup tool and init scripts for DRBD.

%description -n drbdsetup -l pl
Narzêdzie konfiguracyjne i skrypty startowe dla DRBD.

%prep
%setup -q -n %{name}
%if %{_kernel24}
%patch -p1
%endif

%build
%if %{smp}
SMP="-D__SMP__"
%endif
%{__make} \
%ifarch %{ix86}
	KAF_i386="%{rpmcflags} -malign-loops=2 -malign-jumps=2 -malign-functions=2 -fomit-frame-pointer" \
%else
%ifarch %{alpha}
	KAF_alpha="%{rpmcfalgs} -ffixed8 -mno-fp-regs" \
%endif
%endif
	SMPFLAG="$SMP" \
	KERNVER="%{_kernel_ver}" \
	INCLUDE="-I%{_kernelsrcdir}/include" \
	DEBUGFLAGS="%{rpmcflags} %{?debug:-DDBG}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man{5,8},%{_sysconfdir}} \
	$RPM_BUILD_ROOT{/etc/rc.d/init.d,/etc/ha.d/resource.d}

%if %{_kernel24}
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
install drbd/drbd.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
%else
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/block
install drbd/drbd.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/block
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

%post
/sbin/depmod -a

%postun
/sbin/depmod -a

%post -n drbdsetup
chkconfig --add drbd

%preun -n drbdsetup
chkconfig --del drbd

%files
%defattr(644,root,root,755)
%doc *.gz
%if %{_kernel24}
/lib/modules/%{_kernel_ver}/misc/drbd.o
%else
/lib/modules/%{_kernel_ver}/block/drbd.o
%endif

%files -n drbdsetup
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/drbdsetup
%attr(755,root,root) /etc/rc.d/init.d/drbd
%attr(755,root,root) /etc/ha.d/resource.d/datadisk
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/drbd.conf
%{_mandir}/man[58]/*
