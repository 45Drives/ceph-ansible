ceph-ansible-45d-pacific Release notes

ANSIBLE VERSION
anisble-core == 2.12
ansible-collection-ansible*
ansible-collection-community-general
python38-netaddr
python38-six
python38-pyyaml

ALL.YML
* Simplified default all.yml. Removed unncesary options and comments for easier reading
* Dashboard - New option (dashboard_network) for specifying which network dashbaord listens on. Useful for clusters where mgmt network is separate from public
* Dashboard - New option (grafana_network) for specifying which network grafana is on.  
* Dashboard - dashboard/prometheus/alertmanager vip. ???
* Dashboard - grafana_admin_password defaults to 'p@ssw0rd' same as the default dashboard password
* Dashboard - New option (prometheus_storage_tsdb_retention_time) for changing the retention period of prometheus data.
* Dashboard - New option (igw_network) for conig with dashbaord if iscsi gw is on different subnet than public
* Global conf overrides - disable pg autoscaling
* Monitors - Disable insecure global_id reclaim

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
* disable insecure global_id reclaim by default
    * Added config option in all.yml. "allow_insecure_global_reclaim: false"
    * Need to expose via ceph-deploy for the use-case of windows rbd clients, but default to false

ceph-facts
* ansible version check ansible greater 2.10 

PRERUN
* included existing ceph-prerun role, removed centos 7 tasks
* TODO - Update container images
* TODO - Update grafana dashboards/prometheus alerts
    * Look at including quincy info

NFS
* Supports Active/Active and Active/Passive configurations
    * A/A uses nfs-ganesha cluster locking, no floating IP all gateways are active.
    * A/P uses nfs-ganesha pacemaker and keepalived for VIP and service failover.
        * Uses IP as cluster name when starting pacemaker cluster
        * Allows specifying which phsyical interface to host VIP on

DEVICE-ALIAS
* dont run/show device layout in ansible output anymore. Support for non 45drives hardware/ VMs