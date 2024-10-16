import os
import logging
from pathlib import Path
from collections import defaultdict

import numpy as np
from scipy.special import jv

from vibra import app
from vibra.interface.loading_bar import load_function
from vibra.engine.dissipation_models.low_reduced_frequency_model import LowReducedFrequencyModel
from vibra.engine.dissipation_models.porous_materials_models import PorousMaterialModels
from vibra.engine.dissipation_models.viscous_thermal_loss_models import ViscousThermalLossModels
from vibra.engine.mesher.mesh import Mesh
from vibra.engine.properties.model_properties import ModelProperties
from vibra.errors import IncompleteSetupError
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.utils.progress_status import ProgressStatus

window_title_1 = "Error"
window_title_2 = "Warning"


class ModelStatus:
    materials_setted: bool
    width_setted: bool
    solution_executed: bool


class Model:
    def __init__(self):
        self.reset_variables()

    def reset_variables(self):

        self.mesh = None
        self.mesh_setup = None
        self.generated_mesh = False
        self.geometry_path = None

        self.analysis_data = None
        self.solid_acoustic_element = None
        self.surface_acoustic_element = None
        self.solid_structural_element = None
        self.surface_structural_element = None

        self.properties = ModelProperties()

        self.reset_dissipation_model_properties()

    def reset_dissipation_model_properties(self):
        self.lrf_properties = dict()
        self.porous_material_properties = dict()
        self.viscous_thermal_model_properties = dict()

    def set_geometry_path(self, path : str):
        self.geometry_path = path

    def set_properties(self, properties):
        self.properties = properties

    def set_mesh_setup(self, mesh_setup):
        self.mesh_setup = mesh_setup

    def process_visual_geometry_mesh(self, path : str):

        try:

            try:
                self.mesh = Mesh.from_cad(path, dimension=2, size_factor=0.0, minimum_element_size=10, maximum_element_size=40)
            except:
                self.mesh = Mesh.from_cad(path, dimension=2, size_factor=0.0, minimum_element_size=5, maximum_element_size=30)

            self.generated_mesh = False

        except Exception as error_log:
            title = "Error while processing geometry"
            message = str(error_log)
            PrintMessageInput([window_title_1, title, message])
            return -1       

    def process_mesh(self):

        if self.geometry_path is None:
            message = "Geometry not defined"
            context = ( "The geometry file has not been defined yet."
                        "You should to import a supported CAD file format to proceed."
                        "\n\n"
                        "Suported file formats: *.iges and *.step" )
            raise IncompleteSetupError(message, context=context)

        if self.mesh_setup is None:
            message = "Mesh setup not defined"
            context = ( "The mesh setup has not been defined yet."
                        "You should to configure the mesher to proceed." )
            raise IncompleteSetupError(message, context=context)

        # if self.mesh is None:
        #     self.mesh = Mesh.from_cad(self.geometry_path)

        self.mesh.load_cad(self.geometry_path, **self.mesh_setup)
        self.generated_mesh = True

        logging.info("Processing mesh..." + ProgressStatus(90, 100))
        self.mesh._process_solid_elements_connected_to_nodes()

        # logging.info("Renumbering nodes..." + ProgressStatus(90, 100))
        # self.mesh._process_nodes_reordering()

    def set_material(self, material, **kwargs):
        self.properties.set_material(material, **kwargs)

    def set_fluid(self, fluid, **kwargs):
        self.properties.set_fluid(fluid, **kwargs)

    def set_mesh(self, mesh):
        self.mesh = mesh
        self.generated_mesh = True

    def get_volume(self, **kwargs):
        """ This method returns the volume based on kwargs. """
        volume = kwargs.get("volume", None)
        if volume is None:
            try:
                element = kwargs.get("element", None) 
                volume = self.mesh.volume_from_element[element]
            except:
                # temporary solution to allow running external mesh file
                volume = 1
        return volume

    def get_fluid(self, **kwargs):
        """ This method returns the fluid relative to an element or volume and the volume id itself. """
        volume = self.get_volume(**kwargs)
        fluid = self.properties.get_fluid(volume=volume)
        return fluid, volume

    def get_fluid_properties(self, proportional_damping=False, **kwargs):
        """ This method returns the fluid properties """
        fluid, volume = self.get_fluid(**kwargs)
        dynamic_viscosity = fluid.dynamic_viscosity
        if proportional_damping:
            c_0 = self.properties.get_speed_of_sound(fluid, volume=volume)
            rho_0 = self.properties.get_fluid_density(fluid, volume=volume)
        else:
            c_0 = fluid.speed_of_sound
            rho_0 = fluid.fluid_density
        return rho_0, c_0, dynamic_viscosity

    def set_acoustic_element(self, element):
        self.solid_acoustic_element, self.surface_acoustic_element = element

    def set_structural_element(self, element):
        self.solid_structural_element, self.surface_structural_element = element

    def get_acoustic_global_dofs_from_nodes(self, nodes):
        if self.solid_acoustic_element is None:
            return list()
        _dofs_per_node = self.solid_acoustic_element.DOF_PER_NODE
        _nodes = nodes.reshape(-1, 1)
        global_dofs = _dofs_per_node * _nodes + np.arange(_dofs_per_node)
        return np.array(global_dofs.flatten(), dtype=int)

    def get_structural_global_dofs_from_nodes(self, nodes):
        if self.solid_structural_element is None:
            return list()
        _dofs_per_node = self.solid_structural_element.DOF_PER_NODE
        _nodes = nodes.reshape(-1, 1)
        global_dofs = _dofs_per_node * _nodes + np.arange(_dofs_per_node)
        return np.array(global_dofs.flatten(), dtype=int)

    def get_fluid_density_for_particle_velocity_calculation(self, surface_id: int, frequencies: np.ndarray):

        rho = None
        volume_ids = self.mesh.volume_from_surface[surface_id]

        if len(volume_ids) == 1:

            for key in self.properties.volume_properties.keys():
                property, volume_id = key
                if volume_id == volume_ids[0]:
                    if property == "viscous_thermal_model":
                        vt_model = ViscousThermalLossModels(self)
                        vt_model.process_effective_properties(frequencies)
                        return vt_model.effective_properties[volume_id]["rho_eff"]

                    elif property == "porous_material_model":
                        pm_model = PorousMaterialModels(self)
                        pm_model.process_effective_properties(frequencies)
                        return pm_model.effective_properties[volume_id]["rho_eff"]

            fluid = self.properties.get_fluid(surface=surface_id)
            rho = fluid.fluid_density

        return rho

    def process_lrf_properties(self, frequencies):

        model = LowReducedFrequencyModel(self)
        model.process_effective_properties(frequencies)

        self.lrf_properties = dict()
        for element_id, data in model.low_reduced_frequency_properties.items():
            self.lrf_properties[element_id] = data

    def process_porous_material_properties(self, frequencies):

        model = PorousMaterialModels(self)
        model.process_effective_properties(frequencies)

        self.porous_material_properties = dict()
        for volume_id, data in model.effective_properties.items():
            for element_id in self.mesh.elements_from_volume[volume_id]:
                self.porous_material_properties[element_id] = data
            # print(len(self.mesh.elements_from_volume[volume_id]))

    def is_porous_material_model_active(self, surface_id):

        for key, data in self.properties.volume_properties.items():
            prop, volume_id = key
            if prop == "porous_material_model":

                if volume_id in self.mesh.surfaces_from_volumes.keys():
                    surfaces_from_volume = self.mesh.surfaces_from_volumes[volume_id]

                    if surface_id in surfaces_from_volume:
                        elements = self.mesh.elements_from_volume[volume_id]
                        rho_eff = self.porous_material_properties[elements[0]]["rho_eff"]
                        C_eff = self.porous_material_properties[elements[0]]["C_eff"]
                        return True, rho_eff, C_eff

        return False, None, None

    def process_viscous_thermal_model_properties(self, frequencies):

        model = ViscousThermalLossModels(self)
        model.process_effective_properties(frequencies)

        self.viscous_thermal_model_properties = dict()
        for volume_id, data in model.effective_properties.items():
            for element_id in self.mesh.elements_from_volume[volume_id]:
                self.viscous_thermal_model_properties[element_id] = data
            # print(len(self.mesh.elements_from_volume[volume_id]))

    def is_viscous_thermal_model_active(self, surface_id):

        for key, data in self.properties.volume_properties.items():
            prop, volume_id = key
            if prop == "viscous_thermal_model":

                if volume_id in self.mesh.surfaces_from_volumes.keys():
                    surfaces_from_volume = self.mesh.surfaces_from_volumes[volume_id]

                    if surface_id in surfaces_from_volume:
                        elements = self.mesh.elements_from_volume[volume_id]
                        rho_eff = self.viscous_thermal_model_properties[elements[0]]["rho_eff"]
                        C_eff = self.viscous_thermal_model_properties[elements[0]]["C_eff"]
                        return True, rho_eff, C_eff

        return False, None, None

    # Properties can be accessed from outside, so this "indirection layer" is not needed
    def set_dissipation_model_data(self, data, volume=None):
        self.properties.set_dissipation_model(data, volume=volume)

    def set_porous_material_model_data(self, data, surface=None, volume=None):
        self.properties.set_porous_material_model_data(data, surface=surface, volume=volume)

    def set_viscous_thermal_model_data(self, data, group=None, volume=None):
        self.properties._set_property("viscous_thermal_model", data, group=group, volume=volume)

    # def set_lrf_eq_model_data(self, data, group=None, volume=None):
    #     self.properties.set_lrf_eq_model_data(data, group=group, volume=volume)

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