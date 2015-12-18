class DockerMachineException(Exception):
    pass

# class DockerMachineException(Exception):
#     pass


class MissingRequiredArgument(Exception):
    pass


class UnknownDriverException(DockerMachineException):
    pass
