from pathlib import Path
from vibra.engine.mesh import Mesh


class ModelStatus:
    materials_setted: bool
    width_setted: bool
    solution_executed: bool


class Model:
    def __init__(self, geometry_path):
        self.geometry_path = geometry_path

        self.visualization_mesh = Mesh.from_file(Path(geometry_path))
        self.simulation_mesh = self.visualization_mesh
