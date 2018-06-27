# Nutanix Provisioner

Use the following command on a RHEL host to generate a SHA-512 hashed password to be cloud_init_root_pass used with the `kvm` RHEL image.

`python -c 'import crypt,getpass; print crypt.crypt(getpass.getpass())'`

Set the resulting string equal to `cloud_init_root_pass` in `group_vars/*/all.yaml`.

## Ansible Host Prep
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

## SSH key prep

From your bastion node (or the node you wish to execute ansible from)  
First generate an ssh key pair
```
# ssh-keygen
```
```
# for host in master.example.com \
    node1.example.com \
    node2.example.com; \
    do ssh-copy-id -i ~/.ssh/id_rsa.pub $host; \
    done
```


## Encrypting secrets:

Single variable encryption:
```
ansible-vault encrypt_string <string> --ask-vault-pass

```
Single variable encyption, reading input from stdin (SSH key/etc):

```
ansible-vault encrypt_string --stdin-name 'ansible_ssh_private_key'
```

Note: Use same vault password for all variables, or specify --vault-id to label
different variables with groups of passwords.
