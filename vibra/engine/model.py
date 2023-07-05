from pathlib import Path

from vibra.engine.mesher.mesh import Mesh
from vibra.engine.properties.model_properties import ModelProperties
from vibra.engine.properties.fluid import Fluid


class ModelStatus:
    materials_setted: bool
    width_setted: bool
    solution_executed: bool


class Model:
    def __init__(self):
        self.geometry_path = ""
        self.mesh_setup = None
        self.mesh = None

        self.properties = ModelProperties()
        self.properties.set_fluid(Fluid("Air?", density=1.2, speed_of_sound=343))

    def set_geometry_path(self, path):
        self.geometry_path = Path(path)

    def set_mesh_setup(self, mesh_setup):
        self.mesh_setup = mesh_setup

    def process_visual_geometry_mesh(self):
        self.mesh = Mesh.from_cad(self.geometry_path, dimension=2, size_factor=0.1)

    def load_mesh(self):
        if self.mesh_setup is None:
            raise Exception("Mesh setup not defined!")

        self.mesh = Mesh.from_cad(self.geometry_path, **self.mesh_setup)
