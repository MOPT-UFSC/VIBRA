from typing import Sequence


class VibraException(Exception):
    pass


class MeshException(VibraException):
    def __init__(
        self,
        *args,
        nodes: Sequence | None = None,
        faces: Sequence | None = None,
        solids: Sequence | None = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.nodes = nodes if (nodes is not None) else set()
        self.faces = faces if (faces is not None) else set()
        self.solids = solids if (solids is not None) else set()


class ModelException(VibraException):
    def __init__(
        self,
        *args,
        points: Sequence | None = None,
        surfaces: Sequence | None = None,
        volumes: Sequence | None = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.points = points if (points is not None) else set()
        self.surfaces = surfaces if (points is not None) else set()
        self.volumes = volumes if (points is not None) else set()


class InvalidModelSetupError(ModelException):
    pass


class InvalidModelExcitationError(ModelException):
    pass


class InvalidGeometryForAcousticAnalysisError(ModelException):
    pass


class IncompleteSetupError(ModelException):
    pass
