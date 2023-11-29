%define major 1
%define oldlibname %mklibname seat 1
%define libname %mklibname seat
%define devname %mklibname -d seat

Summary:	A minimal seat management daemon and library
Name:		seatd
Version:	0.8.0
Release:	1
License:	MIT
Group:		System/Servers
URL:		https://git.sr.ht/~kennylevinsen/seatd
Source0:	https://git.sr.ht/~kennylevinsen/seatd/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:	seatd.sysusers
BuildRequires:	meson
BuildRequires:	scdoc
BuildRequires:	pkgconfig(libsystemd)

%description
A seat management daemon, that does everything it needs to do.
Nothing more, nothing less. Depends only on libc.

%package -n %{libname}
Summary:	Library files for %{name}
Group:		System/Libraries
%rename		%{oldlibname}

%description -n %{libname}
A seat management library allowing applications to use whatever seat
management is available.

Supports:
 * seatd
 * (e)logind
 * embedded seatd for standalone operation

Each backend can be compile-time included and is runtime auto-detected or
manually selected with the LIBSEAT_BACKEND environment variable.

Which backend is in use is transparent to the application, providing a
simple common interface.

%package -n %{devname}
Summary:	Development files for %{name}
Requires:	%{libname} = %{EVRD}
Group:		Development/C

%description -n %{devname}
Development files for %{name}.

%prep
%autosetup -p1

%build
%meson \
	-Dlibseat-logind=systemd \
	-Dserver=enabled

%meson_build

%install
%meson_install

install -D -m 0644 -pv contrib/systemd/%{name}.service %{buildroot}%{_unitdir}/%{name}.service
install -D -m 0644 -pv %{SOURCE1} %{buildroot}%{_sysusersdir}/%{name}.conf

%pre
%sysusers_create_package %{name} %{SOURCE1}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%{_bindir}/%{name}*
%{_sysusersdir}/%{name}.conf
%{_unitdir}/%{name}.service
%doc %{_mandir}/man1/%{name}*.*

%files -n %{libname}
%{_libdir}/libseat.so.%{major}*

%files -n %{devname}
%{_includedir}/*.h
%{_libdir}/libseat.so
%{_libdir}/pkgconfig/*.pc
