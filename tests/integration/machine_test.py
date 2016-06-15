import os
import unittest

from docker.machine.cli.machine import Machine
from docker.machine.errors import CLIError
from docker.machine.cli.client import Status

digitalocean_access_token = os.environ.get('DOCKERMACHINEPY_DIGITALOCEAN_ACCESS_TOKEN')


class BaseTestCases:
    class MachineDriverBaseTest(unittest.TestCase):
        def __init__(self, machine_name, driver=None, driver_config={}, *args, **kwargs):
            unittest.TestCase.__init__(self, *args, **kwargs)

            self.machine_name = machine_name
            self.driver = driver
            self.driver_config = driver_config

            self.machine = Machine(self.machine_name)
            self.assertFalse(self.machine.exists())
            self.assertEqual(self.machine.create(), self.machine)
            self.assertTrue(self.machine.exists())

        def setUp(self):
            super(BaseTestCases.MachineDriverBaseTest, self).setUp()
            self.machine = Machine(self.machine_name)

        def test_version(self):
            version_info = self.machine.docker_machine_version()
            self.assertIsNotNone(version_info.version_number)
            self.assertIsNotNone(version_info.version_hash)

        def test_active_docker_machines(self):
            self.assertEqual(0, len(Machine.active_docker_machines()))
            self.assertEqual(self.machine, Machine.all_docker_machines()[0])

        def test_url(self):
            self.assertEqual(self.machine.url(), self.machine.driver.url)

        def test_status(self):
            self.assertEqual(self.machine.status(), Status.running)

        def test_running(self):
            self.assertTrue(self.machine.running())

        def test_paused(self):
            self.assertFalse(self.machine.paused())

        def test_stopped(self):
            self.assertFalse(self.machine.stopped())

        def test_stopping(self):
            self.assertFalse(self.machine.stopping())

        def test_starting(self):
            self.assertFalse(self.machine.starting())

        def test_error(self):
            self.assertFalse(self.machine.error())

        def test_timeout(self):
            self.assertFalse(self.machine.timeout())

        def test_runningish(self):
            self.assertTrue(self.machine.runningish())

        def test_stoppedish(self):
            self.assertFalse(self.machine.stoppedish())

        def test_errorish(self):
            self.assertFalse(self.machine.errorish())

        def tearDown(self):
            try:
                self.machine.rm(force=True)
            except CLIError:
                pass

    class MachineDriverTest(MachineDriverBaseTest):
        def __init__(self, machine_name, driver=None, driver_config={}, *args, **kwargs):
            super(BaseTestCases.MachineDriverTest, self).__init__(machine_name, driver, driver_config, *args, **kwargs)

        # def test_tmp_test(self):
        #     self.machine.create(self.driver, **self.driver_config)
        #     self.machine.ip()
        #     pass
        # def test_machine_test(self):
        #     self.assertFalse(self.machine.exists())
        #     self.machine.create(self.driver, **self.driver_config)
        #     self.assertTrue(self.machine.exists())
        #     self.assertEqual(self.machine, Machine.all()[0])
        #     self.machine.rm(force=True)
        #     self.assertFalse(self.machine.exists())


class NoDriverMachineTest(BaseTestCases.MachineDriverBaseTest):
    def __init__(self, *args, **kwargs):
        super(NoDriverMachineTest, self).__init__('noDriverMachineTest', None, {}, *args, **kwargs)

    def test_ip(self):
        self.assertEqual(self.machine.ip(), '127.0.0.1')

    def test_ssh(self):
        with self.assertRaises(CLIError):
            self.machine.ssh()

        with self.assertRaises(CLIError):
            self.machine.ssh('ls -lah')

    def test_config(self):
        with self.assertRaises(CLIError):
            self.machine.config()

    def test_restart(self):
        with self.assertRaises(CLIError):
            self.machine.restart()

    def test_env(self):
        with self.assertRaises(CLIError):
            self.machine.env()

    def test_stop(self):
        with self.assertRaises(CLIError):
            self.machine.stop()

    def test_start(self):
        with self.assertRaises(CLIError):
            self.machine.start()

    def test_kill(self):
        with self.assertRaises(CLIError):
            self.machine.kill()

        # # def inspect(self, format=None, snake_case=False, named_tuple=False):
        # #     return self.client().inspect(self.name, format, snake_case, named_tuple)
        # #
        # # def scp(self, src, dest, recursive=False):
        # #     return self.client().scp(src, dest, recursive)
        # #
        # self.machine.scp()

    # @unittest.skip('Slow test')
    # def test_regenerate_certs(self):
    #     with self.assertRaises(CLIError):
    #         self.machine.regenerate_certs()
    #
    # @unittest.skip('Slow test')
    # def test_upgrade(self):
    #     with self.assertRaises(CLIError):
    #         self.machine.upgrade()

    def tearDown(self):
        try:
            self.assertEqual(self.machine.rm(force=True), self.machine)
            self.assertFalse(self.machine.exists())
        except CLIError:
            pass


class DigitaloceanMachineTest(BaseTestCases.MachineDriverTest if digitalocean_access_token is not None
                              else BaseTestCases.MachineDriverBaseTest):
    def __init__(self, *args, **kwargs):
        driver = 'digitalocean'
        params = dict(access_token=digitalocean_access_token)
        super(DigitaloceanMachineTest, self).__init__('digitaloceanMachineTest', driver, params, *args, **kwargs)

    def test_missing_required_parameter(self):
        with self.assertRaises(ValueError):
            Machine('missingRequiredParameterTestMachine').create(self.driver)

    def test_invalid_access_token(self):
        with self.assertRaises(CLIError):
            Machine('invalidAccessTokenTestMachine').create(self.driver, access_token='INVALID_ACCESS_TOKEN')

