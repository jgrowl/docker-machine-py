class DockerMachineException(Exception):
    pass


class MissingRequiredArgument(DockerMachineException):
    def __init__(self, name):
        self.name = name
