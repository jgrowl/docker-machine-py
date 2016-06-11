import os
from .. import errors

DRIVER_DESCRIPTIONS = {
    'none': {'non_driver_keys': ['url']},
    'digitalocean': {'required': [('access_token', 'DIGITALOCEAN_ACCESS_TOKEN')]},
    'amazonec2': {'required': [
        ('access_key', 'AWS_ACCESS_KEY_ID'),
        ('secret_key', 'AWS_SECRET_ACCESS_KEY'),
        ('vpc_id', 'AWS_VPC_ID')]},
    'azure': {'required': [('subscription_id', 'AZURE_SUBSCRIPTION_ID'), ('subscription_cert', 'AZURE_SUBSCRIPTION_CERT')]},
    'exoscale': {'required': [('api_key', 'EXOSCALE_API_KEY'), ('api_secret_key', 'EXOSCALE_API_SECRET')]},
    'google': {'required': [('project', 'GOOGLE_PROJECT')]},
    'generic': {'required': [('ip_address', None)]},
    'hyperv': {},
    'openstack': {},
    'rackspace': {'required': [
        ('username', 'OS_USERNAME'),
        ('api_key', 'OS_API_KEY'),
        ('region', 'OS_REGION_NAME')]},
    'softlayer': {'required': [
        ('user', 'SOFTLAYER_USER'),
        ('api_key', 'SOFTLAYER_API_KEY'),
        ('domain', 'SOFTLAYER_DOMAIN')]},
    'virtualbox': {},
    'vmwarevcloudair': {'required': [
        ('username', 'VCLOUDAIR_USERNAME'),
        ('password', 'VCLOUDAIR_PASSWORD')]},
    'vmwarefusion': {},
    'vmwarevsphere': {'required': [
        ('username', 'VSPHERE_USERNAME'),
        ('password', 'VSPHERE_PASSWORD')]}
}


class DriverConfig(object):
    def __init__(self, driver, **kwargs):
        self.driver = 'none' if driver is None else driver
        driver_description = DRIVER_DESCRIPTIONS[self.driver]
        required_args = []
        if 'required' in driver_description:
            for tuple in driver_description['required']:
                required_arg_name = tuple[0]
                required_arg_env_var = tuple[1]
                required_arg_value = kwargs[required_arg_name] if required_arg_name in kwargs else None
                required_args.append((required_arg_name, required_arg_value, required_arg_env_var))

        self.non_driver_keys = ['driver']
        if 'non_driver_keys' in driver_description:
            for key in driver_description['non_driver_keys']:
                self.non_driver_keys.append(key)

        self._require(required_args)

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def args(self):
        arg_dictionary = {}
        config_vars = dict(vars(self))
        del config_vars['non_driver_keys']
        for k, v in config_vars.iteritems():
            key = self._format_key(k) if k in self.non_driver_keys else self._format_driver_key(k)
            value = self._format_val(v)
            arg_dictionary[key] = value

        no_none_values = {k: v for k, v in arg_dictionary.items() if v is not None}
        return ["{}={}".format(k, v) for k, v in no_none_values.iteritems()]

    def _format_key(self, arg):
        return '--{}'.format(arg.replace("_", "-"))

    def _format_driver_key(self, arg):
        return '--{}-{}'.format(self.driver, arg.replace("_", "-"))

    def _format_val(self, arg):
        if (isinstance(arg, bool)):
            return 'true' if arg else 'false'
        return arg

    def _lookup_arg(self, arg, env_var=None, default=None):
        if arg is not None:
            return arg

        return default if env_var is None else os.environ.get(env_var, default)

    def _require(self, tuples):
        for tuple in tuples:
            if self._lookup_arg(tuple[1], tuple[2]) is None:
                raise errors.MissingRequiredArgument(tuple[0])


def list_supported_drivers():
    return list(DRIVER_DESCRIPTIONS.keys())
