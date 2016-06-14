from .version import version

__version__ = version
__title__ = 'docker-machine-py'

from .cli.client import Client
CLIENT = Client()
