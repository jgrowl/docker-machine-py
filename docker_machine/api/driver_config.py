class DriverConfig(object):
    def __init__(self, driver):
        self.driver = driver

    def args(self):
        arg_dictionary = dict(map(lambda (k,v): (self._formatKey(k), self._formatVal(v)), vars(self).iteritems()))
        no_none_values = {k: v for k, v in arg_dictionary.items() if v is not None}
        return [item for k in no_none_values for item in (k, no_none_values[k])]

    def _formatKey(self, arg):
        return '--{}-{}'.format(self.driver, arg.replace("_", "-"))

    def _formatVal(self, arg):
        if (isinstance(arg, bool)):
            return 'true' if arg else 'false'

        return arg


class DigitaloceanDriverConfig(DriverConfig):
    def __init__(self, access_token, image='ubuntu-14-04-x64', region='nyc3', ipv6=False, private_networking=False,
                 size='512mb'):
        super(DigitaloceanDriverConfig, self).__init__('digitalocean')
        self.access_token = access_token
        self.image = image
        self.ipv6 = ipv6
        self.region = region
        self.private_networking = private_networking
        self.size = size
