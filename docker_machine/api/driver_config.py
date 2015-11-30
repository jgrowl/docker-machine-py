class DriverConfig:
    def __init__(self, driver):
        self.driver = driver
        self.args = []

    def _arg(self, arg):
        return '{}-{}'.format(self.driver, arg)

        #
        # def test:
        #     members = [attr for attr in dir(Example()) if not callable(attr) and not attr.startswith("__")]

        # def args(self):
        #     return "{} {} {}".format(self.required_args(), self.extra_args())


class DigitaloceanDriverConfig(DriverConfig):
    def __init__(self, access_token, image='ubuntu-14-04-x64', region='nyc3', ipv6=False, private_networking=False,
                 size='512mb'):
        super(DigitaloceanDriverConfig, self).__init__('digitalocean')

        self.args = ['access_token', 'image', 'region', 'ipv6', 'region', 'private_networking', 'size']
        self.access_token = access_token
        self.image = image
        self.ipv6 = ipv6
        self.region = region
        self.private_networking = private_networking
        self.size = size

        # def required_args(self):
        #     return '--access-token={} {}'.format(self.access_token, super(DigitaloceanDriverConfig, self).required_args())
        #
        # def extra_args(self):
        #     return ''
