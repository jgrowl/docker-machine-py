from .api_test import (
    DockerClientTest,
)

from docker_machine.cli.driver_config import (
    DigitaloceanDriverConfig
)

from docker_machine.errors import (
    MissingRequiredArgument
)


class DriverContainerTest(DockerClientTest):

    def test_digitalocean_driver_config_requires_access_token(self):
        self.assertRaises(MissingRequiredArgument, DigitaloceanDriverConfig)

    def test_digitalocean_driver_config(self):
        access_token = 'test_access_token'
        config = DigitaloceanDriverConfig(access_token)
        args = config.args()
        index = args.index('--digitalocean-access-token')
        self.assertEqual(args[index+1], access_token)
