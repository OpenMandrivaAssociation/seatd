%define major	1
%define libname	%mklibname seat %{major}
%define devname	%mklibname -d seat


Name:           seatd
Version:	0.4.0
Release:	1
Summary:        A minimal seat management daemon and library
License:        MIT
URL:            https://git.sr.ht/~kennylevinsen/seatd
Source0:	https://git.sr.ht/~kennylevinsen/seatd/archive/%{version}.tar.gz
BuildRequires:	meson
BuildRequires:	scdoc


%description
%{summary}.

%package -n     %{libname}
Summary:        Library files for %{name}

%description -n %{libname}
A seat management library allowing applications to use whatever seat management is available.
Supports:
    seatd
    (e)logind
    embedded seatd for standalone operation

%package -n     %{devname}
Requires:	%{libname} = %{EVRD}
Summary:        Development files for %{name}

%description -n %{devname}
Development files for %{name}.

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install

%files
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.*

%files -n %{libname}
%{_libdir}/libseat.so.%{major}*

%files -n %{devname}
%{_includedir}/*.h
%{_libdir}/libseat.so
%{_libdir}/pkgconfig/*.pc
