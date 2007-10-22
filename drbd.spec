#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	up		# don't build UP module
%bcond_without	smp		# don't build SMP module
%bcond_without	userspace	# don't build userspace module
%bcond_with	verbose		# verbose build (V=1)
%bcond_with	grsec_kernel	# build for kernel-grsecurity
#
%ifarch sparc
%undefine	with_smp
%endif

%if %{without kernel}
%undefine	with_dist_kernel
%endif
%if %{with kernel} && %{with dist_kernel} && %{with grsec_kernel}
%define	alt_kernel	grsecurity
%endif
%if "%{_alt_kernel}" != "%{nil}"
%undefine	with_userspace
%endif

%define		_rel	55
%define		kname	drbd
Summary:	drbd is a block device designed to build high availibility clusters
Summary(pl):	drbd jest urz±dzeniem blokowym dla klastrów o wysokiej niezawodno¶ci
Name:		%{kname}%{_alt_kernel}
Version:	0.7.24
Release:	%{_rel}
License:	GPL
Group:		Base/Kernel
Source0:	http://oss.linbit.com/drbd/0.7/%{kname}-%{version}.tar.gz
# Source0-md5:	b2c7335514a355b874a634dc12b22522
Patch0:		%{kname}-Makefile.patch
# based on http://members.home.nl/maarten/drbd-0.7.22-2.6.19.patch but compliant
# with older kernels
Patch1:		%{kname}-0.7.22-2.6.19-friendly.patch
URL:		http://www.drbd.org/
%if %{with userspace}
BuildRequires:	bison
BuildRequires:	flex
%endif
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build}
%if %{with kernel}
BuildRequires:	rpmbuild(macros) >= 1.330
%endif
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
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
Conflicts:	drbdsetup24

%description -n drbdsetup
Setup tool and init scripts for DRBD.

%description -n drbdsetup -l pl
Narzêdzie konfiguracyjne i skrypty startowe dla DRBD.

%package -n kernel%{_alt_kernel}-block-drbd
Summary:	Kernel module with drbd - a block device designed to build high availibility clusters
Summary(pl):	Modu³ j±dra do drbd - urz±dzenia blokowego dla klastrów o wysokiej niezawodno¶ci
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Requires:	drbdsetup

%description -n kernel%{_alt_kernel}-block-drbd
drbd is a block device which is designed to build high availability
clusters. This is done by mirroring a whole block device via (a
dedicated) network. You could see it as a network RAID1.

%description -n kernel%{_alt_kernel}-block-drbd -l pl
drbd jest urz±dzeniem blokowym zaprojektowanym dla klastrów o wysokiej
niezawodno¶ci. drbd dzia³a jako mirroring ca³ego urz±dzenia blokowego
przez (dedykowan±) sieæ. Mo¿e byæ widoczny jako sieciowy RAID1.

%package -n kernel%{_alt_kernel}-smp-block-drbd
Summary:	SMP kernel module with drbd - a block device designed to build high availibility clusters
Summary(pl):	Wersja SMP Modu³u j±dra do drbd - urz±dzenia blokowego dla klastrów o wysokiej niezawodno¶ci
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
Requires:	drbdsetup

%description -n kernel%{_alt_kernel}-smp-block-drbd
drbd is a block device which is designed to build high availability
clusters. This is done by mirroring a whole block device via (a
dedicated) network. You could see it as a network RAID1.

%description -n kernel%{_alt_kernel}-smp-block-drbd -l pl
drbd jest urz±dzeniem blokowym zaprojektowanym dla klastrów o wysokiej
niezawodno¶ci. drbd dzia³a jako mirroring ca³ego urz±dzenia blokowego
przez (dedykowan±) sieæ. Mo¿e byæ widoczny jako sieciowy RAID1.

%prep
%setup -q -n %{kname}-%{version}
%patch0 -p1
#%patch1 -p1

%build
%if %{with userspace}
%{__make} tools \
	KVER=dummy \
	CC="%{__cc}" \
	OPTCFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"
%endif

%if %{with kernel}
cd drbd
sed -i -e 's#$(CONFIG_BLK_DEV_DRBD)#m#g' Makefile-2.6
ln -sf Makefile-2.6 Makefile
# kernel module(s)
%build_kernel_modules -m drbd EXTRA_CFLAGS="-DNO_MORE_DEV_FS"
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/sbin,%{_mandir}/man{5,8},%{_sysconfdir}} \
	$RPM_BUILD_ROOT{/etc/rc.d/init.d,/etc/ha.d/resource.d}

%if %{with kernel}
%install_kernel_modules -m drbd/drbd -d misc
%endif

%if %{with userspace}
install user/{drbdadm,drbdsetup} $RPM_BUILD_ROOT/sbin
install scripts/drbd.conf $RPM_BUILD_ROOT%{_sysconfdir}
install scripts/drbd $RPM_BUILD_ROOT/etc/rc.d/init.d

install scripts/drbddisk $RPM_BUILD_ROOT%{_sysconfdir}/ha.d/resource.d

install documentation/*.5 $RPM_BUILD_ROOT%{_mandir}/man5
install documentation/*.8 $RPM_BUILD_ROOT%{_mandir}/man8
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post -n kernel%{_alt_kernel}-block-drbd
%depmod %{_kernel_ver}

%postun -n kernel%{_alt_kernel}-block-drbd
%depmod %{_kernel_ver}

%post -n kernel%{_alt_kernel}-smp-block-drbd
%depmod %{_kernel_ver}smp

%postun -n kernel%{_alt_kernel}-smp-block-drbd
%depmod %{_kernel_ver}smp

%post -n drbdsetup
/sbin/chkconfig --add drbd
%service drbd restart

%preun -n drbdsetup
if [ "$1" = "0" ]; then
	%service drbd stop
	/sbin/chkconfig --del drbd
fi

%if %{with userspace}
%files -n drbdsetup
%defattr(644,root,root,755)
%attr(755,root,root) /sbin/*
%attr(754,root,root) /etc/rc.d/init.d/drbd
%attr(755,root,root) %{_sysconfdir}/ha.d/resource.d/drbddisk
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/drbd.conf
%{_mandir}/man[58]/*
%endif

%if %{with kernel}
%if %{with up} || %{without dist_kernel}
%files -n kernel%{_alt_kernel}-block-drbd
%defattr(644,root,root,755)
%doc ChangeLog README
/lib/modules/%{_kernel_ver}/misc/drbd.ko*
%endif

%if %{with smp} && %{with dist_kernel}
%files -n kernel%{_alt_kernel}-smp-block-drbd
%defattr(644,root,root,755)
%doc ChangeLog README
/lib/modules/%{_kernel_ver}smp/misc/drbd.ko*
%endif
%endif
