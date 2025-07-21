from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vibra.project_files.project import Project

from vibra import app
from vibra.errors import InvalidModelSetupError, InvalidGeometryForAcousticAnalysisError, InvalidModelExcitationError
from vibra.interface.general.print_message_input import PrintMessageInput
from vibra.engine.properties.material import Material

import numpy as np

window_title_1 = "Error"
window_title_2 = "Warning"


class AnalysisRequirementsChecker:
    '''
    This class should be a simple validator.
    It should not be used to update the interface.

    I will handle this by raising errors and warnings if the model is not valid,
    and catch these errors latter in the interface.
    
    But for now I am workarrounding it by just ignoring the checker outside of
    the interface because I have other stuff to worry about.
    '''

    def __init__(self, project: "Project"):

        self.project = project
        self.model = self.project.model
        self.properties = self.project.model.properties

        self.surface_ids = self.model.mesh.geometry_information["surfaces"]
        self.volume_ids = self.model.mesh.geometry_information["volumes"]

    def check_materials(self, surface_thickness=True):

        volumes_without_material = list()
        for volume_id in self.volume_ids:
            prop_data = self.properties._get_property("material", volume=volume_id)
            if prop_data is None:
                volumes_without_material.append(volume_id)

        surfaces_without_material = list()
        for surface_id in self.surface_ids:
            prop_data = self.properties._get_property("material", surface=surface_id)
            if prop_data is None:
                surfaces_without_material.append(surface_id)

        surfaces_without_material, _, shell_without_thickness = self.check_material_and_surface_thickness()
        if volumes_without_material:
            if len(volumes_without_material) != len(self.volume_ids):
                raise InvalidModelSetupError(
                    f"You should assign one material for volumes {volumes_without_material}",
                    "to proceed with the analysis solution.",
                )

        if len(volumes_without_material) == len(self.volume_ids):
            if len(surfaces_without_material) == len(self.surface_ids):
                if len(self.volume_ids):
                    raise InvalidModelSetupError(
                        "You should assign a material for all volumes or some surfaces",
                        "to proceed with the analysis solution.",
                    )
                else:
                    raise InvalidModelSetupError(
                        "You should assign a material to some surfaces",
                        "to proceed with the analysis solution.",
                    )

            if shell_without_thickness:
                if len(shell_without_thickness) == len(self.surface_ids):
                    raise InvalidModelSetupError(
                        "You should assign at least one material and thickness for one surface",
                        "to proceed with the analysis solution.",
                    )
                else:
                    raise InvalidModelSetupError(
                        "You should assign a thickness for the already assigned surface materials",
                        "to proceed with the analysis solution.",
                        surfaces=shell_without_thickness
                    )

    def check_fluids(self):

        volumes_without_fluid = list()
        for volume_id in self.volume_ids:
            prop_data = self.properties._get_property("fluid", volume=volume_id)
            if prop_data is None:
                volumes_without_fluid.append(volume_id)

        surfaces_without_fluid = list()
        for surface_id in self.surface_ids:
            prop_data = self.properties._get_property("fluid", surface=surface_id)
            if prop_data is None:
                surfaces_without_fluid.append(surface_id)

        if self.volume_ids:
            if volumes_without_fluid:
                raise InvalidModelSetupError(
                    f"You should assign one fluid for volume(s) {volumes_without_fluid}",
                    "to proceed with the analysis solution.",
                    volumes=volumes_without_fluid,
                )

            elif surfaces_without_fluid:
                raise InvalidModelSetupError(
                    f"You should assign one fluid for surface(s) {surfaces_without_fluid}",
                    "to proceed with the analysis solution.",
                    surfaces=surfaces_without_fluid,
                )

        else:
            raise InvalidGeometryForAcousticAnalysisError(
                "The selected geometry file has no volumes,",
                "therefore it is invalid for acoustic analysis.",
            )

    def check_material_and_surface_thickness(self):

        shell_without_material = list()
        surface_without_material = list()
        shell_without_thickness = list()
        for surface_id in self.surface_ids:
            mat_data = self.properties._get_property("material", surface=surface_id)
            st_data = self.properties._get_property("surface_thickness", surface=surface_id)
            if mat_data is None:
                surface_without_material.append(surface_id)
                if isinstance(st_data, dict):
                    shell_without_material.append(surface_id)
            elif isinstance(mat_data, Material) and st_data is None:
                shell_without_thickness.append(surface_id)

        return surface_without_material, shell_without_material, shell_without_thickness

    def check_acoustic_harmonic_excitations(self):

        prop_labels = [
            "acoustic_pressure",
            "surface_velocity",
            "mass_flow_rate",
            "incident_plane_wave",
            "compressor_excitation",
            "mass_source",
        ]

        properties = [
            self.properties.volume_properties,
            self.properties.surface_properties,
            self.properties.line_properties,
            self.properties.point_properties,
            self.properties.nodal_properties,
        ]

        for property in properties:
            for (prop_label, *_), data in property.items():
                if prop_label in prop_labels:
                    if np.sum(data["values"]):
                        return False

        raise InvalidModelExcitationError(
            "Enter a valid acoustic model excitation to proceed",
            "with the acoustic harmonic analysis solution.",
        )

    def check_structural_harmonic_excitations(self):

        prop_labels = [
            "prescribed_dofs",
            "nodal_loads",
            "distributed_loads",
            "normal_pressure_load",
        ]

        properties = [
            self.properties.surface_properties,
            self.properties.line_properties,
            self.properties.point_properties,
            self.properties.nodal_properties,
        ]

        for property in properties:
            for (prop_label, *_), data in property.items():
                if prop_label in prop_labels:
                    values = [0 if value is None else value for value in data["values"]]
                    if np.sum(values):
                        return False

        raise InvalidModelExcitationError(
            "Enter a valid structural model excitation to proceed",
            "with the structural harmonic analysis solution.",
        )

    def check_acoustic_harmonic_analysis(self):
        self.check_fluids()
        self.check_acoustic_harmonic_excitations()

    def check_structural_harmonic_analysis(self):
        self.check_materials()
        self.check_structural_harmonic_excitations()

    def check_acoustic_modal_analysis(self):
        self.check_fluids()

    def check_structural_modal_analysis(self):
        self.check_materials()
