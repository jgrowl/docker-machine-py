import unittest

import docker.machine
from docker.machine.errors import DockerMachineException


class BaseTestCases:
    class DriverTest(unittest.TestCase):
        def __init__(self, machine_name, driver=None, driver_config={}, *args, **kwargs):
            unittest.TestCase.__init__(self, *args, **kwargs)

            self.machine_name = machine_name
            self.driver = driver
            self.driver_config = driver_config
            self.client = docker.machine.Client()

        def setUp(self):
            self.client.create(self.machine_name, self.driver, **self.driver_config)

        def test_create_use_and_destroy(self):
            self.client.version()
            self.client.help()
            self.client.active()
            self.client.inspect(self.machine_name)
            self.client.ip(self.machine_name)
            self.client.ls()
            self.client.restart(self.machine_name)
            self.client.status(self.machine_name)
            self.client.url(self.machine_name)

        def tearDown(self):
            try:
                self.client.rm(self.machine_name, force=True)
            except DockerMachineException:
                pass


# class NoDriverMachineTest(unittest.TestCase):
#     # def __init__(self, *args, **kwargs):
#     #     unittest.TestCase.__init__(self, *args, **kwargs)
#     #     pass
#
#     def setUp(self):
#         self.client.create(self.machine_name, self.driver, **self.driver_config)
#
#     def test_create_use_and_destroy(self):
#         self.client.version()
#         self.client.help()
#
#         self.client.create(self.machine_name, self.driver, **self.driver_config)
#         self.client.active()
#         inspection = self.client.inspect(self.machine_name)
#         url = self.client.url(self.machine_name)
#         self.assertEqual(url, url)
#         self.client.ip(self.machine_name)
#         self.client.ls()
#         self.client.restart(self.machine_name)
#         self.client.status(self.machine_name)
#
#     def tearDown(self):
#         try:
#             self.client.rm(self.machine_name, force=True)
#         except DockerMachineException:
#             pass


# class NoDriverMachineTest(BaseTestCases.DriverTest):
#     def __init__(self, *args, **kwargs):
#         super(NoDriverMachineTest, self).__init__('noDriverMachineTest', None, {}, *args, **kwargs)
#
#         #     # # No Driver has empty status
#         #     # self.assertEqual(self.client.machine_status(self.machine_name), '')
#         #     #
#         #     # machine = self.client.machine(self.machine_name)
#         #     # self.assertEqual(machine.name, self.machine_name)
#         #     # self.assertEqual(machine.driver_name, 'none')
#         #     # self.assertEqual(machine.machine_status, '')


# class DigitaloceanDriverMachineTest(api_test.BaseTestCase):
#     def setUp(self):
#         super(DigitaloceanDriverMachineTest, self).setUp()
#         self.machine_name = 'testCreateDigitaloceanDriverMachine'
#         # self.client.create_machine(self.machine_name)
#
#     def test_create_machine_digitalocean_driver(self):
#
#         config = DigitaloceanDriverConfig(access_token='BAD_TOKEN', region='nyc3', private_networking='true')
#         self.client.create_machine(self.machine_name, config)
#
#         # self.assertRaises(DockerMachineException, self.client.create_machine, self.machine_name, DigitaloceanDriverConfig(access_token='BAD_TOKEN'))
#
#         # self.assertEqual(self.client.machine_status(self.machine_name), '')
#         #
#         # machine = self.client.machine(self.machine_name)
#         # self.assertEqual(machine.name, self.machine_name)
#         # self.assertEqual(machine.driver_name, 'none')
#         # self.assertEqual(machine.machine_status, '')
#
#     # def tearDown(self):
#     #     self.client.remove_machine(self.machine_name, force=True)
