Summary:	mold: A Modern Linker
Name:		mold
Version:	1.0.0
Release:	1
License:	GPL v3+
Group:		Development/Libraries
Source0:	https://github.com/rui314/mold/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	27e4b3bc9ae9b65a9bc90785de31ace6
URL:		https://github.com/rui314/mold
BuildRequires:	libstdc++-devel >= 6:10
BuildRequires:	mimalloc-devel >= 1.7
BuildRequires:	openssl-devel
BuildRequires:	tbb-devel >= 2021.3.0
BuildRequires:	xxHash-devel
BuildRequires:	zlib-devel
Requires:	mimalloc >= 1.7
Requires:	tbb >= 2021.3.0
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
export CPPFLAGS="%{rpmcppflags}"
export CFLAGS="%{rpmcflags}"
export CXXFLAGS="%{rpmcxxflags}"
export LDFLAGS="%{rpmldflags}"
%{__make} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	SYSTEM_MIMALLOC=1 \
	SYSTEM_TBB=1 \
	PREFIX="%{_prefix}" \
	BINDIR="%{_bindir}" \
	LIBDIR="%{_libdir}" \
	MANDIR="%{_mandir}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	D=$RPM_BUILD_ROOT \
	SYSTEM_MIMALLOC=1 \
	SYSTEM_TBB=1 \
	STRIP=: \
	PREFIX="%{_prefix}" \
	BINDIR="%{_bindir}" \
	LIBDIR="%{_libdir}" \
	MANDIR="%{_mandir}"

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CONTRIBUTING.md README.md docs/*.md
%attr(755,root,root) %{_bindir}/ld.mold
%attr(755,root,root) %{_bindir}/ld64.mold
%attr(755,root,root) %{_bindir}/mold
%dir %{_libdir}/mold
%attr(755,root,root) %{_libdir}/mold/mold-wrapper.so
%{_mandir}/man1/mold.1*
