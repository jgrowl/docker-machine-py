from . import cli
from . import constants
from . import errors


class Client(
    cli.MachineApiMixin
    ):
    def __init__(self, timeout=constants.DEFAULT_TIMEOUT_SECONDS, tls=False):
        super(Client, self).__init__()

        version_info = self.version_info()
        self.version_number = version_info['version_number']
        self.version_hash = version_info['version_hash']
