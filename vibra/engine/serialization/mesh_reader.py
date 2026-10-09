from pathlib import Path

from vibra.engine.mesher.mesh import Mesh


class MeshReader:
    def read_mesh(self, path: Path | str) -> Mesh:
        mesh = Mesh().load_mesh(path)
        return mesh
