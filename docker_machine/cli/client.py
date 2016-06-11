from subprocess import Popen, PIPE
import json
from enum import Enum
from .tupperware import tupperware
from .. import errors
from docker_machine.cli.driver_config import DriverConfig
from .utils import convert_keys_from_camel_to_snake

LOCALHOST = '127.0.0.1'


class Status(Enum):
    running = "Running"
    paused = "Paused"
    saved = "Saved"
    stopped = "Stopped"
    stopping = "Stopping"
    starting = "Starting"
    error = "Error"
    timeout = "Timeout"


class Filter(object):

    @classmethod
    def from_str(cls, string):
        # todo split string up
        filter_parts = string.split('=')
        return cls(filter_parts[0], filter_parts[1])

    @classmethod
    def construct_filters(cls, possible_filters):
        if isinstance(possible_filters, Filter):
            return [possible_filters]

        if isinstance(possible_filters, str):
            f = cls.from_str(possible_filters)
            return [f]

        if not isinstance(possible_filters, list):
            raise Exception('Bad filter!')

        filters = list()
        for f in possible_filters:
            if isinstance(f, str):
                filters.append(cls.from_str(f))
            elif isinstance(f, Filter):
                filters.append(f)

        return filters

    def __init__(self, key, value):
        """
        :param key:
        :param value:
        :return:
        """
        self.key = key
        self.value = value

    def out(self):
        return ['--filter', '{}={}'.format(self.key, self.value)]
        # driver (driver name)
        # swarm (swarm master's name)
        # state (Running|Paused|Saved|Stopped|Stopping|Starting|Error)
        # name (Machine name returned by driver, supports golang style regular expressions)
        # label (Machine created with --engine-label option, can be filtered with label=<key>[=<value>])


class ClientOutput:
    def __init__(self, raw, formatted=None):
        self.raw = raw
        self.formatted = formatted

    def val(self):
        return self.raw if self.formatted is None else self.formatted


