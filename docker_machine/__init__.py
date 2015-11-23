from .version import version
# from .version import version, version_info

__version__ = version
__title__ = 'docker-machine-py'

from .client import Client
# from .client import Client, AutoVersionClient # flake8: noqa