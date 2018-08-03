Role Name
=========

This role will deploy Ansible Tower in HA clustered mode
This mode consists of 3 Ansible Tower nodes and a Database node (PostgreSQL)

Requirements
------------

Tower and database nodes must exist and be defined in the inventory file. This role expects a minimal RHEL 7.5 installation
This role also requires a valid license and associated information so apply to the Ansible Tower installation.

All tower_license_* variables are expected to be customized when running this role.

Role Variables
--------------

#User to use for downloading/installing ansible tower
tower_install_user: "ansible"

#Version of ansible tower
tower_binary_version: "3.2.5-1"

#Folder name of the extracted ansible tower bundle tarball
tower_binary_folder: "ansible-tower-setup-bundle-{{ tower_binary_version }}.el7"

#File name of the ansible tower tarball
tower_binary_name: "{{ tower_binary_folder }}.tar.gz"

#Remote location from which to download ansible tower tarball
tower_binary_url: "https://releases.ansible.com/ansible-tower/setup-bundle/{{ tower_binary_name }}"

#Folder to download tarball, extract, and perform installation
tower_binary_dir: "/home/{{ tower_install_user }}"

#Agree to the EULA in the license file
tower_license_eula: "true"

#Company name for the license
tower_license_company_name: "Spathe Systems (SOCOM J6)"

#Contact email concerning license files
tower_license_contact_email: "tling@redhat.com"

#Contact name concerning license files
tower_license_contact_name: "Timothy Ling"

#Number of nodes license allows for management from tower
tower_license_instance_count: 100

#Date of license
tower_license_date: 1538753991

#License Key
tower_license_key: ""

#Type of license
tower_license_type: "enterprise"

#If license is a trial or not
tower_license_trial: "true"

#Ansible Tower admin username
tower_admin_user: "admin"

#Ansible Tower initial admin password
tower_admin_password: "redhat"

#Ansible tower postgres database name
tower_pg_database: "awx"

#Ansible tower postgres port
tower_pg_port: "5432"

#Ansible tower postgres username
tower_pg_user: "awx"

#Ansible tower postgres password
tower_pg_password: "redhat"

#Ansible tower rabbit MQ username
tower_rabbitmq_user: "tower"

#Ansible tower rabbit MQ password
tower_rabbitmq_password: "redhat"

#Ansible tower rabbit MQ port
tower_rabbitmq_port: '5672'

#Ansible tower rabbit MQ cookie
tower_rabbitmq_cookie: 'cookiemonster'


#List of packages to install to support Ansible Tower
tower_packages:
  - ansible


Dependencies
------------

N/A

Example Playbook
----------------

#Deploy and Configure Tower
- name: Deploy Ansible Tower
  hosts: tower
  remote_user: ansible
  become: no
  tasks:
    - name: Use role to deploy/config ansible tower cluster
      include_role:
        name: tower_cluster

