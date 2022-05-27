ceph-ansible-45d-pacific Release notes

ALL.YML
* Simplified default all.yml. Removed unncesary options and comments for easier reading
* Dashboard - New option (dashboard_network) for specifying which network dashbaord listens on. Useful for clusters where mgmt network is separate from public
* Dashboard - New option (grafana_network) for specifying which network grafana is on.  
* Dashboard - dashboard/prometheus/alertmanager vip. ???
* Dashboard - grafana_admin_password defaults to 'p@ssw0rd' same as the default dashboard password
* Dashboard - New option (prometheus_storage_tsdb_retention_time) for changing the retention period of prometheus data.
* Dashboard - New option (igw_network) for conig with dashbaord if iscsi gw is on different subnet than public

SMB
* Uses external [samba-ansible playbooks](https://github.com/45Drives/samba-ansible) in place of the old ceph-smb role. 

CORE
* Support for all HDD, all SSD or mixed OSDs 
    * "hybrid_cluster" varible is no longer used and is removed
    * ceph-mds - create pools accordingly
    * ceph-nfs - create pools accordingly



