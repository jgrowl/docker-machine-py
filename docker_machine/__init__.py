from .version import version#, version_info

__version__ = version
__title__ = 'docker-machine-py'

from .client import Client #, AutoVersionClient # flake8: noqa

from .cli.driver_config import DigitaloceanDriverConfig