class Client(object):
    def __init__(self, storage_path=None, tls_ca_cert=None, tls_ca_key=None, tls_client_cert=None,
                 tls_client_key=None, github_api_token=None, native_ssh=False, bugsnag_api_token=None):
        super(Client, self).__init__()

        self.storage_path = storage_path
        self.tls_ca_cert = tls_ca_cert
        self.tls_ca_key = tls_ca_key
        self.tls_client_cert = tls_client_cert
        self.tls_client_key = tls_client_key
        self.github_api_token = github_api_token
        self.native_ssh = native_ssh
        self.bugsnag_api_token = bugsnag_api_token

    def cmd(self, command, *args):
        cmd = ['docker-machine']

        if self.storage_path is not None:
            cmd.extend(['--storage-path', self.storage_path])
        if self.tls_ca_cert:
            cmd.extend(['--tls-ca-cert', self.tls_ca_cert])
        if self.tls_ca_key:
            cmd.extend(['--tls-ca-key', self.tls_ca_key])
        if self.tls_client_cert:
            cmd.extend(['--tls-client-cert', self.tls_client_cert])
        if self.tls_client_key:
            cmd.extend(['--tls-client-key', self.tls_client_key])
        if self.github_api_token:
            cmd.extend(['--github-api-token', self.github_api_token])
        if self.native_ssh:
            cmd.extend(['--native-ssh', self.native_ssh])
        if self.bugsnag_api_token:
            cmd.extend(['--bugsnag_api_token', self.bugsnag_api_token])

        cmd.extend(command)
        cmd.extend(args)
        output = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        out, error = output.communicate()
        returncode = output.returncode

        if returncode == 0:
            return out

        error = error.strip()
        raise errors.DockerMachineException(error)

    def active(self):
        """
        Print which machine is active

        :return:
        """
        try:
            raw = self.cmd(['active'])
        except errors.DockerMachineException, e:
            msg = e.message
            if msg == 'No active host found':
                return ClientOutput(msg, list())
            else:
                raise e

        # TODO: format active

        return ClientOutput(raw)

    def config(self, machine_name, swarm=False):
        """
        Print the connection config for machine

        :param machine_name: A machine name.
        :type machine_name: str or unicode
        :param swarm: Display the Swarm config instead of the Docker daemon
        :return:
        """
        cmd = ['config']
        if swarm:
            cmd.append('--swarm')

        raw = self.cmd(cmd, machine_name)
        return ClientOutput(raw)

    def create(self, machine_name, driver=None, **kwargs):
        """
        Create a machine

        :param machine_name:
        :param driver:
        :param kwargs:
        :return:
        """
        driver_config = DriverConfig(driver, **kwargs)
        cmd = ['create']
        if driver_config.driver == 'none':
            cmd.extend(['--driver', 'none', '--url', LOCALHOST])
        else:
            cmd.extend(driver_config.args())

        cmd.append(machine_name)
        raw = self.cmd(cmd)
        return ClientOutput(raw)

    def env(self, machine_name, swarm=False, shell=None, unset=False, no_proxy=False):
        """
        Display the commands to set up the environment for the Docker client

        :param machine_name
        :param swarm: Display the Swarm config instead of the Docker daemon
        :param shell: Force environment to be configured for a specified shell: [fish, cmd, powershell], default is sh/bash
        :param unset: Unset variables instead of setting them
        :param no_proxy: Add machine IP to NO_PROXY environment variable
        :return:
        """
        cmd = ['env']
        if swarm:
            cmd.append('--swarm')

        if shell is not None:
            cmd.extend(['--shell', shell])

        if unset:
            cmd.append('--unset')

        if no_proxy:
            cmd.append('--no_proxy')

        cmd.append(machine_name)

        raw = self.cmd(cmd)
        ret = {}
        for line in raw.split('\n'):
            if line.startswith('export'):
                kv = line.split('=')
                k = kv[0]
                k = k.replace('export ', '')
                v = kv[1].replace('"', '')
                ret[k] = v

        return ClientOutput(raw, ret)

    def inspect(self, machine_name, format=None, snake_case=False, named_tuple=False):
        """
        Inspect information about a machine

        :param machine_name:
        :param format: Format the output using the given go template.
        :param snake_case Converts the dictionary keys to snake_case instead of leaving them CamelCase
        :param named_tuple Converts the dictionary into nested namedtuples so you can use dot operator to access elements
        :return:
        """
        cmd = ['inspect', machine_name]
        if format is not None:
            cmd.append(format)

        raw = self.cmd(cmd)

        out = json.loads(raw)
        if snake_case:
            out = convert_keys_from_camel_to_snake(out)
        if named_tuple:
            out = tupperware(out)

        return ClientOutput(raw, out)

    def ip(self, *machine_names):
        """
        Get the IP address of a machine

        :param machine_names: One or more machine names.
        :return:
        """
        cmd = ['ip']
        cmd.extend(machine_names)
        raw = self.cmd(cmd)
        formatted = raw.strip('\n')
        return ClientOutput(raw, formatted if formatted else '127.0.0.1')

    def kill(self, *machine_names):
        """
        Kill a machine

        :param args:
        :return:
        """
        cmd = ['kill']
        cmd.extend(machine_names)
        raw = self.cmd(cmd)
        return ClientOutput(raw)

    def ls(self, quiet=False, filters=None, timeout=None):
        """
        List machines

        :param quiet: Enable quiet mode
        :param filters: Filter output based on conditions provided
        :param timeout: Timeout in seconds, default to 10s
        :return:
        """
        cmd = ['ls']

        if quiet:
            cmd.append('--quiet')

        if filters is not None:
            for f in Filter.construct_filters(filters):
                cmd.extend(f.out())

        if timeout is not None:
            cmd.extend(['--timeout', timeout])

        raw = self.cmd(cmd)

        return ClientOutput(raw, self._format_quiet_ls(raw) if quiet else self._format_ls(raw))

    @staticmethod
    def _format_quiet_ls(raw):
        return raw.splitlines() if raw is not None else []

    @staticmethod
    def _format_ls(raw):
        return raw

    def regenerate_certs(self, machine_name=None, force=True):
        """
        Regenerate TLS Certificates for a machine

        :param machine_name:
        :param force:
        :return:
        """
        cmd = ['regenerate-certs']
        if force:
            cmd.extend(['--force'])

        if machine_name is not None:
            cmd.append(machine_name)

        raw = self.cmd(cmd)
        return ClientOutput(raw)

    def restart(self, *machine_names):
        """
        Restart a machine

        :param args:  Argument(s) are one or more machine names.
        :return:
        """
        raw = self.cmd(['restart'], *machine_names)
        return ClientOutput(raw)

    def rm(self, machine_name, force=False, prompt=False):
        """
        Remove a machine

        :param machine_name
        :param force:   Remove local configuration even if machine cannot be removed
        :param prompt:  Prompting further user confirmation
        :return:
        """
        cmd = ['rm']

        # We never want a prompt
        if not prompt:
            cmd.append('-y')

        if force:
            cmd.extend(['--force'])

        cmd.append(machine_name)
        raw = self.cmd(cmd)
        return ClientOutput(raw)

    def ssh(self, machine_name, command=None):
        """
        Log into or run a command on a machine with SSH.

        :param machine_name:
        :param command:
        :return:
        """
        if command is None:
            return self.cmd(['ssh'], machine_name)

        return self.cmd(['ssh'], machine_name, command)

    def scp(self, src, dest, recursive=False):
        """
        Copy files between machines

        :param src:
        :param dest:
        :param recursive:
        :return:
        """
        cmd = ['scp']
        if recursive:
            cmd.extend(['--recursive'])

        cmd.extend([src, dest])
        return self.cmd(cmd)

    def stop(self, *machine_names):
        """
        Stop a machine

        :param args:
        :return:
        """
        raw = self.cmd(['stop'], *machine_names)
        return ClientOutput(raw)

    def start(self, *machine_names):
        """
        Start a machine

        :param args:
        :return:
        """
        raw = self.cmd(['start'], *machine_names)
        return ClientOutput(raw)

    def status(self, machine_name):
        """
        Get the status of a machine

        :param machine_name:
        :return:
        """
        raw = self.cmd(['status'], machine_name)
        return ClientOutput(raw, Status(raw.rstrip('\n')))

    def upgrade(self, *machine_names):
        """
        Upgrade a machine to the latest version of Docker

        :param args:
        :return:
        """
        raw = self.cmd(['upgrade'], *machine_names)
        return ClientOutput(raw)

    def url(self, machine_name):
        """
        Get the URL of a machine

        :param machine_name:
        :return:
        """
        raw = self.cmd(['url'], machine_name)
        return ClientOutput(raw, raw.rstrip('\n'))

    def version(self):
        """
        Show the Docker Machine version or a machine docker version

        :return:
        """
        raw = self.cmd(['version'])
        parts = raw.split()
        version_number = parts[2].replace(',', '')
        version_hash = parts[4]
        from collections import namedtuple
        VersionInfo = namedtuple('VersionInfo', 'version_number version_hash')
        version_info = VersionInfo(version_number, version_hash)
        return ClientOutput(raw, version_info)

    def help(self, command=None):
        """
        Shows a list of commands or help for one command

        :param command
        :return:
        """
        cmd = ['help']
        if command is not None:
            cmd.append(command)

        raw = self.cmd(cmd)
        return ClientOutput(raw)
