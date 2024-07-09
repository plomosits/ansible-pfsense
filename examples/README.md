# pfsense

## Development

### Install a collection from source
```bash
ansible-galaxy collection install ../ --force
```

## Modules

### Factory Default
```bash
ansible-playbook -i inventory.yaml playbooks/factory_defaults.yaml -v
```

### Reboot
```bash
ansible-playbook -i inventory.yaml playbooks/reboot.yaml -v
```