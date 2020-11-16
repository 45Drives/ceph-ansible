================================
Ceph Nautilus Installation Guide
================================

.. contents::
   :depth: 3
..

.. container:: c41

   Ceph Version 14 - Nautilus

   Installation Guide for CentOS 7.

   Release Version 1.4

   --------------

   --------------

   .. rubric:: CHAPTER 1 - WHAT IS CEPH?
      :name: CephNautilusInstallationGuide.xhtml#h.conp56i8v25p
      :class: c14

   Ceph is a license free, open source storage platform that ties
   together multiple storage servers to provide interfaces for object,
   block and file-level storage in a single, horizontally scalable
   storage cluster, with no single point of failure.

   Ceph clusters consist of several different types of services which
   will be explained below :

   .. rubric:: 1.1 - ANSIBLE  ADMINISTRATOR NODE
      :name: CephNautilusInstallationGuide.xhtml#h.vumpkpueddgh
      :class: c25 c17

   T his type of node is where ansible will be configured and run from.
   Any node in the cluster can functi on as the ansible node. This node
    provide the following functions:

   -  Centralized storage cluster management
   -  Ceph configuration files and keys
   -  Optionally, local repositories for installing Ceph on nodes that
      cannot access the Internet

   .. rubric:: 1.2 - MONITOR NODES
      :name: CephNautilusInstallationGuide.xhtml#h.uciuo64rc4gh
      :class: c25 c17

   Each monitor node runs the monitor daemon ( ceph-mon ), which
   maintains a master copy of the cluster map. The cluster map includes
   the cluster topology. A client connecting to the Ceph cluster
   retrieves the current copy of the cluster map from the monitor which
   enables the client to read from and write data to the cluster.
   It's Important  to note that Ceph can run with one monitor; however,
   it is highly suggested to have three monitors to ensure high
   availability.

   .. rubric:: 1.3 - OSD NODES
      :name: CephNautilusInstallationGuide.xhtml#h.f4t020mpta9n
      :class: c25 c17

   Each Object Storage Device (OSD) node runs the Ceph OSD daemon (
   ceph-osd ), which interacts with  logical disks attached to the node
   . Simply put, an OSD node  is a server, and an OSD  itself is an HDD
   or SSD inside the server.  Ceph stores data on these OSDs. Ceph can
   run with very few OSD nodes, where the minimum is three , but
   production clusters realize better performance beginning at modest
   scales, for example 5 OSD nodes in a storage cluster . Ideally, a
   Ceph cluster has multiple OSD nodes, allowing isolated failure
   domains by creating the CRUSH map.

   --------------

   .. rubric:: 
      :name: CephNautilusInstallationGuide.xhtml#h.8d1y07aqd2km
      :class: c25 c17 c38

   .. rubric:: 1.4 - MANAGER NODES
      :name: CephNautilusInstallationGuide.xhtml#h.zh1lda5n1cix
      :class: c25 c17

   Each Manager node runs the MGR daemon ( ceph-mgr ), which maintains
   detailed information about placement groups, process metadata and
   host metadata in lieu of the Ceph Monitor—​significantly improving
   performance at scale. The Ceph Manager handles execution of many of
   the read-only Ceph CLI queries, such as placement group statistics.
   The Ceph Manager also provides the RESTful monitoring APIs.  The
   manager node is also responsible for dashboard hosting, giving the
   user real time metrics, as well as the capability to create new
   pools, exports, etc.

   .. rubric:: 1.5 - MDS NODES
      :name: CephNautilusInstallationGuide.xhtml#h.3advr7nsogu7
      :class: c25 c17

    Each Metadata Server (MDS) node runs the MDS daemon ( ceph-mds ),
   which manages metadata related to files stored on the Ceph File
   System (CephFS). The MDS daemon also coordinates access to the shared
   cluster. The MDS daemon maintains a cache of CephFS metadata in
   system memory to accelerate IO performance. This cache size can be
   grown or shrunk based on workload, allowing linearly scaling of
   performance as data grows. The service is required for CephFS to
   function.

   .. rubric:: 1.6 - OBJECT GATEWAY NODES
      :name: CephNautilusInstallationGuide.xhtml#h.vkv9rj5r2pyy
      :class: c25 c17

   Ceph Object Gateway node runs the Ceph RADOS Gateway daemon (
   ceph-radosgw ), and is an object storage interface built on top of
   librados to provide applications with a RESTful gateway to Ceph
   Storage Clusters. The Ceph Object Gateway supports two interfaces:

   -  S3  - Provides object storage functionality with an interface that
      is compatible with a large subset of the Amazon S3 RESTful API.
   -  Swift - Provides object storage functionality with an interface
      that is compatible with a large subset of the OpenStack Swift API.

   --------------

   Below is a diagram showing the architecture of the above services,
   and how they communicate on the networks.

   The cluster network relieves OSD replication and heartbeat traffic
   from the public network.

   --------------

   .. rubric:: CHAPTER 2 - REQUIREMENTS FOR INSTALLING CEPH
      :name: CephNautilusInstallationGuide.xhtml#h.1ju3awi1xn6a
      :class: c14

   Before starting the installation and configuration of your Ceph
   cluster, there are a few requirements that need to be met.

   .. rubric:: 2.1 - HARDWARE REQUIREMENTS
      :name: CephNautilusInstallationGuide.xhtml#h.ezcmb1fee5hl
      :class: c25 c17

   As mentioned before, there are minimum quantities required for the
   different types of nodes. Below is a table showing the minimum number
   required to achieve a highly available Ceph cluster. It is important
    to note that the MON’s, MGR’s, MDS’s, FSGW’s , and RGW’s  can be
   either virtualized or on physical hardware.

   +---------+---------+---------+---------+---------+---------+---------+
   | Pool    | OSD     | MON     | MGR     | MDS     | FSGW    | RGW     |
   | Type    |         |         |         |         |         |         |
   +---------+---------+---------+---------+---------+---------+---------+
   | 2 Rep / | 3       | 3       | 2       | 2       | 2       | 2       |
   | 3 Rep   |         |         |         |         |         |         |
   +---------+---------+---------+---------+---------+---------+---------+
   | Erasure | 3       | 3       | 2       | 2       | 2       | 2       |
   | Coded   |         |         |         |         |         |         |
   +---------+---------+---------+---------+---------+---------+---------+

   .. rubric:: 2.2 - OPERATING SYSTEM
      :name: CephNautilusInstallationGuide.xhtml#h.hrwwwcix7p8p
      :class: c25 c17

   45Drives requires that Ceph Naut i l us  be deployed on a minimal
   installation of
   CentOS 7.6  or newer. Every node in the cluster should be running the
   same version to ensure uniformity.

   .. rubric:: 2.3 - NETWORK CONFIGURATION
      :name: CephNautilusInstallationGuide.xhtml#h.u7etrhynb5c
      :class: c25 c17

   As seen in the Figure in Chapter 1, all Ceph nodes require a public
   network. It is required to have a network interface card configured
   to a public network where Ceph clients can reach Ceph monitors and
   Ceph OSD nodes.

   45Drives recommends having a second network interface card configured
   as a backend private  network so that Ceph can conduct heart-beating,
   peering, replication, and recovery on a network separate from the
   public network. It is recommended to configure network   b ond ing
    on each network interface card across the cluster. Choice of bonding
   mode will vary depending on needs. 45Drives recommends, either
   bonding mode 1 (Active-Backup) and 4 (LACP) for the cluster nodes.

   --------------

   .. raw:: html

      </p>

   .. rubric:: 2.4 - CONFIGURING FIREWALLS
      :name: CephNautilusInstallationGuide.xhtml#h.fx691pdw4ffj
      :class: c25 c17

   By default w hen installing Ceph using these ansible packages , it
   will open  the required  firewall ports on the appropriate nodes
   using firew alld .

   If using iptables or  requiring manual firewall configuration,  the
   following  is a table for reference showing the default ports /
   ranges which are required for each c e ph daemon as well as services
   used for real time metrics. These must be open before you begin
   installing the cluster.

   Note the cluster role column, that will determine which hosts need
   the ports opened. It corresponds with the group names in the ansible
   inventory file.

   +-------------+-------------+-------------+-------------+-------------+
   | Ceph Daemon | Firewall    | Protocol    | Firewalld   | Cluster     |
   | / Service   | Port        |             |             | Role        |
   |             |             |             | Service     |             |
   |             |             |             | Name        |             |
   +-------------+-------------+-------------+-------------+-------------+
   | ceph-osd    | 6800-7300   | TCP         | ceph        | osds        |
   +-------------+-------------+-------------+-------------+-------------+
   | ceph-mon    | 6789,3300   | TCP         | ceph,       | mons        |
   |             |             |             | ceph-mon    |             |
   +-------------+-------------+-------------+-------------+-------------+
   | ceph-mgr    | 6800-7300   | TCP         | ceph        | mgrs        |
   +-------------+-------------+-------------+-------------+-------------+
   | ceph-mds    | 6800        | TCP         | ceph        | mdss        |
   +-------------+-------------+-------------+-------------+-------------+
   | ceph-radosg | 8080        | TCP         |             | rgws        |
   | w           |             |             |             |             |
   | `[1] <#Ceph |             |             |             |             |
   | NautilusIns |             |             |             |             |
   | tallationGu |             |             |             |             |
   | ide.xhtml#f |             |             |             |             |
   | tnt1>`__    |             |             |             |             |
   +-------------+-------------+-------------+-------------+-------------+
   | Ceph        | 9283        | TCP         |             | mgrs        |
   | Prometheus  |             |             |             |             |
   | Exporter    |             |             |             |             |
   +-------------+-------------+-------------+-------------+-------------+
   | Node        | 9100        | TCP         |             | metric      |
   | Exporter    |             |             |             |             |
   +-------------+-------------+-------------+-------------+-------------+
   | Prometheus  | 9090        | TCP         |             | metric      |
   | Server      |             |             |             |             |
   +-------------+-------------+-------------+-------------+-------------+
   | Alertmanage | 9091        | TCP         |             | metric      |
   | r           |             |             |             |             |
   +-------------+-------------+-------------+-------------+-------------+
   | Grafana     | 3000        | TCP         |             | metric      |
   | Server      |             |             |             |             |
   +-------------+-------------+-------------+-------------+-------------+
   | nfs         | 2049        | TCP         | nfs         | nfss        |
   +-------------+-------------+-------------+-------------+-------------+
   | rpcbind     | 111         | TCP/UDP     | rpc-bind    | nfss        |
   +-------------+-------------+-------------+-------------+-------------+
   | corosync    | 5404-5406   | UDP         |             | nfss        |
   +-------------+-------------+-------------+-------------+-------------+
   | pacemaker   | 2224        | TCP         |             | nfss        |
   +-------------+-------------+-------------+-------------+-------------+
   | samba       | 137,138     | UDP         | samba       | smbs        |
   +-------------+-------------+-------------+-------------+-------------+
   | samba       | 139,445     | TCP         | samba       | smbs        |
   +-------------+-------------+-------------+-------------+-------------+
   | CTDB        | 4379        | TCP/UDP     | ctdb        | smbs        |
   +-------------+-------------+-------------+-------------+-------------+
   | iSCSI       | 3260        | TCP         |             | iscsigws    |
   | Target      |             |             |             |             |
   +-------------+-------------+-------------+-------------+-------------+
   | iSCSI API   | 5000        | TCP         |             | iscsigws    |
   | Port        |             |             |             |             |
   +-------------+-------------+-------------+-------------+-------------+
   | iSCSI       | 9287        | TCP         |             | iscsigws    |
   | Metric      |             |             |             |             |
   | Exporter    |             |             |             |             |
   +-------------+-------------+-------------+-------------+-------------+

           

   .. rubric:: 2.5 - CONFIGURING PASSWORDLESS SSH
      :name: CephNautilusInstallationGuide.xhtml#h.lwch9jnnmg4n
      :class: c25 c17

   Generate an SSH key pair on the Ansible administrator node and
   distribute the public key to all other nodes in the storage cluster
   so that Ansible can access the nodes without being prompted for a
   password.

   Perform the following steps from the Ansible administrator node, as
   the root user.

   #. Generate the SSH key pair, accept the default filename and leave
      the passphrase empty:

   +-----------------------------------------------------------------------+
   | [root @cephADMIN  ~] $ ssh-keygen                                     |
   +-----------------------------------------------------------------------+

          
         2. Copy the public key to all nodes in the storage cluster:  

   +-----------------------------------------------------------------------+
   | [root@cephADMIN ~]$ ssh- copy -id root@ $HOST_NAME                    |
   +-----------------------------------------------------------------------+

   Replace $HOST_NAME with the host name of the Ceph nodes.

   Example

   +-----------------------------------------------------------------------+
   | [root @cephADMIN  ~] $ ssh-copy-id root @cephOSD1                     |
   +-----------------------------------------------------------------------+

   .. rubric:: 2.6 - INSTALL CEPH-ANSIBLE-45D
      :name: CephNautilusInstallationGuide.xhtml#h.ilezps5cszgq
      :class: c25 c17

   45Drives provides a slightly  modified ceph-ansible repository on
   GitHub. From the Ansible administrator node, the first thing to do is
   to pull down the ceph-ansible archive and run the admin-setup script.

   +-----------------------------------------------------------------------+
   | [root @cephADMIN  ~] $ cd /etc/yum.repos.d/                           |
   | [root @cephADMIN  ~] $ curl -LO http: /                               |
   | /images.45drives.com/ceph/rpm/ceph \_45drives.repo                    |
   | [root @cephADMIN  ~] $ yum install ceph-ansible- 45 d                 |
   |                                                                       |
   | [root @cephADMIN  ~] $ touch /usr/share/ceph-ansible/hosts            |
   |                                                                       |
   | [root @cephADMIN ~] $ ln -s /usr/share/ceph-ansible/hosts             |
   | /etc/ansible                                                          |
   +-----------------------------------------------------------------------+

   This will set up  the Ansible environment for a 45Drives Ceph
   cluster.

   .. rubric:: CHAPTER 3 - DEPLOYING CEPH NAUTILUS
      :name: CephNautilusInstallationGuide.xhtml#h.b1szwxxvzbhy
      :class: c14

   This chapter describes how to use the Ansible application to deploy a
   Ceph cluster and other components, such as Metadata Servers, File
   System Gateways, Ceph Object Gateways etc.

   .. rubric:: 3.1 - PREREQUISITES
      :name: CephNautilusInstallationGuide.xhtml#h.uff49erds29x
      :class: c25 c17

   Prepare the cluster nodes. On each node verify:

   -  Passwordless SSH configured from Ansible Node  to all other nodes
   -  Network ing configured

   -  All nodes must be reachable from each on the public network
   -  All OSDS nodes must be reachable on the cluster network as well

   .. rubric:: 3.2 - INSTALLING A CEPH CLUSTER
      :name: CephNautilusInstallationGuide.xhtml#h.cuhd5pekujuu
      :class: c25 c17

   #. Navigate to the /usr/share/ceph-ansible/ directory

   +-----------------------------------------------------------------------+
   | [root @cephADMIN  ~] # cd /usr/share/ceph-ansible/                    |
   +-----------------------------------------------------------------------+

   2. Edit the hosts file and place the hostnames under the correct
      blocks. It is common to collocate the Ceph Manager ( ceph_mgr )
      with the Ceph Monitor nodes.
      If you have a lengthy list with sequential naming you can use a
      range such as OSD_[1:10] . See hosts.sample for a full list of
      host groups available.

   +-----------------------------------------------------------------------+
   | [mons]                                                                |
   | MONITOR_1                                                             |
   | MONITOR_2                                                             |
   | MONITOR_3                                                             |
   | [mgrs]                                                                |
   | MONITOR_1                                                             |
   | MONITOR_2                                                             |
   | MONITOR_3                                                             |
   | [osds]                                                                |
   | OSD_1                                                                 |
   | OSD_2                                                                 |
   | OSD_3                                                                 |
   +-----------------------------------------------------------------------+

   3. Ensure that Ansible can reach the Ceph hosts. Until this finishes
      with success, stop here and verify the connectivity to each host
      in your host file.

   +-----------------------------------------------------------------------+
   | [root @cephADMIN  ceph-ansible] # ansible all -m ping                 |
   +-----------------------------------------------------------------------+

   4. Edit the group_vars/all.yml file:

   +-----------------------------------------------------------------------+
   | [root @cephADMIN  ceph-ansible] # vim group_vars/all.yml              |
   +-----------------------------------------------------------------------+

   Below is a table that includes the minimum parameters that have to be
   updated.

   +-----------------+-----------------+-----------------+-----------------+
   | Option          | Value           | Required        | Notes           |
   +-----------------+-----------------+-----------------+-----------------+
   | monitor_interfa | The interface   | 1 of the 3      | monitor_interfa |
   | ce              | that the        |                 | ce              |
   |                 | Monitor nodes   |                 | ,               |
   |                 | listen to       |                 | monitor_address |
   |                 | (eth0, bond0,   |                 | , or            |
   |                 | etc)            |                 | monitor_address |
   |                 |                 |                 | \_              |
   |                 |                 |                 | block  is       |
   |                 |                 |                 | required        |
   +-----------------+-----------------+-----------------+-----------------+
   | public_network  | The IP address  | Yes             | In the form of: |
   |                 | and netmask of  |                 | 192.168.0.0/16  |
   |                 | the Ceph public |                 |                 |
   |                 | network         |                 |                 |
   +-----------------+-----------------+-----------------+-----------------+
   | cluster_network | The IP address  | No, defaults to | In the form of: |
   |                 | and netmask of  | public_network  | 10.0.0.0/24     |
   |                 | the Ceph        |                 |                 |
   |                 | cluster network |                 |                 |
   +-----------------+-----------------+-----------------+-----------------+
   | hybrid_cluster  | Are there SSD   | No, defaults to | In the form of  |
   |                 | and HDD OSDs in | false           | true or false   |
   |                 | the cluster ?   |                 |                 |
   +-----------------+-----------------+-----------------+-----------------+

   5. Run the ansible-playbook to configure device alias’.

   +-----------------------------------------------------------------------+
   | [root @cephADMIN  ceph-ansible] # ansible-playbook device-alias.yml   |
   +-----------------------------------------------------------------------+

   6. Run the ansible-playbook to generate-osd-vars.yml to populate
      device variables. This will use every disk present in the chassis.
      If you want to exclude certain drives manually remove them from
      the host_vars/ file.

   +-----------------------------------------------------------------------+
   | [root @cephADMIN  ceph-ansible] # ansible-playbook                    |
   | generate-osd-vars.yml                                                 |
   +-----------------------------------------------------------------------+

   7. Run the ceph-ansible playbook to build the cluster. When it
      finishes, the core components of the cluster are deployed and can
      be verified by running “ceph -s” from one of the monitor nodes.

   +-----------------------------------------------------------------------+
   | [root @cephADMIN  ceph-ansible] # ansible-playbook core2.yml          |
   +-----------------------------------------------------------------------+

   .. rubric:: 3.3 - INSTALLING METADATA SERVERS (CephFS )
      :name: CephNautilusInstallationGuide.xhtml#h.tmjfzs1qj3pc
      :class: c25 c17

   Metadata Server daemons are necessary for deploying a Ceph File
   System. This section will show you using Ansible, how to install a
   Ceph Metadata Server (MDS)

   #. Add a new section [mdss]  to the / usr/share/ceph-ansible /hosts
      file:

   +-----------------------------------------------------------------------+
   | [mdss]                                                                |
   | cephMDS1                                                              |
   | cephMDS2                                                              |
   | cephMDS3                                                              |
   +-----------------------------------------------------------------------+

   2. Run the cephfs.yml  playbook and  install and configure the Ceph
      Metadata Servers.

   +-----------------------------------------------------------------------+
   | [ root @cephADMIN  ceph-ansible] # ansible-playbook cephfs.yml        |
   +-----------------------------------------------------------------------+

   3. Verify the file system from one of the cluster nodes

   +-----------------------------------------------------------------------+
   | [root @cephMON  ~] # ceph fs status                                   |
   +-----------------------------------------------------------------------+

   .. rubric:: 3.4 - INSTALLING THE CEPH OBJECT GATEWAY
      :name: CephNautilusInstallationGuide.xhtml#h.fl5omxgeo27m
      :class: c25 c17

   The Ceph Object Gateway, also known as the RADOS gateway, is an
   object storage interface built on top of the librados API to provide
   applications with a RESTful gateway to Ceph storage clusters.

   #. Add a new section, [rgws]  to the / usr/share /ceph-ansible/hosts
       file . Be sure to define the IP for each rgw as well.

   +-----------------------------------------------------------------------+
   | [rgws]                                                                |
   | cephRGW1 radosgw_address= 192.168.18.53                               |
   | cephRGW2 radosgw_address= 192.168.18.56                               |
   +-----------------------------------------------------------------------+

   2. The default port will be 80 , change the following line in
      group_vars/all.yml if another is desired:

   +-----------------------------------------------------------------------+
   | radosgw_civetweb_port:   8080                                         |
   +-----------------------------------------------------------------------+

   3. Below is an example section of the group_vars/all.yml.

   +-----------------------------------------------------------------------+
   | ## Rados Gateway options                                              |
   | #                                                                     |
   | radosgw_frontend_type: beast                                          |
   | radosgw_civetweb_port: 8080                                           |
   | radosgw_civetweb_num_threads: 100                                     |
   | radosgw_civetweb_options: "num_threads= {{                            |
   | radosgw_civetweb_num_threads }} "                                     |
   | # For additional civetweb configuration options available such as     |
   | SSL, logging,                                                         |
   | # keepalive, and timeout settings, please see the civetweb docs at    |
   | # https://github.com/civetweb/civetweb/blob/master/docs/UserManual.md |
   | radosgw_frontend_port: " {{ radosgw_civetweb_port if                  |
   | radosgw_frontend_type == 'civetweb' else '8080' }} "                  |
   | radosgw_frontend_options: " {{ radosgw_civetweb_options if            |
   | radosgw_frontend_type == 'civetweb' }} "                              |
   +-----------------------------------------------------------------------+

   4. Run the rgws.yml  playbook to install the RGWs.

   +-----------------------------------------------------------------------+
   | [root @cephADMIN  ceph-ansible] # ansible-playbook radosgw.yml        |
   +-----------------------------------------------------------------------+

   5. Verify with:

   +-----------------------------------------------------------------------+
   | [root@cephADMIN ceph-ansible]# curl -g http://cephRGW1:8080           |
   | <? xml version= "1.0"  encoding= "UTF-8" ?> <ListAllMyBucketsResult   |
   | xmlns= "http://s3.amazonaws.com/doc/2006-03-01/" ><Owner><ID>         |
   | anonymous                                                             |
   | </ID><DisplayName></DisplayName></Owner><Buckets></Buckets></ListAllM |
   | yBucketsResult>                                                       |
   +-----------------------------------------------------------------------+

   .. rubric:: 
      :name: CephNautilusInstallationGuide.xhtml#h.g34qcqlslinx
      :class: c25 c17 c38

   .. rubric:: 3.4.1 Configure Haproxy for RGW Load Balancing
      :name: CephNautilusInstallationGuide.xhtml#h.lqehplpj3nug
      :class: c9

   Since each object gateway instance has its own IP address, HAProxy
   and keepalived can be used to balance the load across Ceph Object
   Gateway servers.                         

   Another use case for HAProxy and keepalived is to terminate HTTPS at
   the HAProxy server. You can use an HAProxy server to terminate HTTPS
   at the HAProxy server and use HTTP between the HAProxy server and the
   RGWs.

   #. Add a new section, [rgwloadbalancers]  to the
      /usr/share/ceph-ansible/hosts  file. The RGW nodes themselves can
      be used or other CentOS servers

   +-----------------------------------------------------------------------+
   | [rgwloadbalancers]                                                    |
   | cephRGW1                                                              |
   | cephRGW2                                                              |
   +-----------------------------------------------------------------------+

   2. Edit group_vars/rgwloadbalancers.yml and specify

   #. Virtual IP(s)
   #. Virtual IP Netmask
   #. Virtual IP interface

   +-----------------------------------------------------------------------+
   | ###########                                                           |
   | # GENERAL #                                                           |
   | ###########                                                           |
   | haproxy_frontend_port: 80                                             |
   | haproxy_frontend_ssl_port: 443                                        |
   | haproxy_frontend_ssl_certificate:                                     |
   | haproxy_ssl_dh_param: 4096                                            |
   | haproxy_ssl_ciphers:                                                  |
   |  - EECDH+AESGCM                                                       |
   |  - EDH+AESGCM                                                         |
   | haproxy_ssl_options:                                                  |
   |  - no-sslv3                                                           |
   |  - no-tlsv10                                                          |
   |  - no-tlsv11                                                          |
   |  - no-tls-tickets                                                     |
   | virtual_ips:                                                          |
   |   - 192.168.18.57                                                     |
   | virtual_ip_netmask: 16                                                |
   | virtual_ip_interface: eth0                                            |
   +-----------------------------------------------------------------------+

   .. rubric:: 3.5 - CONFIGURING THE SMB GATEWAYS
      :name: CephNautilusInstallationGuide.xhtml#h.dywkpevs1u9y
      :class: c25 c17

   There are two cases that will be covered in this section. They are:

   #. CephFS + Samba + Active Directory Integration
   #. CephFS + Samba + Local Users

   The SMB Gateways can be physical hardware or virtual machines . CTDB
   will be configured with a floating IP for access to the Samba share.

   The CephFS volume will be mounted on each gateway at /mnt/cephfs/  -
   and then the gateways share out that directory via SMB.

   Edit the hosts  file to include the File System Gateways in the
   [smbs] block.

   +-----------------------------------------------------------------------+
   | [smbs]                                                                |
   | smb1                                                                  |
   | smb2                                                                  |
   +-----------------------------------------------------------------------+

   3.5.1 CephFS + Samba + Active Directory Integration
   Edit the group_vars/smbs.yml file to choose the samba role

   +-----------------------------------------------------------------------+
   | # Roles                                                               |
   | samba_server: true                                                    |
   | samba_cluster: true                                                   |
   | domain_member: true                                                   |
   +-----------------------------------------------------------------------+

   Edit group_vars/smbs.yml to edit active_directory_info

   +-----------------------------------------------------------------------+
   | active_directory_info:                                                |
   |  workgroup: 'SAMDOM'                                                  |
   |  idmap_range: '100000 - 999999'                                       |
   |  realm: 'SAMDOM.COM'                                                  |
   |  winbind_enum_groups: yes                                             |
   |  winbind_enum_users: yes                                              |
   |  winbind_use_default_domain: yes                                      |
   |  domain_join_user: ''                                                 |
   |  domain_join_password: ''                                             |
   +-----------------------------------------------------------------------+

   Edit group_vars/smbs.yml to edit ctdb_public_addresses

   +-----------------------------------------------------------------------+
   | ctdb_public_addresses :                                               |
   |  - vip_address : '192.168.103.10'                                     |
   |     vip_interface : 'eth0'                                            |
   |     subnet_mask : '16'                                                |
   |  - vip_address : '192.168.103.11'                                     |
   |     vip_interface : 'eth0'                                            |
   |     subnet_mask : '16'                                                |
   +-----------------------------------------------------------------------+

   Edit group_vars/smbs.yml to edit samba_shares

   +-----------------------------------------------------------------------+
   | samba_shares :                                                        |
   |  - name : 'share1'                                                    |
   |     path : '{{ shared_storage_mountpoint }}/fsgw/share1'              |
   |     writeable : 'yes'                                                 |
   |     guest_ok : 'no'                                                   |
   |     comment : "comment for share1"                                    |
   |  - name : 'share2'                                                    |
   |     path : '{{ shared_storage_mountpoint }}/fsgw/share2'              |
   |     writeable : 'yes'                                                 |
   |     guest_ok : 'no'                                                   |
   |     comment : "comment for share2"                                    |
   +-----------------------------------------------------------------------+

   .. rubric:: 3.5.2 CephFS + Samba + Local Users
      :name: CephNautilusInstallationGuide.xhtml#h.v7qyzh7uenvl
      :class: c9

   If AD is not being used, set domain_member to false.

   Edit the group_vars/smbs.yml file to choose the samba role

   +-----------------------------------------------------------------------+
   | # Roles                                                               |
   | samba_server: true                                                    |
   | samba_cluster: true                                                   |
   | domain_member: false                                                  |
   +-----------------------------------------------------------------------+

   Edit group_vars/smbs.yml to edit samba_shares

   +-----------------------------------------------------------------------+
   | samba_shares :                                                        |
   |  - name : 'share1'                                                    |
   |     path : '{{ shared_storage_mountpoint }}/fsgw/share1'              |
   |     writeable : 'yes'                                                 |
   |     guest_ok : 'no'                                                   |
   |     comment : "comment for share1"                                    |
   |  - name : 'share2'                                                    |
   |     path : '{{ shared_storage_mountpoint }}/fsgw/share2'              |
   |     writeable : 'yes'                                                 |
   |     guest_ok : 'no'                                                   |
   |     comment : "comment for share2"                                    |
   +-----------------------------------------------------------------------+

   Edit group_vars/smbs.yml to edit ctdb_public_addresses

   +-----------------------------------------------------------------------+
   | ctdb_public_addresses :                                               |
   |  - vip_address : '192.168.103.10'                                     |
   |     vip_interface : 'eth0'                                            |
   |     subnet_mask : '16'                                                |
   |  - vip_address : '192.168.103.11'                                     |
   |     vip_interface : 'eth0'                                            |
   |     subnet_mask : '16'                                                |
   +-----------------------------------------------------------------------+

   Run the smb.yml  playbook:

   +-----------------------------------------------------------------------+
   | [root @cephADMIN  ceph-ansible] # ansible-playbook smb.yml            |
   +-----------------------------------------------------------------------+

   .. rubric:: 3.5.2 Samba Overrides
      :name: CephNautilusInstallationGuide.xhtml#h.ymvj8xkvavmt
      :class: c9

   In either case, all smb.conf global config options can be overridden
   using “/etc/samba/overrides.conf”. This is meant to be used when
   making user (no ansible) changes or when needing an option that is
   not defined in the playbooks. The override.conf assumes the same
   syntax as the main smb.conf.

   For example if not using the recommended centralized share management
   , you could define a share in /etc/samba/overrides.conf

   +-----------------------------------------------------------------------+
   | [global]                                                              |
   |                                                                       |
   |     log level = 3                                                     |
   |                                                                       |
   | [share1]                                                              |
   |    path = /mnt/cephfs/fsgw/share1                                     |
   |    comment = comment for  share1                                      |
   |    valid  users = user1                                               |
   |    Write list = user1                                                 |
   +-----------------------------------------------------------------------+

   .. rubric:: 3.5.3 Centralized Share Management
      :name: CephNautilusInstallationGuide.xhtml#h.fh63rpwf92s
      :class: c9

   Samba offers a registry based configuration system to complement the
   original text-only configuration via smb.conf. The "net conf" command
   offers a dedicated interface for reading and modifying the registry
   based configuration.

   .. rubric:: 3.5.3.1 Adding share
      :name: CephNautilusInstallationGuide.xhtml#h.y7i28iv9hje3
      :class: c52 c17

   To create a new share “share1” using net conf

   +-----------------------------------------------------------------------+
   | net  conf addshare share1   $PATH  writable=[ yes \| no ] guest_ok=[  |
   | yes \| no ] "comment"                                                 |
   +-----------------------------------------------------------------------+

   To add extra parameters like “valid users” and “write list”:

   +-----------------------------------------------------------------------+
   | net  conf setparm share1   $PATH  “valid users” “@readonly,@trusted”  |
   +-----------------------------------------------------------------------+

   +-----------------------------------------------------------------------+
   | net  conf setparm share1   $PATH  “write list” “@trusted”             |
   +-----------------------------------------------------------------------+

   .. rubric:: 3.5.3.2 Removing a share
      :name: CephNautilusInstallationGuide.xhtml#h.9qjpgmdzry
      :class: c17 c52

   To remove a share called “share1” using net conf

   +-----------------------------------------------------------------------+
   | net  conf delshare share1                                             |
   +-----------------------------------------------------------------------+

   .. rubric:: 3.5.3.3 Listing current shares
      :name: CephNautilusInstallationGuide.xhtml#h.uho2ptsy38y9
      :class: c52 c17

   To show all defined shares

   +-----------------------------------------------------------------------+
   | net  conf list                                                        |
   +-----------------------------------------------------------------------+

   To show a specific share named “share1”

   +-----------------------------------------------------------------------+
   | net  conf show share1                                                 |
   +-----------------------------------------------------------------------+

   .. rubric:: 3.7 - CONFIGURING CEPHFS WITH NFS GANESHA
      :name: CephNautilusInstallationGuide.xhtml#h.wz1bpzsb594w
      :class: c17 c25

   .. rubric:: 3.7.1 - Prerequisites
      :name: CephNautilusInstallationGuide.xhtml#h.sbxtzkv2mb65
      :class: c9

   -  An Ansible deployed ceph cluster
   -  Ceph File-System created, called “cephfs” for this example
   -  Node(s) to act as NFS Gateway

   -  NFS Gateways can be physical hardware or virtual machines
   -  Password-less SSH access from ansible node

   .. rubric:: 3.7.2 - Active-Active Configuration
      :name: CephNautilusInstallationGuide.xhtml#h.wyeo31rj629v
      :class: c9

   Active-Active NFS

   -  No floating IP. Shares accessible from every gateway IP​.
   -  HA only possible if application can multipath.
   -  Useful for highly concurrent use cases.

   First thing to do is edit the / usr/share
   /ceph-ansible/group_vars/nfss.yml  file.
   NFS Ganesha can be setup on top of Filesystem or Object, so you need
   to specify in the file:

   +-----------------------------------------------------------------------+
   | nfs_file_gw: true                                                     |
   | nfs_obj_gw: false                                                     |
   +-----------------------------------------------------------------------+

   Set the backend driver to “rados_cluster” in
   /usr/share/ceph-ansible/group_vars/nfss.yml .

   +-----------------------------------------------------------------------+
   | # backend mode , either rados_kv,rados_ng, or  rados_cluster          |
   | # Default (rados_ng) is   for  single gateway/active-passive use.     |
   |                                                                       |
   | # rados_kv is  obsoleted by  rados_ng                                 |
   | # rados_cluster is   for  active-active nfs cluster .                 |
   |                                                                       |
   | # Requires ganesha-grace-db to be  initialized                        |
   | ceph_nfs_rados_backend_driver: "rados_cluster"                        |
   +-----------------------------------------------------------------------+

   Now add the NFS Gateway hostnames to the /root/ceph-ansible-45d/hosts
    file

   +-----------------------------------------------------------------------+
   | [nfss]                                                                |
   | cephNFS1                                                              |
   | cephNFS2                                                              |
   +-----------------------------------------------------------------------+

   Next run the nfs.yml playbook:  

   +-----------------------------------------------------------------------+
   | [root @cephADMIN  ceph-ansible] # ansible-playbook nfs.yml            |
   +-----------------------------------------------------------------------+

   This playbook will install all necessary packages as well as setup
   the default export.

   Setting up all of your exports can be done from the dashboard which
   will be setup in the next section.

   .. rubric:: 3.7.3 - Active-Passive Configuration
      :name: CephNautilusInstallationGuide.xhtml#h.x2sjzlt2xcbd
      :class: c9

   Active-Passive

   -  Floating IP. Service only running on 1 of the gateways at a time.​
   -  HA possible for all clients

   First thing to do is edit the
   /usr/share/ceph-ansible/group_vars/nfss.yml  file.
   NFS Ganesha can be setup on top of Filesystem or Object, so you need
   to specify in the file:

   +-----------------------------------------------------------------------+
   | nfs_file_gw: true                                                     |
   | nfs_obj_gw: false                                                     |
   +-----------------------------------------------------------------------+

   Set the backend driver to “rados_ng” in
   /usr/share/ceph-ansible/group_vars/nfss.yml .

   +-----------------------------------------------------------------------+
   | # backend mode , either rados_kv,rados_ng, or  rados_cluster          |
   | # Default (rados_ng) is   for  single gateway/active-passive use.     |
   |                                                                       |
   | # rados_kv is  obsoleted by  rados_ng                                 |
   | # rados_cluster is   for  active-active nfs cluster .                 |
   |                                                                       |
   | # Requires ganesha-grace-db to be  initialized                        |
   | ceph_nfs_rados_backend_driver: "rados_ng"                             |
   +-----------------------------------------------------------------------+

   Specify the floating IP the NFS-Ganesha Gateway will be reachable
   from. in /usr/share/ceph-ansible/group_vars/nfss.yml .

   +-----------------------------------------------------------------------+
   | ceph_nfs_floating_ip_address:   '192.168.18.73'                       |
   | ceph_nfs_floating_ip_cidr:   '16'                                     |
   +-----------------------------------------------------------------------+

   Now add the NFS Gateway hostnames to the
   /usr/share/ceph-ansible/hosts  file

   +-----------------------------------------------------------------------+
   | [nfss]                                                                |
   | cephNFS1                                                              |
   | cephNFS2                                                              |
   +-----------------------------------------------------------------------+

   Next run the nfs.yml playbook:

   +-----------------------------------------------------------------------+
   | [root @cephADMIN  ceph-ansible] # ansible-playbook nfs.yml            |
   +-----------------------------------------------------------------------+

   This playbook will install all necessary packages as well as setup
   the default export.

   Setting up all of your exports can be done from the Ceph dashboard.

   Set the following ceph configuration setting to allow nfs to failover
   properly.

   +-----------------------------------------------------------------------+
   | [root @cephADMIN  ceph-ansible] # ceph config set mds                 |
   | mds_cap_revoke_eviction_timeout 10                                    |
   +-----------------------------------------------------------------------+

   .. rubric:: 3.7 - CONFIGURING RBD + iSCSI
      :name: CephNautilusInstallationGuide.xhtml#h.htd9of2wxfyi
      :class: c25 c17

   .. rubric:: 3.7.1 Prerequisites
      :name: CephNautilusInstallationGuide.xhtml#h.lzr4dv49oqmd
      :class: c9

   -  An Ansible deployed ceph cluster
   -  Node(s) to act as iSCSI Gateway

   -  iSCSI Gateways can be physical hardware or virtual machines.
   -  iSCSi Gateways can be co-located on the OSDs nodes.
   -  Password-less SSH access from the ansible node.

   .. rubric:: 3.7.2 Ceph iSCSI Installation
      :name: CephNautilusInstallationGuide.xhtml#h.tmfdp4k0cidm
      :class: c9

   See Knowledge Base article for more detail. `Ceph iSCSI
   Configuration <https://www.google.com/url?q=http://knowledgebase.45drives.com/kb/kb450229-setup-and-configuration-of-iscsi-gateways-on-ceph-cluster/&sa=D&ust=1605552701036000&usg=AOvVaw3n0TbvnTaE737Z4N5dKWzw>`__

    

   Add iSCSI gateways hostnames to /usr/share/ceph-ansible/hosts

   +-----------------------------------------------------------------------+
   | [iscsigws]                                                            |
   | iscs i1                                                               |
   | iscs i2                                                               |
   | iscs i3                                                               |
   +-----------------------------------------------------------------------+

   Next run the iscsi.yml playbook                           

   +-----------------------------------------------------------------------+
   | [root @cephADMIN  ceph-ansible] # ansible-playbook iscsi.yml          |
   +-----------------------------------------------------------------------+

   .. rubric:: 3.7.3 Ceph iSCSI Configuration
      :name: CephNautilusInstallationGuide.xhtml#h.jmswyqzi4q7s
      :class: c9

   Configuration on the iSCSI nodes is to be done on the iSCSI gateways
   and the ceph dashboard.

   From one of the iSCSI nodes, create the initial iSCSI gateways with
   gwcli . Note the first time gwcli is run you will be promoted with
   the warning below, it can be ignored as gwcli will create an initial
   preferences file if not present.

   +-----------------------------------------------------------------------+
   | [root@iscsi1 ~] # gwcli                                               |
   | Warning: Could not  load preferences file /root/ .gwcli/prefs.bin.    |
   | >                                                                     |
   +-----------------------------------------------------------------------+

   Create iSCSI target of for the cluster

   +-----------------------------------------------------------------------+
   | [root@iscsi1 ~]# gwcli                                                |
   | >  /> cd  /iscsi-target                                               |
   | >  /iscsi-target>  create iqn.2003-01.com.45drives.iscsi-gw:iscsi-igw |
   +-----------------------------------------------------------------------+

   Create the first iSCSI gateway. It has to be the node you are running
   this command on.

   +-----------------------------------------------------------------------+
   | [root@iscsi1 ~]# gwcli                                                |
   | > cd                                                                  |
   | /iscsi-targets/iqn.2003-01.com.45drives.iscsi-gw:iscsi-igw/gateways   |
   | /iscsi-target.. .7283 /gateways> create iscsi1 .45 lab.com 192.168    |
   | .*.\*                                                                 |
   +-----------------------------------------------------------------------+

    

   The Ceph Administration dashboard is recommended to finish iSCSI
   configuration. See Section 5 before proceeding here.

   .. rubric:: CHAPTER 4 - EXPANDING THE CLUSTER
      :name: CephNautilusInstallationGuide.xhtml#h.uesscvhg2tr1
      :class: c14

   .. rubric:: CHAPTER 5 - CONFIGURING THE MANAGEMENT DASHBOARDS
      :name: CephNautilusInstallationGuide.xhtml#h.wmugvvtnp674
      :class: c14

   .. rubric:: 5.1 Installing Ceph Dashboard
      :name: CephNautilusInstallationGuide.xhtml#h.29mw0peeh0rp
      :class: c25 c17

   Using Ansible, the steps below will be install and configure the
   metric collection/alert stack.This will also configure and start the
   ceph management UI.

   By default the metric stack will be installed to the first node
   running the manager service in your cluster. Optionally to specify
   another server to host this stack use the group label “metrics”

   +-----------------------------------------------------------------------+
   | [metrics]                                                             |
   | metric1                                                               |
   +-----------------------------------------------------------------------+

   The Ceph Dashboard is hosted by ceph-mgr service. The dashboard
   playbook will also install haproxy on the metric server, this way the
   dashboard will be reachable from any of the nodes running the
   ceph-mgr service as well as the metric server itself.

   Enable/disable, set port, protocol, and cert in group_vars/all.yml

   +-----------------------------------------------------------------------+
   | dashboard_enabled: true                                               |
   | # When true HAProxy will be installed on the server in the metric     |
   | group                                                                 |
   | dashboard_haproxy: true                                               |
   | dashboard_haproxy_port: 80                                            |
   | dashboard_haproxy_protocol: http                                      |
   | dashboard_haproxy_cert:                                               |
   +-----------------------------------------------------------------------+

   Run the /usr/share/ceph-ansible/dashboard.yml  file:

   +-----------------------------------------------------------------------+
   | [root @cephADMIN  ceph-ansible] # ansible-playbook dashboard.yml      |
   +-----------------------------------------------------------------------+

   Below is a table of the default ports for the dashboards that were
   configured. These can be modified in  
   /usr/share/ceph-ansible/group_vars/all.yml  file

   +-----------------------------------+-----------------------------------+
   | Name                              | Default Port                      |
   +-----------------------------------+-----------------------------------+
   | Grafana                           | 3000/tcp                          |
   +-----------------------------------+-----------------------------------+
   | Prometheus                        | 9090/tcp                          |
   +-----------------------------------+-----------------------------------+
   | Alertmanager                      | 9091/tcp                          |
   +-----------------------------------+-----------------------------------+
   | Ceph Dashboard                    | 8234/tcp                          |
   +-----------------------------------+-----------------------------------+

   --------------

   .. rubric:: CHAPTER 6 - MANAGING STORAGE POOLS VIA CLI
      :name: CephNautilusInstallationGuide.xhtml#h.wocog8t0kct3
      :class: c14

   It is recommended to create storage pools in the Ceph Dashboard . The
   below chapter will go into detail on the specifics of creating pool.

   Before creating pools, there are a few things to consider. First
   thing is the number of placement groups. Second being what type of
   pool is to be created - replicated or erasure coded.

   .. rubric:: 6 .1 - Placement Groups
      :name: CephNautilusInstallationGuide.xhtml#h.plhdyskelh3r
      :class: c25 c17

   Sizing placement groups is very important. You can always increase
   the size of placement groups later but never decrease it. Increasing
   the number of placement groups will cause the data to begin migrating
   to be evenly spread across all placement groups. This will put a
   strain on cluster performance until the migration is complete.

   It is best to use the
   `pg_calculator <https://www.google.com/url?q=https://ceph.com/pgcalc/&sa=D&ust=1605552701057000&usg=AOvVaw12FQlsiwFpWiF4_HAudV85>`__
    to have the proper number of placement groups. If you’re unsure what
   to choose, start with 64 placement groups per pool, and then increase
   the number of placement groups at a later date (ideally before you
   put data on the pool).

   A quick rule of thumb:

   -  Less than 5 OSDs, set pg_num to 128
   -  Between 5 and 10 OSDs, set pg_num to 512
   -  Between 10 and 50 OSDs, set pg_num to 1024
   -  If you have more than 50 OSDs, understand the tradeoffs and use
      the calculator

   .. rubric:: 6 .2 - Pool Types
      :name: CephNautilusInstallationGuide.xhtml#h.bvcubibe3ys2
      :class: c25 c17

   Ceph stores data in pools and there are two types of pools:

   -  Replicated
   -  Erasure-coded

   Ceph uses the replicated pools by default, meaning the Ceph copies
   every object from a primary OSD node to one or more secondary OSDs.
   Erasure coding is a method of storing an object where the erasure
   code algorithm breaks the object into data chunks ( k ) and coding
   chunks ( m ), and stores those chunks in different OSDs.
   Erasure coding uses storage capacity more efficiently than
   replication. The n-replication approach maintains  n  copies of an
   object (3x by default in Ceph), whereas erasure coding maintains only
    k + m  chunks. For example, 3 data and 2 coding chunks use 1.5x the
   storage space of the original object.

   Below is a table showing pool type, required number of OSD nodes, and
   storage efficiency.

   +-----------------+-----------------+-----------------+-----------------+
   | Pool Type       | Storage         | Minimum # of    | Recommended #   |
   |                 | Efficiency      | OSD Nodes       | of OSD Nodes    |
   +-----------------+-----------------+-----------------+-----------------+
   | 2-replication   | 50%             | 3               | 3+              |
   +-----------------+-----------------+-----------------+-----------------+
   | 3-replication   | 33%             | 3               | 3+              |
   +-----------------+-----------------+-----------------+-----------------+
   | 2+1 Erasure     | 66%             | 4               | 5               |
   | Coded           |                 |                 |                 |
   +-----------------+-----------------+-----------------+-----------------+
   | 4+2 Erasure     | 66%             | 8               | 10              |
   | Coded           |                 |                 |                 |
   +-----------------+-----------------+-----------------+-----------------+
   | 8+2 Erasure     | 80%             | 12              | 14              |
   | Coded           |                 |                 |                 |
   +-----------------+-----------------+-----------------+-----------------+
   | 8+4 Erasure     | 66%             | 16              | 20              |
   | Coded           |                 |                 |                 |
   +-----------------+-----------------+-----------------+-----------------+

   \* NOTE  - Minimum # of OSD  Nodes can withstand ‘m’ number of
   failures, after that I/O will stop until you recover that OSD node.
   The Recommended # of OSD  node gives that extra cushion of protection
   and keeps  I/O going while you recover the failed OSD node.  

   .. rubric:: 6 .3 - Creating a Pool
      :name: CephNautilusInstallationGuide.xhtml#h.begwgjwbw13w
      :class: c25 c17

   Below is the syntax required for creating a ceph pool:

   +-----------------------------------------------------------------------+
   | ceph osd  pool create {pool-name} {pg-num} [{pgp-num}] [replicated]   |
   | [crush-ruleset-name]                                                  |
   | ceph osd  pool create {pool-name} {pg-num} {pgp-num} erasure          |
   | [erasure-code-profile]                                                |
   +-----------------------------------------------------------------------+

   A few things to note:

   +-------------+-------------+-------------+-------------+-------------+
   | Variable    | Description | Type        | Required?   | Default     |
   |             |             |             |             | Value       |
   +-------------+-------------+-------------+-------------+-------------+
   | pool-name   | Name of the | String      | Yes         |             |
   |             | pool.  Must |             |             |             |
   |             | be unique.  |             |             |             |
   +-------------+-------------+-------------+-------------+-------------+
   | pg-num      | Total       | Integer     | Yes         | 8           |
   |             | number of   |             |             |             |
   |             | placement   |             |             |             |
   |             | groups.     |             |             |             |
   +-------------+-------------+-------------+-------------+-------------+
   | pgp-num     | Total       | Integer     | Yes         | 8           |
   |             | number of   |             |             |             |
   |             | placement   |             |             |             |
   |             | groups for  |             |             |             |
   |             | placement   |             |             |             |
   |             | purposes.   |             |             |             |
   |             | pg-num=pgp- |             |             |             |
   |             | num         |             |             |             |
   |             |             |             |             |             |
   +-------------+-------------+-------------+-------------+-------------+
   | replicated| | Pool type.  | String      | No          | replicated  |
   | erasure     | Replication |             |             |             |
   |             | level will  |             |             |             |
   |             | be set      |             |             |             |
   |             | later,      |             |             |             |
   |             | erasure-cod |             |             |             |
   |             | e           |             |             |             |
   |             | profile     |             |             |             |
   |             | needs to be |             |             |             |
   |             | defined at  |             |             |             |
   |             | time of     |             |             |             |
   |             | pool        |             |             |             |
   |             | creation.   |             |             |             |
   +-------------+-------------+-------------+-------------+-------------+
   | crush-rules | Name  of a  | String      | No          | For         |
   | et-name     | CRUSH       |             |             | replicated  |
   |             | ruleset to  |             |             | pools it is |
   |             | use for     |             |             | the ruleset |
   |             | this pool.  |             |             | specified   |
   |             | Ruleset     |             |             | by the osd  |
   |             | must exist. |             |             | pool        |
   |             |             |             |             | default     |
   |             |             |             |             | crush       |
   |             |             |             |             | replicated  |
   |             |             |             |             | ruleset     |
   |             |             |             |             |  config     |
   |             |             |             |             | variable.   |
   |             |             |             |             | This        |
   |             |             |             |             | ruleset     |
   |             |             |             |             | must exist. |
   |             |             |             |             | For erasure |
   |             |             |             |             | pools it is |
   |             |             |             |             | erasure-cod |
   |             |             |             |             | e           |
   |             |             |             |             | if the      |
   |             |             |             |             | default     |
   |             |             |             |             | erasure     |
   |             |             |             |             | code        |
   |             |             |             |             | profile is  |
   |             |             |             |             | used or     |
   |             |             |             |             | {pool-name} |
   |             |             |             |             | otherwise.  |
   |             |             |             |             | This        |
   |             |             |             |             | ruleset     |
   |             |             |             |             | will be     |
   |             |             |             |             | created     |
   |             |             |             |             | implicitly  |
   |             |             |             |             | if it       |
   |             |             |             |             | doesn’t     |
   |             |             |             |             | already     |
   |             |             |             |             | exist.      |
   +-------------+-------------+-------------+-------------+-------------+
   | erasure-cod | It must be  | String      | No          |             |
   | e-profile   | an existing |             |             |             |
   |             | profile as  |             |             |             |
   |             | defined by  |             |             |             |
   |             |  osd        |             |             |             |
   |             | erasure-cod |             |             |             |
   |             | e-profile   |             |             |             |
   |             | set .       |             |             |             |
   +-------------+-------------+-------------+-------------+-------------+
   | expected-nu | The         | Integer     | No          | 0           |
   | m-objects   | expected    |             |             |             |
   |             | number of   |             |             |             |
   |             | objects for |             |             |             |
   |             | this pool.  |             |             |             |
   +-------------+-------------+-------------+-------------+-------------+

   Example:  This corresponds to a cluster with 120 OSDs, a replicated
   pool.

   +-----------------------------------------------------------------------+
   | ceph osd  pool create tank_data 8192 8192 replicated                  |
   | ceph osd  pool create tank_metadata 256 256 replicated                |
   +-----------------------------------------------------------------------+

   .. rubric:: CHAPTER 7 - UPGRADING A CEPH CLUSTER
      :name: CephNautilusInstallationGuide.xhtml#h.296selaq9wjm
      :class: c14

   There are two  types of updates when it comes to a Ceph cluster.

   #. Minor Updates
   #. Major Updates

   Both types can be completed without cluster downtime, but release
   notes should be reviewed in both cases.

   .. rubric:: 7.1 - MINOR UPDATES
      :name: CephNautilusInstallationGuide.xhtml#h.f9erf672l6hd
      :class: c25 c17

   Minor updates are minor bug fixes released every 4-6 months. These
   are quick updates that can be done safely by simply running a yum
   update .

   If a new kernel is installed, a reboot will be required to take
   effect. If there is no kernel update you can stop here.

   If there is a new kernel, set osd flag noout  and norebalance  to
   prevent the cluster from trying to heal itself while the nodes reboot
   one by one.

   +-----------------------------------------------------------------------+
   | ceph osd set  flag noout                                              |
   | ceph osd set  flag norebalance                                        |
   +-----------------------------------------------------------------------+

   Then reboot each node one at a time. Do not reboot the next node
   until the prior is up and back in the cluster. After each node is
   rebooted, unset the flags set earlier when you’re all done.

   +-----------------------------------------------------------------------+
   | ceph osd unset  flag noout                                            |
   | ceph osd unset  flag norebalance                                      |
   +-----------------------------------------------------------------------+

   --------------

   .. rubric:: 
      :name: CephNautilusInstallationGuide.xhtml#h.mt41h57xam2t
      :class: c25 c17 c38

   .. rubric:: 7.2 - MAJOR UPDATES
      :name: CephNautilusInstallationGuide.xhtml#h.snlki1u3zz38
      :class: c25 c17

   Major updates are applied with ansible. To upgrade to the next major
   release edit the group_vars/all.yml  in the ceph-ansible-45d
   directory. In the INSTALL  heading, find the line ceph_stable_release
   , replace the existing release with the next stable version.
   For example:  updating from Mimic (13.2.X) to Nautilus (14.2.X)

   +-----------------------------------------------------------------------+
   | [root@cephADMIN ~]# vim /root/ceph-ansible-45d-1.2/group_vars/all.yml |
   | >  Change "ceph_stable_release: mimic"                                |
   | >  To     "ceph_stable_release: nautilus"                             |
   +-----------------------------------------------------------------------+

   Now, run the rolling-updates.yml  playbook.

   +-----------------------------------------------------------------------+
   | [root @cephADMIN  ceph-ansible -45 d -1.2 ] # ansible-playbook        |
   | infrastructure-playbooks/rolling-updates.yml                          |
   +-----------------------------------------------------------------------+

   It will take some time, but all data is up and accessible during the
   update.
   You can verify all nodes are running the new version by running the
   following command:

   +-----------------------------------------------------------------------+
   | [root @cephADMIN  ~] # ceph versions                                  |
   +-----------------------------------------------------------------------+

   --------------

   .. container::

      `[1] <#CephNautilusInstallationGuide.xhtml#ftnt_ref1>`__  This
      port is user specified.  It defaults to 8080
