import os
import logging
from pathlib import Path

import numpy as np

from vibra.engine.mesher.geometry_setup import GeometrySetup
from vibra.engine.mesher.mesh import Mesh
from vibra.engine.properties.model_properties import ModelProperties
from vibra.errors import IncompleteSetupError
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.utils.progress_status import ProgressStatus


class ModelStatus:
    materials_setted: bool
    width_setted: bool
    solution_executed: bool


class Model:
    def __init__(self):
        self.reset_variables()

    def reset_variables(self):
        #
        self.geometry_path = Path("")
        self.mesh = None
        self.mesh_setup = None
        self.generated_mesh = False
        self.surfaces_areas = dict()

        self.analysis_data = None
        self.solid_acoustic_element = None
        self.surface_acoustic_element = None
        self.solid_structural_element = None
        self.surface_structural_element = None

        self.properties = ModelProperties()

    def set_geometry_path(self, path):
        self.geometry_path = Path(path)

    def set_properties(self, properties):
        self.properties = properties

    def set_mesh_setup(self, mesh_setup):
        self.mesh_setup = mesh_setup

    def process_visual_geometry_mesh(self):
        self.mesh = Mesh.from_cad(self.geometry_path, dimension=2, size_factor=0.2)
        self.surfaces_areas = self.mesh.get_model_areas(self.geometry_path)
        self.generated_mesh = False

    def process_mesh(self):
        if not self.geometry_path.exists():
            message = "Geometry not defined"
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

        if self.mesh is None:
            self.mesh = Mesh.from_cad(self.geometry_path)

        # self.geometry_path = Path("data/examples/script_files/script_hex_elements.txt")
        # self.mesh = Mesh.from_cad(self.geometry_path, gmsh_gui=True, **self.mesh_setup)

        self.mesh.update_parameters(**self.mesh_setup)
        self.generated_mesh = True

        logging.info("Renumbering nodes..." + ProgressStatus(90, 100))
        self.mesh._process_nodes_reordering()

    def set_material(self, material):
        self.properties.set_material(material)

    def set_fluid(self, fluid):
        self.properties.set_fluid(fluid)

    def set_acoustic_element(self, element):
        self.solid_acoustic_element, self.surface_acoustic_element = element

    def set_structural_element(self, element):
        self.solid_structural_element, self.surface_structural_element = element

    def get_acoustic_global_dofs_from_nodes(self, nodes):
        if self.solid_acoustic_element is None:
            return []
        _dofs_per_node = self.solid_acoustic_element.DOF_PER_NODE
        _nodes = nodes.reshape(-1, 1)
        global_dofs = _dofs_per_node * _nodes + np.arange(_dofs_per_node)
        return np.array(global_dofs.flatten(), dtype=int)

    def get_structural_global_dofs_from_nodes(self, nodes):
        if self.solid_structural_element is None:
            return []
        _dofs_per_node = self.solid_structural_element.DOF_PER_NODE
        _nodes = nodes.reshape(-1, 1)
        global_dofs = _dofs_per_node * _nodes + np.arange(_dofs_per_node)
        return np.array(global_dofs.flatten(), dtype=int)

    # Properties can be accessed from outside, so this "indirection layer" is not needed
    def set_dissipation_model_data(self, data):
        self.properties.set_dissipation_model(data)

    def set_lrf_eq_model_data(self, data, surface=None, volume=None):
        self.properties.set_lrf_eq_model_data(data, surface=surface, volume=volume)

    def set_structural_boundary_condition(self, data, line, surface):
        self.properties.set_structural_boundary_condition(data, line, surface)

    def set_structural_load(self, data, line, surface):
        self.properties.set_structural_load(data, line, surface)

    def set_acoustic_pressure(self, data, surface):
        self.properties.set_acoustic_pressure(data, surface)

    def set_mass_flow_rate(self, data, surface):
        self.properties.set_mass_flow_rate(data, surface)

    def set_volume_velocity(self, data, surface):
        self.properties.set_volume_velocity(data, surface)

    def set_surface_velocity(self, data, surface):
        self.properties.set_surface_velocity(data, surface)

    def set_specific_impedance(self, data, surface):
        self.properties.set_specific_impedance(data, surface)