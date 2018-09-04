Lab deployer
------------------
## High level Order of Operations
A. Deploy to external lab
- Provision an Ansible core control/bastion node
- Import Ansible roles / playbooks as necessary
- Verify DNS entries are available
- Deploy Ansible Tower (remaining tasks deploy from Tower)
- Provision all OCP instances (don't configure, they need to just be provisioned for the benefit of the load balancer deployer role)
- Deploy all 4 load balancers
- Verify DNS entries resolve correctly
- Deploy Quay
- Deploy OpenShift with CNS
- Run integration code to configure Quay with OCP deployment
- Deploy integrated Open Innovation Labs CI/CD tools (Gitlab, Nexus, Jenkins, example project)
- Collect and export all required images, RPM's, and source code

B. Deploy to internal lab
- Provision an Ansible core control/bastion node
- Upload all images, RPM's and source code to Ansible core VM
- Import Ansible roles / playbooks as necessary
- Deploy Ansible Tower (remaining tasks deploy from Tower)
- Provision all 3 Masters
- Deploy all 4 load balancers
- Deploy Quay
- Deploy OpenShift with CNS
- Deploy integrated Open Innovation Labs CI/CD tools (Gitlab, Nexus, Jenkins, example project)



## Misc. Operations

### RHEL KVM Disk Image Resize
The default RHEL KVM cloud image has a root disk size of 10G. To establish larger sizes the qcow2 image virtual size must be adjusted before uploading to the Nutanix cluster. 

Example:

Resize root size for qcow2 image to 76G:

```bash
qemu-img resize rhel-server-7.5-update-1-x86_64-kvm.qcow2 +65G
```

Check qcow2 image:

```bash
qemu-img info rhel-server-7.5-update-1-x86_64-kvm.qcow2
```

### Hash the password for cloud-config (optional, this can be left blank)

Use the following command on a RHEL host to generate a SHA-512 hashed password to be cloud_init_root_pass used with the `kvm` RHEL image.

`python -c 'import crypt,getpass; print crypt.crypt(getpass.getpass())'`

Set the resulting string equal to `cloud_init_root_pass` in `group_vars/*/all.yaml`.

### Ansible Core Host Prep
[Refer to OpenShift host prep documentation here](https://docs.openshift.com/container-platform/3.9/install_config/install/host_preparation.html "OpenShift Documentation")


```
# subscription-manager register --username=<user_name> --password=<password>
# subscription-manager refresh
# subscription-manager list --available --matches '*OpenShift*'
# POOLID=$(/usr/bin/subscription-manager list --all --available --matches="*OpenShift Container*" | awk '/Pool ID/ {print $3}' | head -1)
# subscription-manager attach --pool=$POOLID
# subscription-manager repos --disable="*"
# subscription-manager repos \
    --enable="rhel-7-server-rpms" \
    --enable="rhel-7-server-extras-rpms" \
    --enable="rhel-7-server-ose-3.9-rpms" \
    --enable="rhel-7-fast-datapath-rpms" \
    --enable="rhel-7-server-ansible-2.4-rpms"
# yum install wget git net-tools bind-utils yum-utils iptables-services bridge-utils bash-completion kexec-tools sos psacct
# yum update
# systemctl reboot
# yum install atomic-openshift-utils
```

### SSH key prep

From your bastion node (or the node you wish to execute ansible from)  
First generate an ssh key pair
```
# ssh-keygen -f <location>/<keyname>
```

This will generate a public and private keypair. The ansible scripts expect the public/private key used for all provisioned VMs to be in `inventories/group_vars/*/all.yml` under the variable names: `ansible_ssh_public_key` and `ansible_ssh_private_key` (Note: see below on how to encrypt the private key)

In addition, many post-provisioning playbooks will need access to the private key for ssh connections. See the `ansible.cfg` file for the specific filename and location of this key.


### Encrypting secrets:

Single variable encryption:

```bash
ansible-vault encrypt_string <string> --ask-vault-pass
```

Single variable encyption, reading input from stdin (useful for SSH key or pasting large text sections):
```
ansible-vault encrypt_string --stdin-name 'ansible_ssh_private_key'
```

Single variable decryption
```
ansible my_server -m debug -a 'var=my_encrypted_var'
```

Note: Use same vault password for all variables, or specify --vault-id to label
different variables with groups of passwords.
