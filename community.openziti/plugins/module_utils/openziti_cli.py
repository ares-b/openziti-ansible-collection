from typing import Optional, List
from ansible.module_utils.basic import AnsibleModule
from abc import ABC, abstractmethod

class OpenZitiCli(ABC):

    def __init__(self, module: AnsibleModule):
        self.module = module
        self.parameters = module.params
        self.cmd = ["ziti"] if not self.parameters["ziti_cli_path"] else [self.parameters['ziti_cli_path']]
        self.cmd_rc = None
        self.cmd_out = None
        self.cmd_err = None

    def _is_ziti_installed(self) -> bool:
        return not (self.parameters["ziti_cli_path"]  is None) or not (self.module.get_bin_path("ziti") is None)

    def execute(self):
        if not self._is_ziti_installed():
            self.module.fail_json("Ziti CLI not found, consider adding it to the path or providing ziti_cli_path parameter before using pki module.")
        self.cmd_rc, self.cmd_out, self.cmd_err = self.module.run_command(self.cmd)

    @abstractmethod
    def is_changed(self):
        pass

    @abstractmethod
    def prepare_cli(self):
        pass

    @abstractmethod
    def get_missing_args(self):
        pass

