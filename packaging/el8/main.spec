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
* Thu Jul 22 2021 Brett Kelly <bkelly@45drives.com> 5.2.1-1
- rework prerun role to use new repo
- rework prerun role to support rocky 8
* Mon Jul 19 2021 Mark Hooper <mhooper@45drives.com> 5.2.0-3
- modified remove-vg.yml playbook
* Mon Jul 19 2021 Mark Hooper <mhooper@45drives.com> 5.2.0-2
- modified remove-vg.yml playbook
* Fri Jul 16 2021 Dawson Della Valle <ddellavalle@45drives.com> 5.2.0-1
- Finalize auto-packaging.
* Fri Jul 16 2021 Dawson Della Valle <ddellavalle@45drives.com> 0.0.0-1
- First auto-package for ubuntu & rhel.