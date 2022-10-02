from typing import List
from ansible.module_utils.basic import AnsibleModule
from abc import ABC, abstractmethod

class OpenZitiCli(ABC):
    """Abstract class for Ziti CLI plugins.
    """
    def __init__(self, module: AnsibleModule):
        self.module = module
        self.parameters = module.params
        self.cmd = ["ziti"] if not self.parameters["ziti_cli_path"] else [self.parameters['ziti_cli_path']]
        self.cmd_rc = None
        self.cmd_out = None
        self.cmd_err = None

    def _is_ziti_installed(self) -> bool:
        """Check if Ziti CLI is installed.

        Checks whether or not ``ziti`` is added to the path or path towards it is provided in module parameters. 
        """
        return not (self.parameters["ziti_cli_path"]  is None) or not (self.module.get_bin_path("ziti") is None)

    def execute(self):
        """Executes the CLI command.
        """
        if not self._is_ziti_installed():
            self.module.fail_json("Ziti CLI not found, consider adding it to the path or providing ziti_cli_path parameter before using pki module.")
        self.cmd_rc, self.cmd_out, self.cmd_err = self.module.run_command(self.cmd)

    @abstractmethod
    def is_changed(self) -> bool:
        pass

    @abstractmethod
    def _prepare_cli(self) -> None:
        pass

    @abstractmethod
    def _check_cli_args(self) -> List[str]:
        pass
