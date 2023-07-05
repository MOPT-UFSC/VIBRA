from pathlib import Path

from vibra.engine.mesher.mesh import Mesh


class ModelStatus:
    materials_setted: bool
    width_setted: bool
    solution_executed: bool


class Model:
    def __init__(self):
        self.mesh_setup = None
        self.geometry_path = ""

    def set_geometry_path(self, path):
        self.geometry_path = Path(path)

    def set_mesh_setup(self, mesh_setup):
        self.mesh_setup = mesh_setup

    def process_visual_geometry_mesh(self):
        self.mesh = Mesh.from_cad(self.geometry_path, dimension=2, size_factor=0.1)

    def load_mesh(self):
        if self.mesh_setup is not None:
            self.mesh = Mesh.from_cad(self.geometry_path, **self.mesh_setup)
        else:
            raise Exception("Mesh setup not defined!")