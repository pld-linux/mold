#
# Conditional build:
%bcond_without	tests		# build without tests

Summary:	mold: A Modern Linker
Name:		mold
Version:	2.40.1
Release:	1
License:	MIT
Group:		Development/Libraries
Source0:	https://github.com/rui314/mold/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	e3633b6000ab83fe9c860518abf2d6ae
URL:		https://github.com/rui314/mold
BuildRequires:	blake3-devel
BuildRequires:	cmake >= 3.14
%{?with_tests:BuildRequires:	glibc-static}
%ifarch %{armv6} riscv64
BuildRequires:	libatomic-devel
%endif
BuildRequires:	libstdc++-devel >= 6:10
%{?with_tests:BuildRequires:	libstdc++-static >= 6:10}
BuildRequires:	mimalloc-devel >= 1.7
BuildRequires:	rpmbuild(macros) >= 2.007
BuildRequires:	tbb-devel >= 2021.3.0
BuildRequires:	zlib-devel
BuildRequires:	zstd-devel
Requires:	mimalloc >= 1.7
Requires:	tbb >= 2021.3.0
ExclusiveArch:	%{ix86} %{x8664} %{arm} aarch64 m68k ppc64 ppc64le riscv32 riscv64 s390x sparc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
mold is a faster drop-in replacement for existing Unix linkers. It is
several times faster than LLVM lld linker, the second-fastest
open-source linker which I originally created a few years ago. mold is
created for increasing developer productivity by reducing build time
especially in rapid debug-edit-rebuild cycles.

%prep
%setup -q

%{__rm} -r third-party/{mimalloc,tbb}

%build
%cmake -B build \
	%{cmake_on_off tests BUILD_TESTING} \
	-DMOLD_USE_MIMALLOC:BOOL=ON \
	-DMOLD_USE_SYSTEM_MIMALLOC:BOOL=ON \
	-DMOLD_USE_SYSTEM_TBB:BOOL=ON

%{__make} -C build

%if %{with tests}
%{__make} -C build test
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.md docs/*.md
%attr(755,root,root) %{_bindir}/ld.mold
%attr(755,root,root) %{_bindir}/mold
%dir %{_libdir}/mold
%attr(755,root,root) %{_libdir}/mold/mold-wrapper.so
%dir %{_libexecdir}/mold
%attr(755,root,root) %{_libexecdir}/mold/ld
%{_mandir}/man1/mold.1*
%{_mandir}/man1/ld.mold.1*
