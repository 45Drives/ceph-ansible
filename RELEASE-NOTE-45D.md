# Notable changes from ceph-ansible-45d 1.4.1
  - ceph-alias role is now a standalone playbook called device-alias.yml
  - Uses 45drives-tools >= 1.6
  - Samba deployments are split into samba-config,samba-domain-join and samba-shares insteads of the monolithic smb.yml

