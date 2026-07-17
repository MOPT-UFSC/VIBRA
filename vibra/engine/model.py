import logging
from copy import deepcopy
from numbers import Number
from pathlib import Path
from typing import Callable, Optional

import numpy as np
from PIL.Image import Image

from vibra import SUPPORTED_GEOMETRY_EXTENSIONS, errors
from vibra.engine.analysis_info import (
    AnalysisID,
    AnalysisMethod,
    AnalysisSetup,
    FrequencySpacing,
    HarmonicAnalysisSetup,
    ModalAnalysisSetup,
)
from vibra.engine.dissipation_models.porous_materials_models import PorousMaterialModels
from vibra.engine.dissipation_models.viscous_thermal_loss_models import ViscousThermalLossModels

# 1d elements - acoustic
from vibra.engine.elements.elements_1d import ACT_LINE_2, ACT_LINE_3
from vibra.engine.elements.elements_2d import (
    ACT_QUADRANGLE_4,
    ACT_QUADRANGLE_8,
    # 2d elements - acoustic
    ACT_TRIANGLE_3,
    ACT_TRIANGLE_6,
    # 2D elements - structural
    STRUCT_TRIANGLE_3,
)
from vibra.engine.elements.elements_3d import (
    # 3d elements - acoustic
    ACT_HEXAHEDRON_8C,
    ACT_HEXAHEDRON_20C,
    ACT_TETRAHEDRON_4C,
    ACT_TETRAHEDRON_10C,
    # 3d elements - structural
    STRUCT_HEXAHEDRON_8,
    STRUCT_HEXAHEDRON_20,
    STRUCT_TETRAHEDRON_4S,
    STRUCT_TETRAHEDRON_10S,
)
from vibra.engine.geometry.geometry import LengthUnits
from vibra.engine.mesher.degrees_of_freedom_decoupling import DegreesOfFreedomDecoupling
from vibra.engine.mesher.element_setup import GMSH_VISUAL_MESH
from vibra.engine.mesher.mesh import Mesh
from vibra.engine.mesher.mesh_setup import HEXAHEDRON_8, HEXAHEDRON_20, TETRAHEDRON_4, TETRAHEDRON_10, ElementTopology, MeshSetup
from vibra.engine.properties.fluid import Fluid
from vibra.engine.properties.model_properties import ModelProperties
from vibra.engine.solution import HarmonicSolution, Solution
from vibra.engine.transfer_impedances.perforated_plate_models import (
    PerforatedPlateModels,
)
from vibra.errors import IncompleteSetupError
from vibra.interface import error_title
from vibra.interface.general.print_message_input import PrintMessageInput


