# Detailed Deployment Procedure

## Initial Setup

- Check for correct DNS entries for all hosts (see `inventories/*/group_vars/all.yml`)
   - Forward/Reverse entry for each node
   - Entries pointing to the loadbalancer VIPs (ocp masters, ansible towers, etc)
   - Wildcard entry for OCP applications pointing to ocp infrastructure loabalancer VIP

- Nutanix cluster has proper Network configured with routing and DNS capability
- Nutanix cluster has a RHEL Image for use in provisioning VMs

- Customize configuration in the `inventories/*` folder to target a specific environment (Dell Lab, SIF, etc)

## Deploy 

### Provision an Ansible core control/bastion node
Automated Path:

Prerequisites:
Linux OS with Ansible installed
Proper SSH Private key for ansible user
Linux Machine that can access Nutanix cluster

Run the `deployer_bastion.yml` playbook to provision a 'bastion' host to run future provisioning playbooks. All future steps are assumed to take place on the bastion host.

Command:
```bash
ansible-playbook -i inventories/sif_lab/ deployer_bastion.yml
```

Manual Path:

- Create a VM within the Nutanix WebUI with the following configuration:
    2 vCPU
    2048 GB RAM
    75 GB Root Disk

- Transfer the `nutanix_automation` repository to the ansible bastion server via SCP


### Provision and Deploy Repository Server
This server acts as a centralized repository for RPMs, extra binaries, and Docker Images.
See the `deploy_repository.yml` playbook and the README in the `repository` role for more
details.

Automated Provisioning:

```bash
ansible-playbook -i inventories/sif_lab/ deployer_repository.yml
```


Offline Provisioning:
- Create a VM within the Nutanix WebUI with the following configuration:
    2 vCPU
    4096 GB RAM
    75 GB  / Root Disk
    150 GB /repos Disk (Repository storage)
    100 GB /var/lib/dock Disk (Docker storage) 


### Provision and Deploy Loadbalancer servers
Provisions 2 clusters of Highly Available HAProxy servers
One cluster primarly loadbalances across the OCP master servers for Web console access
One cluster primarly loadbalances accross the OCP infrasturcture servers for OCP application loadbalancing

Prerequisites: 
Ensure the following files are present in the root directory of the Ansible playbooks:
  .vaultpass - This file contains the password to unlock the Ansible vault
  .keyfile - This file contains the private SSH key used by the 'ansible' user to log into the created nodes

```bash
ansible-playbook -i inventories/sif_lab deployer_loadbalancers.yml
```

### Provision and Deploy Ansible Tower Servers
Provisions a HA Ansible Tower cluster of 3 tower nodes and a database node.

```bash
ansible-playbook -i inventories/sif_lab/ deployer_tower.yml
```

### Provision all OCP instances 

Provision OCP VMs:

``` bash
ansible-playbook -i inventories/sif_lab/ deployer_ocp.yml
```

### Deploy OpenShift with CNS

Install openshift ansible playbooks:

```bash
sudo yum install openshift-ansible-playbooks
```

```bash
ansible-playbook -i inventories/sif_lab /usr/share/ansible/openshift-ansible/playbooks/prerequisites.yml
```

```bash 
ansible-playbook -i inventories/sif_lab /usr/share/ansible/openshift-ansible/playbooks/deploy_cluster.yml
```


### Provision and  Deploy Quay
TODO Quay deployer in progress

```bash
ansible-playbook -i inventories/sif_lab/ deployer_quay.yml
```

### Run integration code to configure Quay with OCP deployment

### Deploy integrated Open Innovation Labs CI/CD tools (Gitlab, Nexus, Jenkins, example project)

### Deploy COTS application in OCP to verify CI/CD pipeline and OCP deployment

