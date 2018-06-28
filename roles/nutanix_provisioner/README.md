Nutanix VM Provisioner
=========

A basic Ansible role to provision virtual machines on a Nutanix AHV using APIv3.

Requirements
------------

Use the following command on a RHEL host to generate a SHA-512 hashed password to be cloud_init_root_pass used with the `kvm` RHEL image.

`python -c 'import crypt,getpass; print crypt.crypt(getpass.getpass())'`

Set the resulting string equal to `cloud_init_root_pass` in `group_vars/*/all.yaml`.

Role Variables
--------------
TODO

A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well.

Dependencies
------------
TODO

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------
TODO

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }

License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
