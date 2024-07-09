#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r"""
---
module: pfsense_setup_wizard
short_description: pfsense setup
description: This module setups pfsense on a target.
version_added: 2.7.2
author: Philipp Lomosits
options:
  steps:
    description: Steps configuration.
    type: dict
    required: true
    suboptions:
      2:
        description: General Information
        suboptions:
          hostname:
            description: "Name of the firewall host, without domain part."
            type: str
          domain:
            description: "Domain name for the firewall."
            type: str
          primarydnsserver:
            description: Primary DNS Server
            type: str
          secondarydnsserver:
            description: Secondary DNS Server
            type: str
          overridedns:
            description: Allow DNS servers to be overridden by DHCP/PPP on WAN
            type: bool
        type: dict
      3:
        description: Time Server Information
        suboptions:
          timeserverhostname:
            description: Enter the hostname (FQDN) of the time server.
            type: str
          timezone:
            description: Timezone
            type: str
        type: dict
      4:
        description: Configure WAN Interface
        suboptions:
          selectedtype:
            description: SelectedType
            type: str
        
          macaddress:
            description: 'This field can be used to modify ("spoof") the MAC address of
              the WAN interface (may be required with some cable connections). Enter a MAC
              address in the following format: xx:xx:xx:xx:xx:xx or leave blank.'
            type: str
          mtu:
            description: Set the MTU of the WAN interface. If this field is left blank,
              an MTU of 1492 bytes for PPPoE and 1500 bytes for all other connection types
              will be assumed.
            type: int
          mss:
            description: If a value is entered in this field, then MSS clamping for TCP
              connections to the value entered above minus 40 (TCP/IP header size) will
              be in effect. If this field is left blank, an MSS of 1492 bytes for PPPoE
              and 1500 bytes for all other connection types will be assumed. This should
              match the above MTU value in most all cases.
            type: int

          ipaddress:
            description: IP Address
            type: str
          subnetmask:
            description: Subnet Mask
            type: int
            choices: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
          upstreamgateway:
            description: Upstream Gateway
            type: str

          dhcphostname:
            description: The value in this field is sent as the DHCP client identifier and
              hostname when requesting a DHCP lease. Some ISPs may require this (for client
              identification).
            type: str

          pppoeusername:
            description: PPPoE Username
            type: str
          pppoepassword:
            description: PPPoE Password
            type: str
          pppoeservicename:
            description: 'Hint: this field can usually be left empty'
            type: str
          pppoedialondemand:
            description: This option causes the interface to operate in dial-on-demand mode,
              allowing a virtual full time connection. The interface is configured, but
              the actual connection of the link is delayed until qualifying outgoing traffic
              is detected.
            type: bool
          pppoeidletimeout:
            description: If no qualifying outgoing packets are transmitted for the specified
              number of seconds, the connection is brought down. An idle timeout of zero
              disables this feature.
            type: int

          pptpusername:
            description: PPTP Username
            type: str
          pptppassword:
            description: PPTP Password
            type: str
          pptplocalipaddress:
            description: PPTP Local IP Address
            type: str
          pptplocalsubnet:
            description: pptplocalsubnet
            type: int
            choices: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
          pptpremoteipaddress:
            description: PPTP Remote IP Address
            type: str
          pptpdialondemand:
            description: This option causes the interface to operate in dial-on-demand mode,
              allowing a virtual full time connection. The interface is configured, but
              the actual connection of the link is delayed until qualifying outgoing traffic
              is detected.
            type: bool
          pptpidletimeout:
            description: If no qualifying outgoing packets are transmitted for the specified
              number of seconds, the connection is brought down. An idle timeout of zero
              disables this feature.
            type: int

          blockrfc1918privatenetworks:
            description: When set, this option blocks traffic from IP addresses that are
              reserved for private networks as per RFC 1918 (10/8, 172.16/12, 192.168/16)
              as well as loopback addresses (127/8). This option should generally be left
              turned on, unless the WAN network lies in such a private address space, too.
            type: bool

          blockbogonnetworks:
            description: When set, this option blocks traffic from IP addresses that are
              reserved (but not RFC 1918) or not yet assigned by IANA. Bogons are prefixes
              that should never appear in the Internet routing table, and obviously should
              not appear as the source address in any packets received.
            type: bool
        type: dict
      5:
        description: Configure LAN Interface
        suboptions:
          lanipaddress:
            description: Type dhcp if this interface uses DHCP to obtain its IP address.
            type: str
          subnetmask:
            description: Subnet Mask
            type: int
            choices: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
        type: dict
      6:
        description: Set Admin WebGUI Password
        suboptions:
          adminpassword:
            description: Admin Password
            type: str
          adminpasswordagain:
            description: Admin Password AGAIN
            type: str
        type: dict
