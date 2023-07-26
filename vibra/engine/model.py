import os
import numpy as np
from pathlib import Path

from vibra.engine.mesher.mesh import Mesh
from vibra.engine.properties.fluid import Fluid
from vibra.engine.properties.model_properties import ModelProperties
from vibra.errors import IncompleteSetupError
from vibra.interface.general.print_message_input import PrintMessageInput

from vibra.engine.assemblers.acoustic_modal_assembler import AcousticModalAssembler
from vibra.engine.assemblers.structural_modal_assembler import StructuralModalAssembler


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
        self.generated_mesh = False
        
        self.frequencies = None
        self.acoustic_element = None
        self.structural_element = None

        self.lines_with_prescribed_dofs = {}
        self.surfaces_with_prescribed_dofs = {}
        self.volumes_with_prescribed_dofs = {}

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
        self.generated_mesh = False

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
        self.generated_mesh = True

    def set_material(self, material):
        self.properties.set_material(material)

    def set_fluid(self, fluid):
        self.properties.set_fluid(fluid)

    def set_acoustic_element(self, element):
        self.acoustic_element = element

    def set_structural_element(self, element):
        self.structural_element = element

    def get_acoustic_global_dofs_from_nodes(self, nodes):
        if self.acoustic_element is None:
            return []
        _dofs_per_node = self.acoustic_element.DOF_PER_NODE
        _nodes = nodes.reshape(-1, 1)
        global_dofs = _dofs_per_node*_nodes + np.arange(_dofs_per_node)
        return np.array(global_dofs.flatten(), dtype=int)
            
    def get_structural_global_dofs_from_nodes(self, nodes):
        if self.structural_element is None:
            return []
        _dofs_per_node = self.structural_element.DOF_PER_NODE
        _nodes = nodes.reshape(-1, 1)
        global_dofs = _dofs_per_node*_nodes + np.arange(_dofs_per_node)
        return np.array(global_dofs.flatten(), dtype=int)

    def set_structural_boundary_condition(self, data):
        try:
            
            if "line" in data["entity_type"]:
                for _id in data["entity_ids"]:
                    self.lines_with_prescribed_dofs[_id] = data["values"]

            if "surface" in data["entity_type"]:
                for _id in data["entity_ids"]:
                    self.surfaces_with_prescribed_dofs[_id] = data["values"]

        except Exception as error_log:
            print(str(error_log))