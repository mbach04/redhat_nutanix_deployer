# Nutanix Provisioner




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
