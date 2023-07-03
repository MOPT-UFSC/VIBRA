from pathlib import Path

from vibra.engine.mesher.mesh import Mesh


class ModelStatus:
    materials_setted: bool
    width_setted: bool
    solution_executed: bool


class Model:
    def __init__(self, geometry_path):
        self.geometry_path = geometry_path

        self.mesh = Mesh.from_cad(Path(geometry_path), dimention=2, size_factor=0.05)
