
from vibra import app
from vibra.engine.dissipation_models.porous_materials_models import PorousMaterialModels
from vibra.engine.dissipation_models.viscous_thermal_loss_models import ViscousThermalLossModels
from vibra.engine.transfer_impedances.perforated_plate_models import PerforatedPlateModels
from vibra.engine.mesher.mesh import Mesh
from vibra.engine.properties.fluid import Fluid
from vibra.engine.properties.model_properties import ModelProperties
from vibra.errors import IncompleteSetupError
from vibra.interface.general.print_message_input import PrintMessageInput

import logging
import numpy as np


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
        self.initial_element_size = None

        self.f_min = 2
        self.f_max = 600
        self.f_step = 2
        self.frequencies = None
        self.frequency_setup = dict()
        self.list_frequencies = list()

        self.analysis_data = None
        self.solid_acoustic_element = None
        self.surface_acoustic_element = None
        self.solid_structural_element = None
        self.surface_structural_element = None

        self.properties = ModelProperties()

        self.reset_dissipation_model_properties()

    def reset_dissipation_model_properties(self):
        self.perforated_plate_impedance_data = dict()
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
                self.mesh = Mesh()
                element_size = self.mesh.compute_initial_max_mesh_size(path)
                self.mesh.load_cad(
                                   path,
                                   dimension = 2,
                                   size_factor = 0.08,
                                   minimum_element_size = element_size*0.4,
                                   maximum_element_size = element_size
                                   )

            except:
                self.mesh = Mesh()
                element_size = 10
                self.mesh.load_cad(
                                   path,
                                   dimension = 2,
                                   size_factor = 0.0,
                                   minimum_element_size = element_size*0.5, 
                                   maximum_element_size = element_size
                                   )

            self.initial_element_size = element_size
            self.generated_mesh = False
            app().main_window.update_geometry_information(self.mesh.geometry_information)

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

        logging.info("Processing mesh [80/100]")
        self.mesh.load_cad(self.geometry_path, **self.mesh_setup)
        self.generated_mesh = True

        logging.info("Processing mesh... [90/100]")
        self.mesh._process_solid_elements_connected_to_nodes()

    def set_mesh(self, mesh):
        self.mesh = mesh
        self.generated_mesh = True

    def set_frequency_setup(self, analysis_setup: dict):

        self.frequency_setup.clear()

        self.frequencies = None
        self.f_min = analysis_setup.get("f_min", None)
        self.f_max = analysis_setup.get("f_max", None)
        self.f_step = analysis_setup.get("f_step", None)

        if "frequencies" in analysis_setup.keys():
            self.frequencies = analysis_setup.get("frequencies", None)

        elif (self.f_min, self.f_max, self.f_step).count(None) == 0:

            try:
                self.frequencies = np.arange(self.f_min, self.f_max + self.f_step, self.f_step)
            except:
                self.frequencies = None
                return

        self.frequency_setup = {
                                "f_min" : self.f_min,
                                "f_max" : self.f_max,
                                "f_step" : self.f_step,
                                "frequencies" : self.frequencies
                                }

    def change_analysis_frequency_setup(self, frequencies: list | np.ndarray | None):

        if frequencies is None:
            return False

        if isinstance(frequencies, np.ndarray):
            frequencies = list(frequencies)

        condition_1 = self.list_frequencies == list() 
        condition_2 = not self.properties.check_if_there_are_tables_at_the_model()

        if condition_1 or condition_2:

            # f_min = frequencies[0]
            # f_max = frequencies[-1]
            # f_step = frequencies[1] - frequencies[0]

            # frequency_setup = { "f_min" : float(f_min),
            #                     "f_max" : float(f_max),
            #                     "f_step" : float(f_step) }

            # self.set_frequency_setup(frequency_setup)

            self.list_frequencies = frequencies

            return False

        if self.list_frequencies != frequencies:
            return True

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

    def set_acoustic_element(self, element):
        self.solid_acoustic_element, self.surface_acoustic_element = element

    def set_structural_element(self, element):
        self.solid_structural_element, self.surface_structural_element = element

    def get_acoustic_global_dofs_from_nodes(self, nodes: np.ndarray):
        if self.solid_acoustic_element is None:
            return list()
        _dofs_per_node = self.solid_acoustic_element.DOFS_PER_NODE
        _nodes = nodes.reshape(-1, 1)
        global_dofs = _dofs_per_node * _nodes + np.arange(_dofs_per_node)
        return np.array(global_dofs.flatten(), dtype=int)

    def get_structural_property_data_from_nodes(self, nodes: np.ndarray, data: dict, selection: str):

        output_data = dict()
        if data["element_type"] == "2d_element":
            if self.surface_structural_element is None:
                return output_data
            dofs_per_node = self.surface_structural_element.DOFS_PER_NODE

        else:
            if self.solid_structural_element is None:
                return output_data
            dofs_per_node = self.solid_structural_element.DOFS_PER_NODE

        local_dofs = np.arange(dofs_per_node, dtype=int)
        global_dofs = dofs_per_node * nodes.reshape(-1, 1) + local_dofs

        den = 1
        if "nodal_attribution" in data.keys():

            nodal_attribution = data["nodal_attribution"]
            averaged = data["averaged"]
            if nodal_attribution and averaged:
                den = len(nodes)

            elif not nodal_attribution:
                #TODO: process element integration
                den = 1

                if selection == "surfaces":
                    pass
                elif selection == "lines":
                    pass
                else:
                    pass

        for node_gdofs in global_dofs:
            for j, gdof in enumerate(node_gdofs):

                values = data["values"][j]
                if values is None:
                    continue

                output_data[gdof] = values / den

        return output_data

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

            fluid = self.properties._get_property("fluid", surface=surface_id)
            rho = fluid.fluid_density
        
        elif len(volume_ids) > 1:

            fluids = list()
            for volume_id in volume_ids:
                fluid = self.properties._get_property("fluid", volume=volume_id)
                if isinstance(fluid, Fluid):
                    if fluid not in fluids:
                        fluids.append(fluid)

            if len(fluids) == 1:
                fluid = fluids[0]
                rho = fluid.fluid_density

        return rho

    def process_porous_material_properties(self, frequencies: np.ndarray):

        pm_model = PorousMaterialModels(self)
        pm_model.process_effective_properties(frequencies)

        self.porous_material_properties = dict()
        for volume_id, data in pm_model.effective_properties.items():
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

    def process_viscous_thermal_model_properties(self, frequencies: np.ndarray):

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

    def set_viscous_thermal_model_data(self, data, group=None, volume=None):
        self.properties._set_property("viscous_thermal_model", data, group=group, volume=volume)

    def process_perforated_plate_impendace(self, frequencies: np.ndarray, solution: np.ndarray | None = None):

        pp_model = PerforatedPlateModels(self)
        pp_model.process_acoustic_transfer_impedances(frequencies)

        self.perforated_plate_impedance_data.clear()
        self.perforated_plate_impedance_data = pp_model.perforated_plate_impedance_data

    def process_surface_thickness(self):
        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property == "surface_thickness":
                self.mesh.set_face_element_thickness(surface_id, data)