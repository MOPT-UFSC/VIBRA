from pathlib import Path

from vibra.engine.mesher.mesh import Mesh


class OccMesher:
    def __init__(self, path: str | Path | None = None):
        self.reset()
        if path is not None:
            self.set_path(path)

    def reset(self):
        self.path: Path | None = None

    def set_path(self, path: str | Path):
        self.path = Path(path).expanduser()

    def generate(self, threads: int = 0) -> Mesh:
        return Mesh()
