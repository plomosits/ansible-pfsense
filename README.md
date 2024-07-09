# Plomosits Pfsense Collection

This repository contains the `plomosits.pfsense` Ansible Collection.

Inspired by [pfsensible.core](https://github.com/pfsensible/core) project, I'm working on a collection that does not require any prerequisites on the pfsense target.

## Tested with Ansible and pfsense

Tested with ansible-core >=2.14 releases and the current development version of ansible-core and pfsense >=2.7.2.

## External requirements

Some modules and plugins require external libraries. Please check the requirements for each plugin or module you use in the documentation to find out which requirements are needed.

## Included content

Please check the included content on the [Ansible Galaxy page for this collection](https://galaxy.ansible.com/plomosits/pfsense).

## Using this collection

The version of the collection is aligned to the version of pfsense. The idea behind is to support different releases of pfsense.
So if you have using pfsense v2.7.2 you can use this collection with the same version or version below.

|                pfsense | plomosits.pfsense |
|-----------------------:|------------------:|
| 2.7.2 <= **x** < 2.8.0 |             2.7.2 |
|                  2.8.x |             2.8.0 | # in future

```bash
ansible-galaxy collection install plomosits.pfsense:==X.Y.Z
```

You can also include it in a `requirements.yml` file and install it via `ansible-galaxy collection install -r requirements.yml` using the format:

```yaml
collections:
  - name: plomosits.pfsense
    version: X.Y.Z
```

See [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Sample Configuration
```yaml
# inventory.yaml
firewalls:
  hosts:
    pfsense:
      ansible_host: 192.168.1.1
      ansible_user: admin
      ansible_password: pfsense
      
      ansible_connection: httpapi
      ansible_network_os: plomosits.pfsense.pfsense
      ansible_httpapi_port: 443
      ansible_httpapi_use_ssl: yes
      ansible_httpapi_validate_certs: no
```
```yaml
# playbooks/reboot.yaml
- name: pfSense Reboot
  hosts: all
  gather_facts: false

  collections:
    - plomosits.pfsense

  tasks:
    - name: Reboot
      pfsense_reboot:
        mode: reboot
```
### run
```bash
ansible-playbook -i inventory.yaml playbooks/reboot.yaml
```

## [Examples](examples)

## Modules
The following modules are currently available:

- [plomosits.pfsense.pfsense_factory_defaults](../content/module/pfsense_factory_defaults/)
- [plomosits.pfsense.pfsense_reboot](../content/module/pfsense_reboot/)

## More information

<!-- List out where the user can find additional information, such as working group meeting times, slack/IRC channels, or documentation for the product this collection automates. At a minimum, link to: -->

- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/devel/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/devel/dev_guide/index.html)
- [Ansible Collections Checklist](https://github.com/ansible-collections/overview/blob/main/collection_requirements.rst)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html)
- [The Bullhorn (the Ansible Contributor newsletter)](https://us19.campaign-archive.com/home/?u=56d874e027110e35dea0e03c1&id=d6635f5420)
- [News for Maintainers](https://github.com/ansible-collections/news-for-maintainers)

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
