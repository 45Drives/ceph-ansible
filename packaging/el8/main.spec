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
* Mon Sep 26 2022 Brett Kelly <bkelly@45drives.com> 5.3.3-1
- build 5.3.3
* Mon Sep 26 2022 Brett Kelly <bkelly@45drives.com> 5.3.3-100
- bump build rev
* Mon Sep 26 2022 Brett Kelly <bkelly@45drives.com> 5.3.3-99
- use 45drives ceph repos instead of community
* Wed Jul 06 2022 Mark Hooper <mhooper@45drives.com> 5.3.2-1
- updated samba-ansible dependency to >= 1.1.3
- updated manifest to release to 45drives stable repo
- modified samba deployment to use either winbind, or sssd to join domains.
- joining domain can now use a kerberos ticket, or username/password
- updated nfs playbooks to specify vip interface
* Tue Jul 05 2022 Brett Kelly <bkelly@45drives.com> 5.3.1-17
- specify which phys iterface the VIP will reside
* Mon Jun 20 2022 Mark Hooper <mhooper@45drives.com> 5.3.1-16
- added samba-common package to redhat_samba_packages list in purge-smb.yml
* Fri Jun 10 2022 Mark Hooper <mhooper@45drives.com> 5.3.1-15
- updated kerberos_init.yml playbook
* Thu Jun 09 2022 Mark Hooper <mhooper@45drives.com> 5.3.1-14
- added kerberos_init.yml playbook
* Thu Jun 09 2022 Mark Hooper <mhooper@45drives.com> 5.3.1-13
- updated list of redhat_samba_packages to be removed when purging samba
* Tue Jun 07 2022 Mark Hooper <mhooper@45drives.com> 5.3.1-12
- removed ceph* wildcard in list of ubuntu packages for samba
* Mon Jun 06 2022 Mark Hooper <mhooper@45drives.com> 5.3.1-11
- fixed typo in configure_memory_allocator.yml
* Fri Jun 03 2022 Mark Hooper <mhooper@45drives.com> 5.3.1-10
- updated how listeners are notified in configure_memory_allocator.yml
* Thu Jun 02 2022 Brett Kelly <bkelly@45drives.com> 5.3.1-9
- added task to remove any cephfs mounts on all hosts when purhing cluster
* Wed Jun 01 2022 Brett Kelly <bkelly@45drives.com> 5.3.1-8
- update ansible dependancy to 2.9.27
* Wed Jun 01 2022 Brett Kelly <bkelly@45drives.com> 5.3.1-7
- fixed version number
* Wed Jun 01 2022 Brett Kelly <bkelly@45drives.com> 2.3.2-1
- merged in external samba role
- added missing delegate task when creating cephfs/nfs pools
* Wed Mar 30 2022 Brett Kelly <bkelly@45drives.com> 5.3.1-6
- smb rework pre-release
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