# Notable changes from ceph-ansible-45d 1.4.1

- ceph-alias role is now a standalone playbook called device-alias.yml
- Uses 45drives-tools >= 1.6
- added update-server.yml playbook. update all ceph nodes in parallel
- samba role now import samba-shares playbook. samba-shares playbook can be run after deployment to add new shares without reconfiging the whole smb cluster
- 
