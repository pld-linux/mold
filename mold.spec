Summary:	mold: A Modern Linker
Name:		mold
Version:	1.1.1
Release:	1
License:	GPL v3+
Group:		Development/Libraries
Source0:	https://github.com/rui314/mold/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	49a64a18376bb6b216c05a900f4aacae
URL:		https://github.com/rui314/mold
BuildRequires:	libstdc++-devel >= 6:10
BuildRequires:	mimalloc-devel >= 1.7
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	tbb-devel >= 2021.3.0
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
%{__make} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcppflags} %{rpmcflags}" \
	CXXFLAGS="%{rpmcppflags} %{rpmcxxflags}" \
	LDFLAGS="%{rpmldflags}" \
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
%dir %{_libexecdir}/mold
%attr(755,root,root) %{_libexecdir}/mold/ld
%{_mandir}/man1/mold.1*
