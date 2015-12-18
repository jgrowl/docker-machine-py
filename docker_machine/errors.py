class DockerMachineException(Exception):
    pass


class MissingRequiredArgument(Exception):
    def __init__(self, arg_name):
        self.arg_name = arg_name


class UnknownDriverException(DockerMachineException):
    pass
