ANSIBLE_BECOME_METHOD=sudo ANSIBLE_BECOME=true ansible-playbook -i inventory_custom -e "bundle_install=true upgrade_ansible_with_tower=true" install.yml
