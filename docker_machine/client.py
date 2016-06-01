# import json
# import struct
# import sys
#
# import requests
# import requests.exceptions

from . import cli
from . import constants
from . import errors
# from .auth import auth
# from .unixconn import unixconn
# from .ssladapter import ssladapter
from .utils import utils
# from .utils import utils, check_resource
# from .tls import TLSConfig


class Client(
    # requests.Session,
    # api.BuildApiMixin,
    # api.ContainerApiMixin,
    # api.DaemonApiMixin,
    # api.ExecApiMixin,
    # api.ImageApiMixin,
    # api.VolumeApiMixin,
    # api.NetworkApiMixin
    cli.MachineApiMixin
    ):
    def __init__(self, timeout=constants.DEFAULT_TIMEOUT_SECONDS, tls=False):
        super(Client, self).__init__()

        version_info = self.version_info()
        self.version_number = version_info['version_number']
        self.version_hash = version_info['version_hash']

        # if tls and not base_url.startswith('https://'):
        #     raise errors.TLSParameterError(
        #         'If using TLS, the base_url argument must begin with '
        #         '"https://".')
        #
        # self.base_url = base_url
        # self.timeout = timeout
        #
        # self._auth_configs = auth.load_config()
        #
        # base_url = utils.parse_host(base_url, sys.platform)
        # if base_url.startswith('http+unix://'):
        #     self._custom_adapter = unixconn.UnixAdapter(base_url, timeout)
        #     self.mount('http+docker://', self._custom_adapter)
        #     self.base_url = 'http+docker://localunixsocket'
        # else:
        #     # Use SSLAdapter for the ability to specify SSL version
        #     if isinstance(tls, TLSConfig):
        #         tls.configure_client(self)
        #     elif tls:
        #         self._custom_adapter = ssladapter.SSLAdapter()
        #         self.mount('https://', self._custom_adapter)
        #     self.base_url = base_url
        #
        # # version detection needs to be after unix adapter mounting
        # if version is None:
        #     self._version = constants.DEFAULT_DOCKER_API_VERSION
        # elif isinstance(version, six.string_types):
        #     if version.lower() == 'auto':
        #         self._version = self._retrieve_server_version()
        #     else:
        #         self._version = version
        # else:
        #     raise errors.DockerException(
        #         'Version parameter must be a string or None. Found {0}'.format(
        #             type(version).__name__
        #         )
        #     )
    # @property
    # def api_version(self):
    #     return self._version


# class AutoVersionClient(Client):
#     def __init__(self, *args, **kwargs):
#         if 'version' in kwargs and kwargs['version']:
#             raise errors.DockerException(
#                 'Can not specify version for AutoVersionClient'
#             )
#         kwargs['version'] = 'auto'
#         super(AutoVersionClient, self).__init__(*args, **kwargs)