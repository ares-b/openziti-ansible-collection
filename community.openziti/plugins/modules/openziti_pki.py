# -*- coding: utf-8 -*-

# (c) 2022, Arslane BAHLEL <arslane.bahlel+openziti@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
'''

RETURN = '''
'''

from os.path import isdir
from os.path import join as path_join
from os import makedirs
from ansible_collections.community.openziti.plugins.module_utils.openziti_cli import OpenZitiCli

from ansible.module_utils.basic import AnsibleModule

class OpenZitiPki(OpenZitiCli):

    required_args = {
        "ca": ["ca_name", "file_name"],
        "intermediate": ["ca_name", "file_name", "name", "key_file"],
        "client": ["ca_name", "file_name", "name", "key_file"],
        "server": ["ca_name", "file_name", "name", "key_file", "dns", "ip"],
    }

    def __init__(self, module: AnsibleModule):
        super().__init__(module)
        self.component = self.parameters["component"]
        self.mode = self.parameters["mode"]

        self._check_cli_args()
        self._prepare_cli()

    def _prepare_cli(self) -> None:
        self.cmd.extend([
            "pki",
            f"{self.mode}",
            f"{self.component}",
            "--ca-name",
            f"{self.parameters['ca_name']}",
            "--max-path-len",
            f"{self.parameters['max_path_len'] or -1}",
            "--pki-country",
            f"{self.parameters['country']}",
            "--pki-locality",
            f"{self.parameters['locality']}",
            "--pki-province",
            f"{self.parameters['province']}",
            "--pki-organization",
            f"{self.parameters['organization']}",
            "--pki-organizational-unit",
            f"{self.parameters['organizational_unit']}",
            "--pki-root",
            f"{self.parameters['pki_path']}"
        ])

        if self.component == "ca":
            self.cmd.extend([
                "--ca-file",
                f"{self.parameters['file_name']}",
                "--private-key-size",
                f"{self.parameters['private_key_size'] or 4096}",
                "--expire-limit",
                f"{self.parameters['expire_limit'] or 3650}"
            ])    
        elif self.component == "intermediate":
            self.cmd.extend([
                "--intermediate-file",
                f"{self.parameters['file_name']}",
                "--intermediate-name",
                f"{self.parameters['name']}",
                "--private-key-size",
                f"{self.parameters['private_key_size'] or 4096}",
                "--expire-limit",
                f"{self.parameters['expire_limit'] or 3650}"
            ])
        elif self.component == "client":
            self.cmd.extend([
                "--client-file",
                f"{self.parameters['file_name']}",
                "--client-name",
                f"{self.parameters['name']}",
                "--private-key-size",
                f"{self.parameters['private_key_size'] or 2048}",
                "--expire-limit",
                f"{self.parameters['expire_limit'] or 365}",
                "--key-file",
                f"{self.parameters['key_file']}",
                "--email",
                f"{self.parameters['email']}"
            ])
        elif self.component == "server":
            self.cmd.extend([
                "--client-file",
                f"{self.parameters['file_name']}",
                "--client-name",
                f"{self.parameters['name']}",
                "--private-key-size",
                f"{self.parameters['private_key_size'] or 4096}",
                "--expire-limit",
                f"{self.parameters['expire_limit'] or 365}",
                "--key-file",
                f"{self.parameters['key_file']}",
                "--dns",
                f"{self.parameters['dns']},"
                "--ip",
                f"{self.parameters['ip']}"
            ])
        else:
            raise ValueError(f"Incorrect pki component {self.component}")

    def _check_cli_args(self) -> None:       
        missing_args = [arg for arg in self.required_args[self.component] if self.parameters[arg] is None]

        if missing_args:
            raise ValueError(f"{self.mode} component {self.component} requires arguments [{', '.join(missing_args)}].")

    def is_changed(self) -> bool:
        
        component_path = path_join(self.parameters["pki_path"], self.parameters["file_name"])

        if isdir(component_path):
            self.diff = { "before": component_path, "after": component_path }
            self.output_msg = f"PKI {self.component} {self.parameters['file_name']} already exists."
            return False

        self.diff = { "before": None, "after": component_path }
        self.output_msg = f"PKI {self.component} {self.parameters['file_name']} created."
        return True


def main():
    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=dict(
            ca_name=dict(required=True, type='str'),
            file_name=dict(required=True, type='str'),
            name=dict(type='str', default=None),
            key_file=dict(type='str', default=None),
            email=dict(type='str', default=None),
            dns=dict(type='str', default=None),
            ip=dict(type='str', default=None),
            pki_path=dict(required=True, type='str', default=None),
            max_path_len=dict(type='int', default=None),
            private_key_size=dict(type='int', default=None),
            expire_limit=dict(type='int', default=None),
            country=dict(default='US', type='str'),
            locality=dict(default='Charlotte', type='str'),
            organization=dict(default='NetFroundry', type='str'),
            organizational_unit=dict(default='ADV-DEV', type='str'),
            province=dict(default='NC', type='str'),
            mode=dict(choices=['create'], default='create'),
            component=dict(choices=['ca', 'intermediate', 'client', 'server'], default='ca'),
            ziti_cli_path=dict(type='str', default =None),
        )
    )
    
    try:
        ziti_cli = OpenZitiPki(module)
    except ValueError as error:
        module.fail_json(str(error))
        
    changed = ziti_cli.is_changed()
    
    if not module.check_mode:
        if not isdir(module.params['pki_path']):
            makedirs(module.params['pki_path'])
        ziti_cli.execute()

    module.exit_json(changed=changed, msg=ziti_cli.output_msg, diff=ziti_cli.diff)


if __name__ == '__main__':
    main()
