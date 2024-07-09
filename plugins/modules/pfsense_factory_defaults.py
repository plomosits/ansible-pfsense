#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r"""
---
module: factory_defaults
short_description: Factory Defaults
description: This module manages factory defaults of a target.
version_added: 2.7.2
author: Philipp Lomosits
"""

EXAMPLES = r"""
- name: factory_defaults
  plomosits.pfsense.factory_defaults:
"""

RETURN = r"""
msg:
    description: The output message that the package module generates.
    type: str
    returned: always
    sample: 'Resetting'
"""

from ansible.module_utils._text import to_text
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection

from ansible_collections.plomosits.pfsense.plugins.module_utils.diag_defaults \
    import diag_defaults


def main():
    module_args = dict()

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    result = {"changed": False}

    try:
        connection = Connection(module._socket_path)

        diag_defaults(connection)

        result.update({"changed": True, "msg": "Resetting"})

    except Exception as exc:
        module.fail_json(msg=to_text(exc))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
