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
* Wed Mar 09 2022 Brett Kelly <bkelly@45drives.com> 5.2.10-1
- Added support for all flash clusters
* Fri Jan 14 2022 Brett Kelly <bkelly@45drives.com> 5.2.7-1
- option to skip ceph-prerun
- disable pg_autoscaling by defualt
* Thu Oct 07 2021 Mark Hooper <mhooper@45drives.com> 5.2.3-2
- first stable build of ceph-ansible-45d v5.2.3
- modified device-alias.yml playbook to be hardware agnostic if /etc/vdev_id.conf
  was not created using dmap
* Thu Oct 07 2021 Mark Hooper <mhooper@45drives.com> 5.2.3-1
- first build for pre-release package ceph-ansible-45d
* Thu Oct 07 2021 Mark Hooper <mhooper@45drives.com> 5.2.2-6
- updated device-alias.yml to skip running dmap when /etc/vdev_id.conf exists and
  isn't created using dmap
* Mon Sep 13 2021 Brett Kelly <bkelly@45drives.com> 5.2.2-5
- ceph-iscsi: el8 install from ceph-iscsi repo
* Wed Sep 08 2021 Brett Kelly <bkelly@45drives.com> 5.2.2-4
- fixed syntax error ganesha.conf.j2
* Wed Sep 08 2021 Brett Kelly <bkelly@45drives.com> 5.2.2-3
- added rocky nfs support
* Tue Sep 07 2021 Mark Hooper <mhooper@45drives.com> 5.2.2-2
- added Rocky to list of distros in iscsi.yml
* Tue Aug 24 2021 Mark Hooper <mhooper@45drives.com> 5.2.2-1
- updated version for cockpit-ceph-deploy requirements
- releasing 5.2.2-1 on 45drives-stable repo
* Wed Jul 28 2021 Mark Hooper <mhooper@45drives.com> 5.2.1-5
- added python3-netaddr dependency for rocky
* Tue Jul 27 2021 Mark Hooper <mhooper@45drives.com> 5.2.1-4
- updated purge-rgw.yml to use apt purge to fix issue with haproxy and keepalived
* Mon Jul 26 2021 Mark Hooper <mhooper@45drives.com> 5.2.1-3
- added an infractructure playbook to purge rgw and rgwloadbalancers
* Thu Jul 22 2021 Mark Hooper <mhooper@45drives.com> 5.2.1-2
- modified generate-osd-vars.yml to ignore ceph-deploy host_vars files
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