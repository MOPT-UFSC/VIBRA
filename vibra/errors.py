from typing import Optional, Sequence


class VibraException(Exception):
    show_traceback: bool = False


class MeshException(VibraException):
    def __init__(
        self,
        *args,
        nodes: Optional[Sequence] = None,
        edges: Optional[Sequence] = None,
        faces: Optional[Sequence] = None,
        solids: Optional[Sequence] = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.nodes = nodes if (nodes is not None) else set()
        self.edges = edges if (edges is not None) else set()
        self.faces = faces if (faces is not None) else set()
        self.solids = solids if (solids is not None) else set()


class ModelException(VibraException):
    def __init__(
        self,
        *args,
        points: Optional[Sequence] = None,
        lines: Optional[Sequence] = None,
        surfaces: Optional[Sequence] = None,
        volumes: Optional[Sequence] = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.points = points if (points is not None) else set()
        self.lines = lines if (lines is not None) else set()
        self.surfaces = surfaces if (surfaces is not None) else set()
        self.volumes = volumes if (volumes is not None) else set()


class SolverSubprocessError(RuntimeError):
    def __init__(
        self,
        returncode: int,
        stderr: str = "",
    ) -> None:
        self.returncode = returncode
        self.stderr = stderr.strip()

        message = f"Subprocess failed with returncode {returncode}"
        super().__init__(message)

    def __str__(self) -> str:
        if self.stderr:
            return self.stderr
        return super().__str__()


class InvalidMaterialError(VibraException):
    pass


class InvalidFluidError(VibraException):
    pass


class InvalidDomainError(VibraException):
    pass


class InvalidModelSetupError(ModelException):
    pass


class InvalidAnalysisSetupError(ModelException):
    pass


class InvalidModelExcitationError(ModelException):
    pass


class InvalidGeometryError(ModelException):
    pass


class IncompleteSetupError(ModelException):
    pass


class MeshingAlgorithmError(MeshException):
    show_traceback = True


class InvalidMeshSetupError(MeshException):
    pass
