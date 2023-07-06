from pathlib import Path
import os

from vibra.engine.mesher.mesh import Mesh
from vibra.engine.properties.model_properties import ModelProperties
from vibra.engine.properties.fluid import Fluid
from vibra.interface.general.print_message_input import PrintMessageInput


class ModelStatus:
    materials_setted: bool
    width_setted: bool
    solution_executed: bool


class Model:
    def __init__(self):
        #
        self.material = None
        self.fluid = None
        self.mesh = None
        self.mesh_setup = None
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

    def process_mesh(self):
        #
        if self.geometry_path == "" or not os.path.exists(self.geometry_path):
            window_title = "ERROR"
            title = "Geometry file not defined"
            message = "The geometry file has not been defined yet. You should to import a supported CAD file format to proceed."
            message += "\n\n Suported file formats: *.iges and *.step"
            PrintMessageInput([title, message, window_title])
            return
        #
        if self.mesh_setup is None:
            window_title = "ERROR"
            title = "Mesh setup not defined"
            message = "The mesh setup has not been defined yet. You should to configure the mesher to proceed."
            PrintMessageInput([title, message, window_title])
            return
        #
        self.mesh = Mesh.from_cad(self.geometry_path, **self.mesh_setup)

    def set_material(self, material):
        self.material = material

    def set_fluid(self, fluid):
        self.fluid = fluid
    
