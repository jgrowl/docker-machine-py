from . import api_test
from docker_machine.cli.driver_config import DigitaloceanDriverConfig
from docker_machine.errors import DockerMachineException


class NoDriverMachineTest(api_test.BaseTestCase):
    def setUp(self):
        super(NoDriverMachineTest, self).setUp()
        self.machine_name = 'testNoDriverMachine'
        self.client.create_machine(self.machine_name)

    def test_create_machine_no_driver(self):
        # No Driver has empty status
        self.assertEqual(self.client.machine_status(self.machine_name), '')

        machine = self.client.machine(self.machine_name)
        self.assertEqual(machine.name, self.machine_name)
        self.assertEqual(machine.driver_name, 'none')
        self.assertEqual(machine.machine_status, '')

    def tearDown(self):
        self.client.remove_machine(self.machine_name, force=True)


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
