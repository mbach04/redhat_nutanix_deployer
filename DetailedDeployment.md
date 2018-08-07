# Detailed Deployment Procedure

## Initial Setup

- Check for correct DNS entries for all hosts (see `inventories/*/group_vars/all.yml`)

## Deploy to Dell lab

### Provision an Ansible core control/bastion node
Automated Path:

Prerequisites:
Linux OS with Ansible installed
Proper SSH Private key for ansible user
Linux Machine connected to Dell VPN and can access Nutanix cluster

Run the `deployer_bastion.yml` playbook to provision a 'bastion' host to run future provisioning playbooks. All future steps are assumed to take place on the bastion host.

Command:
```bash
ansible-playbook -i inventories/dell_lab/ deployer_bastion.yml
```

Manual Path:
Connection to Dell VPN and can access Nutanix cluster WebUI

- TODO

### Provision and Deploy Repository Server
This server acts as a centralized repository for RPMs, extra binaries, and Docker Images.
See the `deploy_repository.yml` playbook and the README in the `repository` role for more
details.

```bash
ansible-playbook -i inventories/dell_lab/ deployer_repository.yml
```

### Provision and Deploy Ansible Tower Servers
Provisions a HA Ansible Tower cluster of 3 tower nodes and a database node.

```bash
ansible-playbook -i inventories/dell_lab/ deployer_tower.yml
```

### Provision all OCP instances 

### Provision and Deploy all 4 Load Balancers (OCP Master/OCP Application)

### Provision and  Deploy Quay

### Deploy OpenShift with CNS

### Run integration code to configure Quay with OCP deployment

### Deploy integrated Open Innovation Labs CI/CD tools (Gitlab, Nexus, Jenkins, example project)

### Deploy COTS application in OCP to verify CI/CD pipeline and OCP deployment

