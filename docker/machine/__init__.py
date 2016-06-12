from .version import version

__version__ = version
__title__ = 'docker-machine-py'

from .cli.machine import Machine
from .cli.client import Client, Status, Filter
CLIENT = Client()