class Model:
    def __init__(self, disable_resume_callback: Optional[Callable] = None):
        self.disable_resume_callback = disable_resume_callback
        self.reset_variables()

    def reset_variables(self):
        self.name: str = "Model"
        self.thumbnail: Optional[Image] = None

        self.length_unit: LengthUnits = "millimeter"
        self.mesh_setup: Optional[MeshSetup] = None
        self.analysis_setup: Optional[AnalysisSetup] = None
        self.solution: Optional[Solution] = None

        # TODO: review these variables
        self.mesh: Optional[Mesh] = None
        self.stop_processing = False
        self.geometry_path: Optional[Path | str] = None
        self.initial_element_size = None
        self.geometry_qf = 1.0

        self.list_frequencies = list()

        self.decouple_info = dict()
        self.nodes_mapping = dict()

        self.solid_acoustic_element = None
        self.surface_acoustic_element = None

        self.acoustic_element_1d = None
        self.acoustic_element_2d = None
        self.acoustic_element_3d = None

        self.structural_element_1d = None
        self.structural_element_2d = None
        self.structural_element_3d = None

        self.properties = ModelProperties(self.disable_resume_callback)

        self.reset_dissipation_model_properties()

    @property
    def element_topology(self) -> ElementTopology | None:
        if not isinstance(self.mesh, Mesh):
            return

        if self.mesh.element_topology is None:
            self.mesh.update_element_topology_based_on_connectivity()

        return self.mesh.element_topology

    @property
    def analysis_id(self) -> AnalysisID:
        if isinstance(self.analysis_setup, AnalysisSetup):
            return self.analysis_setup.analysis_id

        return AnalysisID.NO_ANALYSIS

    @property
    def frequencies(self) -> Optional[np.ndarray]:
        """
        This property was created for retro compatibility.
        """
        if isinstance(self.analysis_setup, HarmonicAnalysisSetup):
            return self.analysis_setup.get_frequencies()

        return None

    @property
    def solution_steps_mask(self):
        if isinstance(self.analysis_setup, HarmonicAnalysisSetup):
            return self.analysis_setup.solution_steps_mask

        return list()

    @property
    def global_damping(self) -> Optional[np.ndarray]:
        """
        This property was created for retro compatibility.
        """
        if isinstance(self.analysis_setup, HarmonicAnalysisSetup):
            return self.analysis_setup.global_damping

        return (None, None, None)

    @property
    def outdated_solution(self):
        if isinstance(self.analysis_setup, ModalAnalysisSetup | HarmonicAnalysisSetup):
            return self.analysis_setup.outdated_solution

        return False

    @property
    def can_resume_solution(self) -> bool:
        if not isinstance(self.solution, HarmonicSolution):
            return False

        try:
            return not np.all(self.solution.status)
        except Exception:
            return False

    def reset_current_solution(self):
        self.solution = None

    def get_harmonic_analysis_setup(self, **kwargs) -> HarmonicAnalysisSetup:
        analysis_setup = HarmonicAnalysisSetup(**kwargs)
        analysis_setup.solution_steps_mask = self.get_solution_steps_mask(frequencies=analysis_setup.get_frequencies())
        return analysis_setup

    def reset_dissipation_model_properties(self):
        self.perforated_plate_impedance_data = dict()
        self.porous_material_properties = dict()
        self.viscous_thermal_model_properties = dict()

    def set_length_unit(self, length_unit: str = "millimeter"):
        self.length_unit = length_unit

    def set_geometry_quality_factor(self, geometry_qf: float = 1.0):
        self.geometry_qf = geometry_qf

    def set_geometry_path(self, path: Path | str):
        self.geometry_path = path

    def check_path_for_geometry_file(self, path: Path | str):
        """
        This method returns True if a CAD extension file is detected
        in the input path, otherwise, it returns False.
        """

        if isinstance(path, Path):
            path = str(path)

        ext = path.split(".")[-1].lower()
        if ext in SUPPORTED_GEOMETRY_EXTENSIONS:
            return True

        return False

    def set_properties(self, properties):
        self.properties = properties

    def set_mesh_setup(self, mesh_setup: MeshSetup | None):
        self.mesh_setup = mesh_setup

    def initialize_mesh(self):
        self.mesh = Mesh(length_unit=self.length_unit, geometry_qf=self.geometry_qf)

    def process_visual_geometry_mesh(self, path: str):
        self.mesh = Mesh(length_unit=self.length_unit, geometry_qf=self.geometry_qf)

        try:
            try:
                element_size = self.mesh.compute_initial_mesh_size(path)
                mesh_setup = MeshSetup(
                    minimum_element_size=element_size * 0.4,
                    maximum_element_size=element_size,
                    custom_element_setup=GMSH_VISUAL_MESH,
                )
                self.mesh.load_cad(path, mesh_setup)

            except Exception:
                element_size = 10
                mesh_setup = MeshSetup(
                    minimum_element_size=element_size * 0.5,
                    maximum_element_size=element_size,
                    custom_element_setup=GMSH_VISUAL_MESH,
                )

            self.initial_element_size = element_size

        except Exception as error_log:
            from traceback import print_exception

            print_exception(error_log)
            title = "Error while processing geometry"
            message = str(error_log)
            PrintMessageInput([error_title, title, message])
            return -1

    def process_mesh_data(self, path: str):
        self.initialize_mesh()

        try:
            logging.info("Processing mesh... [15/100]")

            self.mesh.geometry_imported = False
            self.mesh.load_mesh(path)

        except Exception as error_log:
            from traceback import print_exception

            print_exception(error_log)
            title = "Error while processing geometry"
            message = str(error_log)
            PrintMessageInput([error_title, title, message])
            return -1

    def process_mesh(self):
        if self.geometry_path is None:
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
            context = "The mesh setup has not been defined yet.You should to configure the mesher to proceed."
            raise IncompleteSetupError(message, context=context)

        logging.info("Processing mesh [80/100]")
        self.mesh = Mesh(length_unit=self.length_unit, geometry_qf=self.geometry_qf)
        self.mesh.load_cad(self.geometry_path, self.mesh_setup)

        if self.disable_resume_callback is not None:
            self.disable_resume_callback()

    def set_analysis_setup(self, analysis_setup: Optional[AnalysisSetup]):
        if not isinstance(analysis_setup, AnalysisSetup | None):
            raise ValueError("Invalid analysis setup")

        self.analysis_setup = analysis_setup

    def get_solution_steps_mask(self, frequencies: np.ndarray | list | None = None, tol: float = 1e-10):

        if frequencies is None:
            frequencies = deepcopy(self.frequencies)

        if frequencies is None:
            return list()

        all_true = [True for _ in range(len(frequencies))]
        table_frequencies = self.properties.process_all_tables_frequencies_vectors()

        if not table_frequencies:
            return all_true

        if len(table_frequencies) != 1:
            return all_true

        mask = list()
        _table_frequencies = np.array(table_frequencies[0], dtype=float)

        for freq in _table_frequencies:
            diff_abs = np.min(np.abs(frequencies - freq)) < tol
            mask.append(bool(diff_abs))

        return mask

    def has_spectral_content_been_modified(self):
        if isinstance(self.analysis_setup, ModalAnalysisSetup):
            return False

        cond_A = self.analysis_setup.frequency_spacing == FrequencySpacing.USER_DEFINED
        cond_B = len(self.solution_steps_mask) != int(sum(self.solution_steps_mask))
        return cond_A or cond_B

    def is_the_mesh_setup_defined(self):
        if isinstance(self.geometry_path, str | Path):
            if self.is_there_a_geometry_imported():
                if not isinstance(self.mesh_setup, MeshSetup):
                    return True

        return False

    def is_there_a_valid_mesh(self):

        if isinstance(self.geometry_path, str | Path):
            if self.is_there_a_geometry_imported():
                if not isinstance(self.mesh_setup, MeshSetup):
                    return False

        disconnected_nodes = bool(self.mesh.disconnected_nodes_data)
        collapsed_elements = bool(
            self.mesh.collapsed_3d_elements 
            or self.mesh.collapsed_2d_elements 
            or self.mesh.collapsed_1d_elements
        )  # fmt: skip

        if disconnected_nodes or collapsed_elements:
            return False

        if self.mesh.surfaces_from_volume:
            if self.mesh.solids_connectivity.any():
                return True
            else:
                return False

        if self.mesh.lines_from_surface:
            if self.mesh.faces_connectivity.any():
                return True
            else:
                return False

        return False

    def is_there_a_geometry_imported(self):
        suffix = Path(self.geometry_path).suffix.strip(".").lower()
        return suffix in SUPPORTED_GEOMETRY_EXTENSIONS

    def is_there_a_compressor_excitation_in_model(self):
        compressor_properties = [
            "compressor_excitation_spectrum",
            "compressor_excitation_waveform",
            "reciprocating_compressor_excitation",
        ]

        for prop_label in compressor_properties:
            if self.properties.is_the_surface_property_present_in_the_model(prop_label):
                return True

        return False

    def is_there_a_valid_analysis_setup(self, current_analysis_id: int | None = None):

        if not isinstance(self.analysis_setup, HarmonicAnalysisSetup | ModalAnalysisSetup):
            return False

        if self.analysis_id == AnalysisID.NO_ANALYSIS:
            return False

        if isinstance(current_analysis_id, int):
            if self.analysis_id != current_analysis_id:
                return False

        def check_modal_setup():
            for key in ["modes_number", "sigma_factor"]:
                f_data = getattr(self.analysis_setup, key)
                if not isinstance(f_data, Number):
                    return False
            return True

        if AnalysisID(self.analysis_id).is_harmonic():
            frequencies = self.analysis_setup.frequencies
            solution_steps_mask = self.analysis_setup.solution_steps_mask
            analysis_method = self.analysis_setup.analysis_method

            if isinstance(frequencies, np.ndarray | list):
                if isinstance(solution_steps_mask, np.ndarray | list):
                    return True

            for key in ["f_min", "f_max", "f_step"]:
                f_data = getattr(self.analysis_setup, key)
                if not isinstance(f_data, Number):
                    return False

            if analysis_method == AnalysisMethod.MODE_SUPERPOSITION:
                return check_modal_setup()

            return True

        elif AnalysisID(self.analysis_id).is_modal():
            return check_modal_setup()

    def change_analysis_frequency_setup(self, frequencies: list | np.ndarray | None):
        if frequencies is None:
            return False

        if isinstance(frequencies, np.ndarray):
            frequencies = list(frequencies)

        condition_1 = self.list_frequencies == list()
        condition_2 = not self.properties.check_if_there_are_tables_at_the_model()

        if condition_1 or condition_2:
            self.list_frequencies = frequencies
            return False

        if self.list_frequencies != frequencies:
            return True

    def get_tabular_frequency_setup(self) -> None | tuple:
        """
        This method returns the frequency setup of the model's tabular data.
        """
        tables_frequencies = self.properties.process_all_tables_frequencies_vectors()
        if len(tables_frequencies) != 1:
            return None

        frequencies = tables_frequencies[0]
        f_min = frequencies[0]
        f_max = frequencies[-1]
        f_step = frequencies[1] - frequencies[0]

        return (f_min, f_max, f_step, frequencies)

    def get_structural_elements(self):
        element_type = self.element_topology

        if element_type == TETRAHEDRON_4:
            return STRUCT_TETRAHEDRON_4S(self), STRUCT_TRIANGLE_3(self), None

        elif element_type == TETRAHEDRON_10:
            return STRUCT_TETRAHEDRON_10S(self), None, None

        elif element_type == HEXAHEDRON_8:
            return STRUCT_HEXAHEDRON_8(self), None, None

        elif element_type == HEXAHEDRON_20:
            return STRUCT_HEXAHEDRON_20(self), None, None

        else:
            raise NotImplementedError(f'Element type "{element_type}" is not supported yet.')

    def get_acoustic_elements(self):
        element_type = self.element_topology

        if element_type == TETRAHEDRON_4:
            return ACT_TETRAHEDRON_4C(self), ACT_TRIANGLE_3(self), ACT_LINE_2(self)

        elif element_type == TETRAHEDRON_10:
            return ACT_TETRAHEDRON_10C(self), ACT_TRIANGLE_6(self), ACT_LINE_3(self)

        elif element_type == HEXAHEDRON_8:
            return ACT_HEXAHEDRON_8C(self), ACT_QUADRANGLE_4(self), ACT_LINE_2(self)

        elif element_type == HEXAHEDRON_20:
            return ACT_HEXAHEDRON_20C(self), ACT_QUADRANGLE_8(self), ACT_LINE_3(self)

        else:
            raise NotImplementedError(f'Element type "{element_type}" is not supported yet.')

    def set_structural_elements(self):
        element_3d, element_2d, element_1d = self.get_structural_elements()
        self.structural_element_1d = element_1d
        self.structural_element_2d = element_2d
        self.structural_element_3d = element_3d

    def set_acoustic_elements(self):
        element_3d, element_2d, element_1d = self.get_acoustic_elements()
        self.acoustic_element_1d = element_1d
        self.acoustic_element_2d = element_2d
        self.acoustic_element_3d = element_3d

    def get_acoustic_global_dof_from_nodes(self, node_ids: np.ndarray):
        """
        This method returns the global dof for the entered nodes.

        Parameter
        ---------
        node_ids: np.ndarray
            The vector with the node indexes.

        Return
        ------
        global_dof: np.array
            An array containing the global dof from input nodes.
        """
        _nodes = node_ids.reshape(-1, 1)
        _dof_per_node = self.acoustic_element_3d.DOF_PER_NODE

        global_dof = _dof_per_node * _nodes + np.arange(_dof_per_node)
        global_dof = np.array(global_dof.flatten(), dtype=int)

        return global_dof

    def get_structural_property_data_from_nodes(self, nodes: np.ndarray, data: dict, selection: str):
        output_data = dict()
        if data["element_type"] == "2d_element":
            element_2d = self.structural_element_2d
            if element_2d is None:
                return output_data

            dof_per_node = element_2d.DOF_PER_NODE

        else:
            element_3d = self.structural_element_3d
            if element_3d is None:
                return output_data

            dof_per_node = element_3d.DOF_PER_NODE

        local_dof = np.arange(dof_per_node, dtype=int)
        global_dof = dof_per_node * nodes.reshape(-1, 1) + local_dof

        den = 1
        if "nodal_attribution" in data.keys():
            nodal_attribution = data["nodal_attribution"]
            averaged = data["averaged"]
            if nodal_attribution and averaged:
                den = len(nodes)

            elif not nodal_attribution:
                # TODO: process element integration
                den = 1

                if selection == "surfaces":
                    pass
                elif selection == "lines":
                    pass
                else:
                    pass

        for node_gdof in global_dof:
            for j, gdof in enumerate(node_gdof):
                values = data["values"][j]
                if values is None:
                    continue

                output_data[gdof] = values / den

        return output_data

    def map_fluid_properties_to_volumes(self):
        """
        This method maps the fluid properties against each volume
        to calculate the global matrices factors.
        """

        frequency_dependent = False
        fluid_properties_from_volume = dict()

        if self.frequencies is None:
            number_frequencies = 1
        elif isinstance(self.frequencies, np.ndarray):
            number_frequencies = self.frequencies.size
        else:
            return dict(), False

        aux_ones = np.ones(number_frequencies, dtype=float)

        # prevent frequency-varying fluid properties
        # while solving acoustic modal analysis
        is_harmonic = self.analysis_id == AnalysisID.ACOUSTIC_HARMONIC
        if self.analysis_id == AnalysisID.NO_ANALYSIS:
            raise errors.InvalidModelSetupError("An AnalysisID should be provided.")

        for vol_id in self.mesh.elements_from_volume.keys():
            pm_data = self.properties._get_property("porous_material_model", volume=vol_id)
            vt_data = self.properties._get_property("viscous_thermal_model", volume=vol_id)
            fluid = self.properties._get_property("fluid", volume=vol_id)

            if isinstance(pm_data, dict) and is_harmonic:
                pm_data = self.porous_material_properties.get(vol_id)
                rho_f = pm_data["rho_eff"]
                C_f = pm_data["C_eff"]
                frequency_dependent = True

            elif isinstance(vt_data, dict) and is_harmonic:
                vt_data = self.viscous_thermal_model_properties.get(vol_id)
                rho_f = vt_data["rho_eff"]
                C_f = vt_data["C_eff"]
                frequency_dependent = True

            elif isinstance(fluid, Fluid):
                proportional_damping = self.properties._get_property("proportional_damping", volume=vol_id)
                rho = self.properties.get_fluid_density(fluid, proportional_damping)
                C = self.properties.get_speed_of_sound(fluid, proportional_damping)
                rho_f = rho * aux_ones
                C_f = C * aux_ones

            else:
                continue

            fluid_properties_from_volume[vol_id] = {
                "rho_f": rho_f,
                "C_f": C_f,
                "rho_0": fluid.fluid_density,
                "C_0": fluid.speed_of_sound,
                "mu_0": fluid.dynamic_viscosity,
            }

        return fluid_properties_from_volume, frequency_dependent

    def get_fluid_properties_from_surface(self, surface_id: int):
        """
        This method returns the fluid density and speed of sound properties
        from selected surface. If an internal surface is selected, neighboring
        volumes will be compared and valid properties will be returned if a single
        fluid was detected. The output data is in complex array form.

        Parameters
        ----------
        surface_id: int
            The selected surface id.

        Returns
        -------
        density: np.ndarray
            The fluid density array of complex values.

        speed_of_sound: np.ndarray
            The fluid speed of sound array of complex values.

        """
        fluid = None
        volumes_from_surface = self.mesh.volumes_from_surface[surface_id]

        if len(volumes_from_surface) == 1:
            for key in self.properties.volume_properties.keys():
                property, volume_id = key
                if volume_id == volumes_from_surface[0]:
                    if property == "viscous_thermal_model":
                        vt_model = ViscousThermalLossModels(self)
                        vt_model.process_effective_properties()
                        density = vt_model.effective_properties[volume_id]["rho_eff"]
                        speed_of_sound = vt_model.effective_properties[volume_id]["rho_eff"]
                        return density, speed_of_sound

                    elif property == "porous_material_model":
                        pm_model = PorousMaterialModels(self)
                        pm_model.process_effective_properties()
                        density = pm_model.effective_properties[volume_id]["rho_eff"]
                        speed_of_sound = pm_model.effective_properties[volume_id]["rho_eff"]
                        return density, speed_of_sound

            fluid = self.properties._get_property("fluid", surface=surface_id)

        elif len(volumes_from_surface) > 1:
            fluids = list()
            for volume_id in volumes_from_surface:
                fluid = self.properties._get_property("fluid", volume=volume_id)
                if not isinstance(fluid, Fluid):
                    continue
                if fluid not in fluids:
                    fluids.append(fluid)

            if len(fluids) == 1:
                fluid = fluids[0]

        if isinstance(fluid, Fluid):
            proportional_damping = self.properties._get_property("proportional_damping", volume=volumes_from_surface[0])
            density = self.properties.get_fluid_density(fluid, proportional_damping)
            speed_of_sound = self.properties.get_speed_of_sound(fluid, proportional_damping)
            return density, speed_of_sound

        return None, None

    def get_fluid_properties_from_volume(self, volume_id: int, frequencies: np.ndarray):
        """
        This method returns the fluid density and speed of sound properties
        from selected volume. The output data is in complex array form.
        """
        for key in self.properties.volume_properties.keys():
            property, vol_id = key
            if vol_id == volume_id:
                if property == "viscous_thermal_model":
                    vt_model = ViscousThermalLossModels(self)
                    vt_model.process_effective_properties()
                    density = vt_model.effective_properties[volume_id]["rho_eff"]
                    speed_of_sound = vt_model.effective_properties[volume_id]["rho_eff"]
                    return density, speed_of_sound

                elif property == "porous_material_model":
                    pm_model = PorousMaterialModels(self)
                    pm_model.process_effective_properties()
                    density = pm_model.effective_properties[volume_id]["rho_eff"]
                    speed_of_sound = pm_model.effective_properties[volume_id]["rho_eff"]
                    return density, speed_of_sound

        fluid = self.properties._get_property("fluid", volume=volume_id)
        proportional_damping = self.properties._get_property("proportional_damping", volume=vol_id)

        if isinstance(fluid, Fluid):
            density = self.properties.get_fluid_density(fluid, proportional_damping)
            speed_of_sound = self.properties.get_speed_of_sound(fluid, proportional_damping)
            return density, speed_of_sound

        return None, None

    def get_surface_density_and_speed_of_sound(self, surface_id: int) -> float | complex | np.ndarray:
        """
        It returs the density and speed of sound of selected surface.

        Parameter
        ---------
        surface_id: int
            The selected surface ID.

        Returns
        -------
        density: np.ndarray, float or None
            The density of selected surface.

        speed_of_sound: np.ndarray, float or None
            The speed of sound of selected surface.
        """

        density = None
        speed_of_sound = None

        rho_eff_pm, C_eff_pm = self.get_porous_material_model_effective_properties(surface_id)
        rho_eff_tv, C_eff_tv = self.get_viscous_thermal_model_effective_properties(surface_id)

        if isinstance(rho_eff_pm, np.ndarray):
            density = rho_eff_pm
            speed_of_sound = C_eff_pm

        elif isinstance(rho_eff_tv, np.ndarray):
            density = rho_eff_tv
            speed_of_sound = C_eff_tv

        else:
            fluid = self.properties._get_property("fluid", surface=surface_id)
            if not isinstance(fluid, Fluid):
                return None, None

            density = fluid.fluid_density
            speed_of_sound = fluid.speed_of_sound

        return (density, speed_of_sound)

    def get_surface_impedance(self, surface_id: int) -> float | complex | np.ndarray:
        """
        It returs the acoustic impedance of selected surface.

        Parameter
        ---------
        surface_id: int
            The selected surface ID.

        Returns
        -------
        impedance: np.ndarray, float or None
            The acoustic impedance of selected surface.
        """

        impedance = None

        at_data = self.properties._get_property("anechoic_termination", surface=surface_id)
        si_data = self.properties._get_property("specific_impedance", surface=surface_id)
        pw_data = self.properties._get_property("incident_plane_wave", surface=surface_id)

        if isinstance(at_data, dict) or isinstance(pw_data, dict):
            density, speed_of_sound = self.get_surface_density_and_speed_of_sound(surface_id)
            impedance = density * speed_of_sound

        elif isinstance(si_data, dict):
            if "real_values" in si_data.keys():
                real_values = np.array(si_data["real_values"])
                imag_values = np.array(si_data["imag_values"])
                impedance = real_values + 1j * imag_values

            elif "anechoic_termination" in si_data.keys():
                density, speed_of_sound = self.get_surface_density_and_speed_of_sound(surface_id)
                impedance = density * speed_of_sound

            elif "values" in si_data.keys():
                impedance = si_data["values"][0]

        return impedance

    def is_surface_impedance_frequency_dependent(self, surface_id: int) -> bool:
        """
        This method verifies whether the acoustic impedance of the selected surface is
        frequency-dependent, returning True if positive and False otherwise.
        """
        properties = ["porous_material_model", "viscous_thermal_model", "proportional_damping"]
        for volume_id in self.mesh.volumes_from_surface.get(surface_id):
            for _property in properties:
                prop_data = self.properties._get_property(_property, volume=volume_id)
                if isinstance(prop_data, dict):
                    return True
        return False

    def get_downstream_pressure_and_particle_velocity(self, surface_id: int):
        """
        This method computes the downstream pressure and particle velocity
        from the model acoustic excitation.

        Parameters
        ----------
        surface_id: int
            The input surface ID.

        Returns
        -------
        P_downstream: np.ndarray
            The downstream pressure vector or matrix.

        V_downstream: np.ndarray
            The downstream velocity vector or matrix.
        """

        frequencies = self.frequencies

        Zo_in = self.get_surface_impedance(surface_id)
        if Zo_in is None:
            return None, None

        pw_data = self.properties._get_property("incident_plane_wave", surface=surface_id)
        sv_data = self.properties._get_property("surface_velocity", surface=surface_id)

        if not (pw_data or sv_data):
            return None, None

        if isinstance(pw_data, dict):
            values = pw_data.get("values")[0]
            _incident_wave_vector = pw_data.get("incident_wave_vector")
            incident_wave_vector = np.array(_incident_wave_vector, dtype=float)

            if isinstance(values, complex | float):
                P_inc = values * np.ones_like(frequencies, dtype=complex)
            else:
                P_inc = values

            node_normals = self.mesh.get_stacked_normals_for_surface_elements(surface_id)
            avg_normal = np.average(node_normals, axis=0).flatten()

            P_downstream = P_inc * (avg_normal @ incident_wave_vector)
            V_downstream = -P_downstream / Zo_in

        if isinstance(sv_data, dict):
            if "real_values" in sv_data.keys():
                real_values = np.array(sv_data["real_values"])
                imag_values = np.array(sv_data["imag_values"])
                V_in = real_values + 1j * imag_values

            elif "values" in sv_data.keys():
                V_in = sv_data["values"][0]
                V_in = V_in[self.solution_steps_mask]

            P_downstream = V_in * Zo_in / 2
            V_downstream = P_downstream / Zo_in

        return P_downstream, V_downstream

    def process_porous_material_properties(self):
        """
        This method processes the porous material model effective properties.
        """
        pm_model = PorousMaterialModels(self)
        pm_model.process_effective_properties()
        self.porous_material_properties = deepcopy(pm_model.effective_properties)

    def get_porous_material_model_effective_properties(self, surface_id: int):
        """
        This method returns the porous material model-related
        effective properties of selected surface.

        Parameter
        ---------
        surface_id: int
            The surface tag.

        Returns
        -------
        rho_eff: np.ndarray or None
            The effective fluid density.

        C_eff: np.ndarray or None
            The effective speed of sound.
        """

        rho_eff = None
        C_eff = None

        for key in self.properties.volume_properties.keys():
            prop, volume_id = key
            if prop != "porous_material_model":
                continue

            if volume_id not in self.mesh.surfaces_from_volume.keys():
                continue

            if surface_id in self.mesh.surfaces_from_volume.get(volume_id):
                if not self.porous_material_properties:
                    self.process_porous_material_properties()

                pm_properties = self.porous_material_properties.get(volume_id)
                if not isinstance(pm_properties, dict):
                    continue

                rho_eff = pm_properties.get("rho_eff")
                C_eff = pm_properties.get("C_eff")
                break

        return rho_eff, C_eff

    def process_viscous_thermal_model_properties(self):
        """
        This method processes the viscous thermal model effective properties.
        """
        vt_model = ViscousThermalLossModels(self)
        vt_model.process_effective_properties()
        self.viscous_thermal_model_properties = deepcopy(vt_model.effective_properties)

    def get_viscous_thermal_model_effective_properties(self, surface_id: int):
        """
        This method returns the viscous thermal model-related
        effective properties of selected surface.

        Parameter
        ---------
        surface_id: int
            The surface tag.

        Returns
        -------
        rho_eff: np.ndarray or None
            The effective fluid density.

        C_eff: np.ndarray or None
            The effective speed of sound.
        """

        rho_eff = None
        C_eff = None

        for key in self.properties.volume_properties.keys():
            prop, volume_id = key
            if prop != "viscous_thermal_model":
                continue

            if volume_id not in self.mesh.surfaces_from_volume.keys():
                continue

            if surface_id in self.mesh.surfaces_from_volume.get(volume_id):
                if not self.viscous_thermal_model_properties:
                    self.process_viscous_thermal_model_properties()

                vt_properties = self.viscous_thermal_model_properties.get(volume_id)
                if not isinstance(vt_properties, dict):
                    continue

                rho_eff = vt_properties.get("rho_eff")
                C_eff = vt_properties.get("C_eff")
                break

        return rho_eff, C_eff

    def set_viscous_thermal_model_data(self, data, group=None, volume=None):
        self.properties._set_property("viscous_thermal_model", data, group=group, volume=volume)

    def process_perforated_plate_impedance(self, solution: np.ndarray | None = None):
        """
        This method processes the internal perforated plate acoustic impedance.

        Parameters
        ----------
        solution: np.ndarray, optional
            The nodal pressures solution matrix used to compute the non-linear
            perforated plate model.
        """
        pp_model = PerforatedPlateModels(self)
        pp_model.process_acoustic_transfer_impedances()

        self.perforated_plate_impedance_data.clear()
        self.perforated_plate_impedance_data = pp_model.perforated_plate_impedance_data

    def process_surface_thickness(self):
        for key, data in self.properties.surface_properties.items():
            property, surface_id = key
            if property == "surface_thickness":
                self.mesh.set_face_element_thickness(surface_id, data)

    def is_surface_thickness_properly_applied_in_model(self):
        volume_exists = self.mesh.are_there_volumes_in_geometry()
        if volume_exists:
            return None

        surface_ids = self.mesh.geometry_information.get("surfaces")
        surface_without_thickness = self.properties.get_entities_without_property("surface_thickness", surfaces=surface_ids)

        return surface_without_thickness

    def is_the_property_present_in_model(self, property_to_check: str, attribution_filter: str | None = None):
        """ """
        properties = {
            "volumes": self.properties.volume_properties,
            "surfaces": self.properties.surface_properties,
            "lines": self.properties.line_properties,
            "points": self.properties.point_properties,
            "nodes": self.properties.nodal_properties,
        }

        if attribution_filter is None:
            for _property in properties.values():
                for property_label, *args in _property.keys():
                    if property_label == property_to_check:
                        return True

        _property = properties.get(attribution_filter, dict())
        for property_label, *args in _property.keys():
            if property_label == property_to_check:
                return True

        return False

    def process_degrees_of_freedom_decoupling(self):
        if not self.properties.is_the_surface_property_present_in_the_model("degrees_of_freedom_decoupling"):
            return

        self.mesh.cache_mesh_information()
        self.dof_decoupling = DegreesOfFreedomDecoupling(self)
        self.dof_decoupling.process_degrees_of_freedom_decoupling()

    def toggle_processing_callback(self):
        self.stop_processing = not self.stop_processing
