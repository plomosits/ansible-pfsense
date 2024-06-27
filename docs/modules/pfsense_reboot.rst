
        This module manages reboot of a target - rst.

ADDED IN: version 2.7.2

OPTIONS (= is mandatory):

- mode
        Mode for the reboot process.
        choices: [reboot, reroot]
        default: reboot


AUTHOR: Philipp Lomosits

EXAMPLES:

- name: reboot
  lomo.pfsense.reboot:

- name: reroot
  lomo.pfsense.reboot:
    mode: reroot


RETURN VALUES:
- msg
        The output message that the package module generates.
        returned: always
        sample: Rebooting
        type: str
