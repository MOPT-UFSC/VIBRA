class VibraException(Exception):
    def __init__(self, message, context=""):
        super().__init__(message)
        self.context = context


class IncompleteSetupError(VibraException):
    pass


class IncompleteMeshSetup(VibraException):
    pass


class MeshError(VibraException):
    pass


class UnsuportedFileError(VibraException):
    pass
