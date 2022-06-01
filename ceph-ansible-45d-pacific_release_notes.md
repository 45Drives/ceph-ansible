ceph-ansible-45d-pacific Release notes

ALL.YML
* Simplified default all.yml. Removed unncesary options and comments for easier reading
* Dashboard - New option (dashboard_network) for specifying which network dashbaord listens on. Useful for clusters where mgmt network is separate from public
* Dashboard - New option (grafana_network) for specifying which network grafana is on.  
* Dashboard - dashboard/prometheus/alertmanager vip. ???
* Dashboard - grafana_admin_password defaults to 'p@ssw0rd' same as the default dashboard password
* Dashboard - New option (prometheus_storage_tsdb_retention_time) for changing the retention period of prometheus data.
* Dashboard - New option (igw_network) for conig with dashbaord if iscsi gw is on different subnet than public
* Global conf overrides - disable pg autoscaling 

SMB
* Uses external [samba-ansible playbooks](https://github.com/45Drives/samba-ansible) in place of the old ceph-smb role. 

CORE
* Support for all HDD, all SSD or mixed OSDs 
    * "hybrid_cluster" varible is no longer used and is removed
    * ceph-mds - create pools accordingly
    * ceph-nfs - create pools accordingly
* OSD memory target setting is honored. Regardless if there is excess memory in the server or not
    * Defaults to 2GiB
* Balancer is enabled by default. Mode is upmap

PRERUN
* included existing ceph-prerun role, removed centos 7 tasks
* TODO - Update container images
* TODO - Update grafana dashboards/prometheus alerts
    * Look at including quincy info

NFS
* Supports Active/Active and Active/Passive configurations
    * A/A uses nfs-ganesha cluster locking, no floating IP all gateways are active.
    * A/P uses nfs-ganesha pacemaker and keepalived for VIP and service failover.
