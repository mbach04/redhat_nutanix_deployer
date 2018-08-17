# Instructions for Initial SIF Lab Install

## Initial Setup

- Check for correct DNS entries for all hosts (see `inventories/*/group_vars/all.yml`)
- Ensure all variables and hostnames are set correctly in the `inventories` folder

## Automated Deployment to SIF Lab - Week 1

### Provision an Ansible core control/bastion node
This has been manually deployed in the SIF lab. It must be used as a jumpbox for the rest of the installation.


### Provision and Deploy Repository Server
This server acts as a centralized repository for RPMs, extra binaries, and Docker Images.
See the `deploy_repository.yml` playbook and the README in the `repository` role for more
details.

```bash
ansible-playbook -i inventories/sif_lab/ deployer_repository.yml
```

### Provision and Deploy Loadbalancers
Provisions two sets of two loadbalancers each. The first set is configured to loadbalance the OpenShift masters as well as the Ansible Tower nodes. The second set will loadbalance the OpenShift infra nodes.

```bash
ansible-playbook -i inventories/sif_lab/ deployer_loadbalancer.yml
```

### Provision, Deploy, and Configure OpenShift
Provisions an HA OpenShift cluster of 3 masters, 4 application nodes, 2 infra nodes, and 3 CNS nodes. These playbooks will also configure default users and storage on the cluster.

```bash
ansible-playbook -i inventories/sif_lab/ deployer_ocp.yml
```
```bash
ansible-playbook -i inventories/sif_lab/ocp_inventory /usr/share/ansible/openshift-ansible/playbooks/prerequisites.yml
```
```bash
ansible-playbook -i inventories/sif_lab/ocp_inventory /usr/share/ansible/openshift-ansible/playbooks/deploy_cluster.yml
```
```bash
ansible-playbook -i inventories/sif_lab/ocp_inventory standalone_playbooks/htpasswd.yml
```
```bash
ansible-playbook -i inventories/sif_lab/ocp_inventory standalone_playbooks/configure_storageclass.yml
```

### Provision and Deploy Ansible Tower Servers
Provisions a HA Ansible Tower cluster of 3 tower nodes and a database node.

```bash
ansible-playbook -i inventories/sif_lab/ deployer_tower.yml
```


