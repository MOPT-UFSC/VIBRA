import os
from pathlib import Path

from vibra.engine.mesher.mesh import Mesh
from vibra.engine.properties.fluid import Fluid
from vibra.engine.properties.model_properties import ModelProperties
from vibra.errors import IncompleteSetupError
from vibra.interface.general.print_message_input import PrintMessageInput


class ModelStatus:
    materials_setted: bool
    width_setted: bool
    solution_executed: bool


class Model:
    def __init__(self):
        self.reset_variables()
        
    def reset_variables(self):
        #
        self.geometry_path = ""
        self.mesh = None
        self.mesh_setup = None

        self.properties = ModelProperties()
        # self.properties.set_fluid(Fluid("Air", density=1.2, speed_of_sound=343))

    def set_geometry_path(self, path):
        self.geometry_path = Path(path)
    
    def set_properties(self, properties):
        self.properties = properties

    def set_mesh_setup(self, mesh_setup):
        self.mesh_setup = mesh_setup

    def process_visual_geometry_mesh(self):
        self.mesh = Mesh.from_cad(self.geometry_path, dimension=2, size_factor=0.1)

    def process_mesh(self):
        if self.geometry_path == "" or not os.path.exists(self.geometry_path):
            message = "Geometry file not defined"
            context = (
                "The geometry file has not been defined yet."
                "You should to import a supported CAD file format to proceed."
                "\n\n"
                "Suported file formats: *.iges and *.step"
            )
            raise IncompleteSetupError(message, context=context)

        if self.mesh_setup is None:
            message = "Mesh setup not defined"
            context = (
                "The mesh setup has not been defined yet."
                "You should to configure the mesher to proceed."
            )
            raise IncompleteSetupError(message, context=context)
                
        # self.geometry_path = Path("data/examples/script_files/script_hex_elements.txt")
        self.mesh = Mesh.from_cad(self.geometry_path, gmsh_gui=False, **self.mesh_setup)

    def set_material(self, material):
        self.properties.set_material(material)

    def set_fluid(self, fluid):
        self.properties.set_fluid(fluid)