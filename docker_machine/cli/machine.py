from subprocess import Popen, PIPE
import json
from .. import errors
from docker_machine.utils.utils import convert_keys_from_camel_to_snake
from docker_machine.utils.tupperware import tupperware


class Machine(object):
    def __init__(self, inspection, machine_status, env):
        self.machine_status = machine_status
        self.inspection = inspection
        self.env = env
        # self.name
        # self.config_version
        # self.driver_name
        # self.driver
        # self.host_options
        # self.raw_driver

    def __getattr__(self, name):
        try:
            return getattr(self.inspection, name)
        except AttributeError, e:
            raise AttributeError("Inspection' object has no attribute '%s'" % name)

    @staticmethod
    def create_from_inspect(json, machine_status, env):
        inspection = tupperware(convert_keys_from_camel_to_snake(json))
        return Machine(inspection, machine_status, env)


class MachineApiMixin(object):

    @staticmethod
    def cmd(command):
        cmd = ['docker-machine']
        cmd.extend(command)
        output = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        out, error = output.communicate()

        if not error:
            return out

        # # TODO: add machine_name to command args?
        # if error == 'Host "none" does not exist':
        #     raise errors.DockerMachineException(error)

        raise errors.DockerMachineException(error.strip())

    def version_info(self):
        out = self.cmd(['--version'])
        parts = out.split()
        version_number = parts[2]
        version_hash = parts[3]
        return dict(version_number=version_number, version_hash=version_hash)

    def machine_names(self):
        out = self.cmd(['ls', '-q'])
        machine_names = out.splitlines()
        return machine_names

    def machine_name_exists(self, machine_name):
        return machine_name in self.machine_names()

    def machine_inspect(self, machine_name):
        out = self.cmd(['inspect', machine_name])
        return json.loads(out)

    def _env(self, machine_name):
        out = self.cmd(['env', machine_name])
        ret = {}
        for line in out.split('\n'):
            if line.startswith('export'):
                kv = line.split('=')
                k = kv[0]
                k = k.replace('export ', '')
                v = kv[1].replace('"', '')
                ret[k] = v
        return ret

    def ip(self, machine_name):
        return self.cmd(['ip', machine_name])

    def machine(self, machine_name):
        env = self._env(machine_name)
        machine_status = self.machine_status(machine_name)
        inspect = self.machine_inspect(machine_name)
        return Machine.create_from_inspect(inspect, machine_status, env)

    def machines(self):
        machines = []
        for machine_name in self.machine_names():
            machines.append(self.machine(machine_name))

        return machines

    def machine_status(self, name):
        out = self.cmd(['status', name])
        return out.rstrip('\n').lower()

    def create_machine(self, name, driver_config=None):
        command = ['create']

        if driver_config is None:
            command.extend(['--driver', 'none', '--url', 'localhost'])
        else:
            command.extend(driver_config.args())

        command.append(name)
        self.cmd(command)

    def remove_machine(self, name, force=False):
        command = ['rm']

        if force:
            command.append('--force')

        command.append(name)

        return self.cmd(command)

