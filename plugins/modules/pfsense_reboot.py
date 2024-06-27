#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r"""
---
module: reboot
short_description: Reboot
description: This module manages reboot of a target.
version_added: 2.7.2
author: Philipp Lomosits
options:
  mode:
    description: Mode for the reboot process.
    choices: [ "reboot", "reroot" ]
    default: reboot
"""

EXAMPLES = r"""
- name: reboot
  lomo.pfsense.reboot:

- name: reroot
  lomo.pfsense.reboot:
    mode: reroot
"""

RETURN = r"""
msg:
    description: The output message that the package module generates.
    type: str
    returned: always
    sample: 'Rebooting'
"""

from ansible.module_utils._text import to_text
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection

from ansible_collections.lomo.pfsense.plugins.module_utils.diag_reboot \
    import reboot


def main():
    module_args = dict(
        mode=dict(type="str", default="reboot", choices=["reboot", "reroot"]),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    result = {"changed": False}

    try:
        connection = Connection(module._socket_path)

        reboot(connection, "Reroot" if module.params["mode"] == "reroot" else "Reboot")

        result.update({"msg": "Rebooting"})

    except Exception as exc:
        module.fail_json(msg=to_text(exc))

    module.exit_json(**result)


if __name__ == "__main__":
    main()