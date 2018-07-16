#!/bin/bash
ansible-playbook -i inventory_custom -e "bundle_install=true upgrade_ansible_with_tower=true" install.yml