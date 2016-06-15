import os

from docker.machine.driver_description import DRIVER_DESCRIPTIONS


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

    @staticmethod
    def _format_key(arg):
        return '--{}'.format(arg.replace("_", "-"))

    def _format_driver_key(self, arg):
        return '--{}-{}'.format(self.driver, arg.replace("_", "-"))

    @staticmethod
    def _format_val(arg):
        if isinstance(arg, bool):
            return 'true' if arg else 'false'
        return arg

    @staticmethod
    def _lookup_arg(arg, env_var=None, default=None):
        if arg is not None:
            return arg

        return default if env_var is None else os.environ.get(env_var, default)

    def _require(self, tuples):
        for t in tuples:
            if self._lookup_arg(t[1], t[2]) is None:
                raise ValueError('Missing required argument: {} for driver {}'.format(t[0], self.driver))


def list_supported_drivers():
    return list(DRIVER_DESCRIPTIONS.keys())
