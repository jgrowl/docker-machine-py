from subprocess import Popen, PIPE
import re
import json
from .. import errors


class Machine(object):
    def __init__(self, name, config_version, driver_name, driver, host_options, raw_driver, machine_status):
        self.name = name
        self.config_version = config_version
        self.driver_name = driver_name
        self.driver = driver
        self.host_options = host_options
        self.raw_driver = raw_driver
        self.machine_status = machine_status

    @staticmethod
    def create_from_inspect(json, machine_status):
        name = json['Name']
        raw_driver = json['RawDriver']
        config_version = json['ConfigVersion']
        driver_name = json['DriverName']
        driver = json['Driver']
        host_options = json['HostOptions']

        return Machine(name, config_version, driver_name, driver, host_options, raw_driver, machine_status)


class MachineApiMixin(object):

    @staticmethod
    def cmd(command):
        output = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        out, err = output.communicate()

        if err:
            raise errors.DockerMachineException(err)
        return out

    def machine_names(self):
        out = self.cmd(['docker-machine', 'ls', '-q'])
        machine_names = out.splitlines()
        return machine_names

    def machine_inspect(self, machine_name):
        out = self.cmd(['docker-machine', 'inspect', machine_name])
        return json.loads(out)

    def machine(self, machine_name):
        machine_status = self.machine_status(machine_name)
        inspect = self.machine_inspect(machine_name)
        return Machine.create_from_inspect(inspect, machine_status)

    def machines(self):
        machines = []
        for machine_name in self.machine_names():
            machines.append(self.machine(machine_name))

        return machines

    def machine_status(self, name):
        out = self.cmd(['docker-machine', 'status', name])

        s = out.rstrip('\n').lower()
        # if s not in ['running']:
        #     return None

        return s

    def create_machine(self, name, driver_config=None):
        command = ['docker-machine', 'create']

        if driver_config is None:
            command.extend(['--driver', 'none', '--url', 'localhost'])
        else:
            command.extend(driver_config.args())

        command.append(name)
        self.cmd(command)

    def remove_machine(self, name, force=False):
        command = ['docker-machine', 'rm']

        if force:
            command.append('--force')

        command.append(name)

        return self.cmd(command)

