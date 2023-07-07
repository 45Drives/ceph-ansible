all:

install:
	mkdir -p $(DESTDIR)/usr/share/ceph-ansible/

	cp -a ansible.cfg $(DESTDIR)/usr/share/ceph-ansible/
	cp -a *.yml $(DESTDIR)/usr/share/ceph-ansible/
	cp -a *.sample $(DESTDIR)/usr/share/ceph-ansible/
	cp -a group_vars $(DESTDIR)/usr/share/ceph-ansible/
	cp -a roles $(DESTDIR)/usr/share/ceph-ansible/
	cp -a library $(DESTDIR)/usr/share/ceph-ansible/
	cp -a plugins $(DESTDIR)/usr/share/ceph-ansible/
	cp -a infrastructure-playbooks $(DESTDIR)/usr/share/ceph-ansible/

uninstall:
	rm -rf $(DESTDIR)/usr/share/ceph-ansible