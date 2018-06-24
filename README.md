# Nutanix Provisioner

Use the following command on a RHEL host to generate a SHA-512 hashed password to be cloud_init_root_pass used with the `kvm` RHEL image.

`python -c 'import crypt,getpass; print crypt.crypt(getpass.getpass())'`

Set the resulting string equal to `cloud_init_root_pass` in `group_vars/*/all.yaml`.


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
