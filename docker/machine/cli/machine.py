import docker.machine
import inspect


class Machine(object):

    @classmethod
    def default_client(cls):
        return docker.machine.CLIENT

    @classmethod
    def docker_machine_version(cls):
        return cls.default_client().version().val()

    @classmethod
    def all_docker_machines(cls):
        machine_names = cls.all_docker_machine_names()
        return map(cls, machine_names) if machine_names is not None else list()

    @classmethod
    def active_docker_machine_names(cls):
        return cls.default_client().active().val()

    @classmethod
    def active_docker_machines(cls):
        machine_names = cls.default_client().active().val()
        return map(cls, machine_names) if machine_names is not None else list()

    @classmethod
    def all_docker_machine_names(cls):
        return cls.default_client().ls(quiet=True).val()

    def __init__(self, name, client=None):
        self.name = name
        self.client = self.default_client() if client is None else client

        if self.exists():
            self._initialize()
        else:
            self.inspection = None

    def __getattr__(self, name):
        if hasattr(self.client, name):
            def wrapper(*args, **kw):
                fun_name = getattr(self.client, name)
                argspec = inspect.getargspec(fun_name)

                client_output = None
                if 'machine_name' in argspec.args:
                    args = (self.name,) + args
                    client_output = getattr(self.client, name)(*args, **kw)
                elif argspec.varargs == 'machine_names':
                    args = args + (self.name,)
                    client_output = getattr(self.client, name)(*args, **kw)

                after_callback = '_after_{}'.format(name)
                if hasattr(self, after_callback):
                    getattr(self, after_callback)()

                return self if client_output.formatted is None else client_output.formatted
            return wrapper

        try:
            return getattr(self.inspection, name)
        except AttributeError:
            raise AttributeError("Machine object has no attribute '{}'".format(name))

    def __eq__(self, other):
        return self.name == other.name

    def exists(self):
        return len(self.client.ls(quiet=True, filters='name={}'.format(self.name)).formatted) != 0

    def _after_create(self):
        self._initialize()

    def _initialize(self):
        self.inspection = self.client.inspect(self.name, snake_case=True, named_tuple=True).formatted
