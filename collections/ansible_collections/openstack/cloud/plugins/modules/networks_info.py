#!/usr/bin/python

# Copyright (c) 2015 Hewlett-Packard Development Company, L.P.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = '''
---
module: networks_info
short_description: Retrieve information about one or more OpenStack networks.
author: OpenStack Ansible SIG
description:
    - Retrieve information about one or more networks from OpenStack.
    - This module was called C(openstack.cloud.networks_facts) before Ansible 2.9, returning C(ansible_facts).
      Note that the M(openstack.cloud.networks_info) module no longer returns C(ansible_facts)!
options:
   name:
     description:
        - Name or ID of the Network
     required: false
     type: str
   filters:
     description:
        - A dictionary of meta data to use for further filtering.  Elements of
          this dictionary may be additional dictionaries.
     required: false
     type: dict
requirements:
    - "python >= 3.6"
    - "openstacksdk"

extends_documentation_fragment:
- openstack.cloud.openstack
'''

EXAMPLES = '''
- name: Gather information about previously created networks
  openstack.cloud.networks_info:
    auth:
      auth_url: https://identity.example.com
      username: user
      password: password
      project_name: someproject
  register: result

- name: Show openstack networks
  debug:
    msg: "{{ result.openstack_networks }}"

- name: Gather information about a previously created network by name
  openstack.cloud.networks_info:
    auth:
      auth_url: https://identity.example.com
      username: user
      password: password
      project_name: someproject
    name:  network1
  register: result

- name: Show openstack networks
  debug:
    msg: "{{ result.openstack_networks }}"

- name: Gather information about a previously created network with filter
  # Note: name and filters parameters are Not mutually exclusive
  openstack.cloud.networks_info:
    auth:
      auth_url: https://identity.example.com
      username: user
      password: password
      project_name: someproject
    filters:
      tenant_id: 55e2ce24b2a245b09f181bf025724cbe
      subnets:
        - 057d4bdf-6d4d-4728-bb0f-5ac45a6f7400
        - 443d4dc0-91d4-4998-b21c-357d10433483
  register: result

- name: Show openstack networks
  debug:
    msg: "{{ result.openstack_networks }}"
'''

RETURN = '''
openstack_networks:
    description: has all the openstack information about the networks
    returned: always, but can be null
    type: complex
    contains:
        id:
            description: Unique UUID.
            returned: success
            type: str
        name:
            description: Name given to the network.
            returned: success
            type: str
        status:
            description: Network status.
            returned: success
            type: str
        subnets:
            description: Subnet(s) included in this network.
            returned: success
            type: list
            elements: str
        tenant_id:
            description: Tenant id associated with this network.
            returned: success
            type: str
        shared:
            description: Network shared flag.
            returned: success
            type: bool
'''

from ansible_collections.openstack.cloud.plugins.module_utils.openstack import OpenStackModule


class NetworkInfoModule(OpenStackModule):

    deprecated_names = ('networks_facts', 'openstack.cloud.networks_facts')

    argument_spec = dict(
        name=dict(required=False, default=None),
        filters=dict(required=False, type='dict', default=None)
    )
    module_kwargs = dict(
        supports_check_mode=True
    )

    def run(self):

        kwargs = self.check_versioned(
            filters=self.params['filters']
        )
        if self.params['name']:
            kwargs['name_or_id'] = self.params['name']
        networks = self.conn.search_networks(**kwargs)

        self.exit(changed=False, openstack_networks=networks)


def main():
    module = NetworkInfoModule()
    module()


if __name__ == '__main__':
    main()
