Name: ::package_name::
Version: ::package_version::
Release: ::package_build_version::%{?dist}
Summary: ::package_description_short::
License: ::package_licence::
URL: ::package_url::
Source0: %{name}-%{version}.tar.gz
BuildArch: ::package_architecture_el::
Requires: ::package_dependencies_el::

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
::package_title::
::package_description_long::

%prep
%setup -q

%build

%install
make DESTDIR=%{buildroot} install

%files
%doc README.rst
%license LICENSE
/usr/share/ceph-ansible/*

%changelog
* Fri Jul 16 2021 Dawson Della Valle <ddellavalle@45drives.com> 5.2.0-1
- Finalize auto-packaging.
* Fri Jul 16 2021 Dawson Della Valle <ddellavalle@45drives.com> 0.0.0-1
- First auto-package for ubuntu & rhel.