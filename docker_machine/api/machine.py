from subprocess import Popen, PIPE
import re
from .. import errors

class MachineApiMixin(object):
    def machines(self, quiet=False, all=False, trunc=False, latest=False,
               since=None, before=None, limit=-1, size=False,
               filters=None):

        output = Popen(['docker-machine', 'ls'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        out, err = output.communicate()

        # rc = output.returncode
        # if rc != 0:
        #     # raise errors.AnsibleError('Error with executing docker-machine env')
        #     # raise Error
        #     raise Exception('YO')

        lines = out.splitlines()
        del lines[0]

        machines = list(map((lambda x: re.split('\s+', x)), lines))
        machines = list(
            map((lambda x: {'name': x[0], 'active': x[1], 'driver': x[2], 'state': x[3], 'url': x[4], 'swarm': x[5]}),
                machines))

        # return err
        return machines

    def machine_status(self, name):
        output = Popen(['docker-machine', 'status', name], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        out, err = output.communicate()

        s = out.rstrip('\n').lower()
        # if s not in ['running']:
        #     return None

        return s

    def create_machine(self, name, driver_config=None):
        command = ['docker-machine', 'create']

        # if driver_config is None:
        #     command.extend(['--driver', 'none'])
        # else:
        #     for key, value in driver_config.iteritems():
        #         command.extend([key, value])

        # TODO: make args a list
        command.extend(driver_config.args())

        command.append(name)

        output = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        out, err = output.communicate()
        if err is not None:
            raise errors.DockerMachineException(err)
        return out

    def remove_machine(self, name, force=False):
        command = ['docker-machine', 'rm']

        if force:
            command.append('--force')

        command.append(name)

        output = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        out, err = output.communicate()
        return out
