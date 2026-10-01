from copy import deepcopy
from pathlib import Path

from vibra.engine.mesher.mesh import Mesh
from vibra.engine.mesher.mesh_setup import MeshSetup


class GmshMesher:
    def __init__(self, path: str | Path | None = None):
        self.setup = MeshSetup()
        self.path: Path | None = None

        if path is not None:
            self.set_path(path)

    def set_path(self, path: str | Path):
        self.path = Path(path).expanduser()

    def configure_mesh(self, setup: MeshSetup):
        self.setup = setup

    def generate(self, threads: int = 0) -> Mesh:
        if self.path is None:
            raise ValueError("Path is not set")

        return Mesh().load_cad(
            self.path,
            deepcopy(self.setup),
            threads,
        )
