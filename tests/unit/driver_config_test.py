from .api_test import (
    DockerClientTest,
)

from docker_machine.api.driver_config import (
    DigitaloceanDriverConfig
)


class DriverContainerTest(DockerClientTest):

    def test_digitalocean_driver_config(self):
        access_token = 'test_access_token'
        config = DigitaloceanDriverConfig(access_token)
        args = config.args()
        index = args.index('--digitalocean-access-token')
        self.assertEqual(args[index+1], access_token)