"""

EXAMPLES = r"""
- name: pfsense setup
  plomosits.pfsense.setup_wizard:
    steps:
      2:
        hostname: pfSense
        domain: home.arpa
        primarydnsserver: 8.8.8.8
        secondarydnsserver: 8.8.4.4
        overridedns: true
      3:
        timeserverhostname: 0.europe.pool.ntp.org
        timezone: Europe/Vienna
      4:
        blockrfc1918privatenetworks: true
        blockbogonnetworks: true
      5:
        lanipaddress: 192.168.1.1
        subnetmask: 24
"""

RETURN = r"""
msg:
    description: The output message that the package module generates.
    type: str
    returned: always
    sample: 'Congratulations! pfSense is now configured.'
"""

from ansible.module_utils._text import to_text
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection

from ansible_collections.plomosits.pfsense.plugins.module_utils.wizard \
    import wizard


def main():
    module_args = dict(
        steps=dict(type="dict", options={
            "2": dict(type="dict", apply_defaults=True, options=dict(
                hostname=dict(type="str", required=True),
                domain=dict(type="str", required=True),
                primarydnsserver=dict(type="str"),
                secondarydnsserver=dict(type="str"),
                overridedns=dict(type="bool"),
            )),
            "3": dict(type="dict", apply_defaults=True, options=dict(
                timeserverhostname=dict(type="str", required=True),
                timezone=dict(type="str", required=True)
            )),
            "4":dict(type="dict", apply_defaults=True, options=dict(
                selectedtype=dict(type="str", default="dhcp", choices=["Static", "dhcp", "pppoe", "pptp"]),
                macaddress=dict(type="str"),
                mtu=dict(type="int"),
                mss=dict(type="int"),
                ipaddress=dict(type="str"),
                subnetmask=dict(type="int", choices=range(1,33)),
                upstreamgateway=dict(type="str"),
                dhcphostname=dict(type="str"),
                pppoeusername=dict(type="str"),
                pppoepassword=dict(type="str"),
                pppoeservicename=dict(type="str"),
                pppoedialondemand=dict(type="bool"),
                pppoeidletimeout=dict(type="int"),
                pptpusername=dict(type="str"),
                pptppassword=dict(type="str"),
                pptplocalipaddress=dict(type="str"),
                pptplocalsubnet=dict(type="int", choices=range(1,33)),
                pptpremoteipaddress=dict(type="str"),
                pptpdialondemand=dict(type="bool"),
                pptpidletimeout=dict(type="int"),
                blockrfc1918privatenetworks=dict(type="bool"),
                blockbogonnetworks=dict(type="bool")
            )),
            "5":dict(type="dict", apply_defaults=True, options=dict(
                lanipaddress=dict(type="str", required=True),
                subnetmask=dict(type="int", required=True, choices=range(1, 33))
            )),
            "6":dict(type="dict", apply_defaults=True, options=dict(
                adminpassword=dict(type="str"),
                adminpasswordagain=dict(type="str")
            ))
        }),
        foo=dict(type="str", default="pfSense")
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    result = {"changed": False}

    try:
        connection = Connection(module._socket_path)

        for step_id in range(0, 8):
            wizard(connection, "setup_wizard", step_id, module.params["steps"].get(str(step_id), {}))

        result.update({"changed": True, "msg": "Congratulations! pfSense is now configured."})

    except Exception as exc:
        module.fail_json(msg=to_text(exc))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
