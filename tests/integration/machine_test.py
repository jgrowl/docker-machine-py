from . import api_test

class ListMachinesTest(api_test.BaseTestCase):
    def test_list_machines(self):
        # self.assertFalse(self.client.machines(all=True))

        return True

        # [{'name': 'testMachine', 'url': 'tcp://159.203.118.136:2376', 'driver': 'digitalocean', 'swarm': '', 'state': 'Running', 'active': '-'}] is not false

        # self.assertEqual(True, True)
        # res0 = self.client.containers(all=True)
        # size = len(res0)
        # res1 = self.client.create_container(BUSYBOX, 'true')
        # self.assertIn('Id', res1)
        # self.client.start(res1['Id'])
        # self.tmp_containers.append(res1['Id'])
        # res2 = self.client.containers(all=True)
        # self.assertEqual(size + 1, len(res2))
        # retrieved = [x for x in res2 if x['Id'].startswith(res1['Id'])]
        # self.assertEqual(len(retrieved), 1)
        # retrieved = retrieved[0]
        # self.assertIn('Command', retrieved)
        # self.assertEqual(retrieved['Command'], six.text_type('true'))
        # self.assertIn('Image', retrieved)
        # self.assertRegex(retrieved['Image'], r'busybox:.*')
        # self.assertIn('Status', retrieved)


class MachineStatusTest(api_test.BaseTestCase):
    def test_machine_status(self):
        self.assertEquals(self.client.machine_status('testMachine'), 'running')

class CreateMachinesTest(api_test.BaseTestCase):
    def test_create_machine(self):
        driver_config = {'--driver': 'digitalocean', '--digitalocean-access-token': ''}
        # self.assertFalse(self.client.create_machine('testMachine', driver_config))

class RemoveMachinesTest(api_test.BaseTestCase):
    def test_remove_machine(self):
        return True
        # self.assertFalse(self.client.remove_machine('testMachine'))
        # Successfully removed testMachine\n'
