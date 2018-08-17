
Role Name
=========

This role configures a RPM repository, Docker registry, and generic Binary httpd hosting to support installing Quay, Ansible Tower, and OCP

Requirements
------------

Authentication and proper licenses for Quay, Ansible Tower, and OCP

Role Variables
--------------

#Variables to enable/disable groups of tasks
#Enable/disable setup and config of subscription manager
repo_config_subscriptionmanager: true
#Enable/disable setup of mirroing repositories
repo_config_reposync: true
#Enable/disable setup of custom binary hosting
repo_config_binaries: true
#Enable/disable setup and activation of httpd server for rpms/binaries
repo_config_httpd_setup: true
#Enable/disable setup and config of docker registry
repo_config_docker_registry: true
#Enable/disalbe export of docker registry hosted images to local filesystem
repo_config_docker_archive: true

#Define block device dedicated to repository storage
repo_disk_dev: "/dev/sdb"
#Set partition number for formatting repository storage block device
repo_disk_partition_num: 1
#Define filesystem type for dedicated repository storage
repo_disk_fstype: "xfs"

#Set base directory for repository storage
repo_dir_base: "/repos"

#Set directory for storage of RPMs
repo_dir_yum: "{{ repo_dir_base }}/yum"
#Set directory for storage of docker images/registry
repo_dir_docker: "{{ repo_dir_base }}/docker"
#Set directory for storage of generic binaries
repo_dir_binaries: "{{ repo_dir_base }}/binaries"

#Set remote url source for EPEL repository
repo_epel_base_url: "https://dl.fedoraproject.org/pub/epel"

#Red Hat Subscription manager username
repo_rhsm_user: ""
#Red Hat Subscription manager password
repo_rhsm_password: ""

#List of extra binaraies to download and host
repo_binaries_download_list:
  - "https://releases.ansible.com/ansible-tower/setup-bundle/ansible-tower-setup-bundle-3.2.5-1.el7.tar.gz"


#List of RHEL repositories to enable and reposync
repo_enabled_repositories:
  - rhel-7-server-rpms
  - rhel-7-server-extras-rpms
  - rhel-7-fast-datapath-rpms
  - rhel-7-server-ansible-2.5-rpms
  - rhel-7-server-ose-3.9-rpms

#List of non RHEL repositories to reposync
repo_enabled_repositories_nonrhel:
  - epel

#Base prerequisite packages needed to be installed
repo_packages:
  - docker
  - yum-utils
  - createrepo
  - git
  - ansible
  - httpd

#File for docker configuration
repo_docker_config_path: "/etc/docker/daemon.json"

#List of OCP images that will be hosted in the docker registry
repo_openshift_images: []

#List of Quay images that will be hosted in the docker registry
repo_quay_coreos_images: []

#List of Nexus images that will be hosted in the docker registry
repo_nexus_images: []

Dependencies
------------

N/A

Example Playbook
----------------

# Configure the Repository VM
- name: YUM Nutanix Configuration
  hosts: repository
  remote_user: ansible
  become: yes
  vars_prompt:
    - name: "rhsm_username"
      prompt: "RHSM Username"
    - name: "rhsm_password"
      prompt: "RHSM Password"

  tasks:
    - name: Configure using the repository role
      include_role:
        name: repository
      vars:
        repo_rhsm_user: "{{ rhsm_username }}"
        repo_rhsm_password: "{{ rhsm_password }}"

