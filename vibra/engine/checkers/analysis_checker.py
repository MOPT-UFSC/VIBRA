from numbers import Number

import numpy as np

from vibra import errors
from vibra.engine.analysis_info import (
    AnalysisID,
    AnalysisMethod,
    HarmonicAnalysisSetup,
    ModalAnalysisSetup,
)
from vibra.engine.model import Model


class AnalysisChecker:
    def __init__(self, model: Model):
        self.model = model

    def check_analysis_requirements(self, is_resume: bool = False):
        match self.model.analysis_id:
            case AnalysisID.STRUCTURAL_MODAL:
                self.check_structural_modal_analysis()
            case AnalysisID.STRUCTURAL_HARMONIC:
                self.check_structural_harmonic_analysis()
            case AnalysisID.ACOUSTIC_MODAL:
                self.check_acoustic_modal_analysis()
            case AnalysisID.ACOUSTIC_HARMONIC:
                self.check_acoustic_harmonic_analysis()
            case _:
                raise NotImplementedError(f'Analysis type "{self.model.analysis_id.name}" is not implemented.')

    def check_analysis_setup(self, analysis_id_to_check: AnalysisID):

        analysis_id = self.model.analysis_id
        if AnalysisID(analysis_id).is_harmonic():
            if not isinstance(self.model.analysis_setup, HarmonicAnalysisSetup):
                raise errors.InvalidModelSetupError("A HarmonicAnalysisSetup is needed to proceed with the analysis solution.")

        if AnalysisID(analysis_id).is_modal():
            if not isinstance(self.model.analysis_setup, ModalAnalysisSetup):
                raise errors.InvalidModelSetupError("A ModalAnalysisSetup is needed to proceed with the analysis solution.")

        if analysis_id_to_check != analysis_id:
            raise errors.InvalidAnalysisSetupError(
                f"The solver expects an '{analysis_id_to_check.name}' analysis type \
                 but received the '{analysis_id.name}' analysis type instead."
            )

        if not self.model.is_there_a_valid_analysis_setup():
            raise errors.InvalidAnalysisSetupError("An invalid analysis setup has been configured.")

    def check_acoustic_harmonic_analysis(self, is_resume: bool = False):
        self.check_can_resume(is_resume)
        self.check_mesh()
        self.check_contains_volumes()
        self.check_fluids_volumes()
        self.check_acoustic_harmonic_excitations()

    def check_structural_harmonic_analysis(self, is_resume: bool = False):
        self.check_can_resume(is_resume)
        self.check_mesh()

        if self.model.mesh.are_there_volumes_in_geometry():
            self.check_materials_volumes()
        else:
            self.check_materials_surfaces()

        self.check_structural_harmonic_excitations()

        if self.model.analysis_setup.analysis_method == AnalysisMethod.MODE_SUPERPOSITION:
            self.check_mode_superposition_prescribed_dof_criterion()

    def check_acoustic_modal_analysis(self, is_resume: bool = False):
        self.check_can_resume(is_resume)
        self.check_mesh()
        self.check_contains_volumes()
        self.check_fluids_volumes()
        self.check_frequency_varying_fluid_properties_for_modal_analysis()

    def check_structural_modal_analysis(self, is_resume: bool = False):
        self.check_can_resume(is_resume)
        self.check_mesh()

        if self.model.mesh.are_there_volumes_in_geometry():
            self.check_materials_volumes()
        else:
            self.check_materials_surfaces()

    # common checkers:
    def check_can_resume(self, is_resume: bool):
        if is_resume and not self.model.can_resume_solution:
            raise errors.InvalidAnalysisSetupError("Analysis can not be resumed.")

    def check_mesh(self):
        mesh = self.model.mesh
        if mesh is None:
            raise errors.InvalidMeshSetupError("There is no mesh available")

        if not self.model.is_there_a_valid_mesh():
            raise errors.InvalidMeshSetupError("No mesh was provided")

        if mesh.disconnected_nodes_data:
            text = "Disconnected nodes have been detected during the mesh post-processing. \n"
            text += "The model solution will stay deactivated until the meshing-related issues \n"
            text += "have been addressed."
            raise errors.InvalidMeshSetupError(text)

        if mesh.collapsed_elements_data:
            text += "Collapsed elements have been detected during the mesh post-processing. \n"
            text += "The model solution will stay deactivated until the collapsed-related \n"
            text += "issues have been addressed."
            raise errors.InvalidMeshSetupError(text)

    def check_materials_volumes(self):
        volumes_without_material = self._entities_without_property(
            "material",
            "volumes",
        )

        if volumes_without_material:
            raise errors.InvalidModelSetupError(
                f"You should assign one material for volumes {volumes_without_material} "
                "to proceed with the analysis solution.",
                volumes=volumes_without_material,
            )  # fmt: skip

    def check_materials_surfaces(self):
        surfaces_without_material = self._entities_without_property(
            "material",
            "surfaces",
        )

        if surfaces_without_material:
            raise errors.InvalidModelSetupError(
                f"You should assign one material for surfaces {surfaces_without_material} "
                "to proceed with the analysis solution.",
                surfaces=surfaces_without_material,
            )  # fmt: skip

    def check_fluids_volumes(self):
        volumes_without_fluid = self._entities_without_property(
            "fluid",
            "volumes",
        )

        if volumes_without_fluid:
            raise errors.InvalidModelSetupError(
                f"You should assign one fluid for volumes {volumes_without_fluid} "
                "to proceed with the analysis solution.",
                volumes=volumes_without_fluid,
            )  # fmt: skip

    def check_fluids_surfaces(self):
        surfaces_without_fluid = self._entities_without_property(
            "fluid",
            "surfaces",
        )

        if surfaces_without_fluid:
            raise errors.InvalidModelSetupError(
                f"You should assign one fluid for surfaces {surfaces_without_fluid} "
                "to proceed with the analysis solution.",
                surfaces=surfaces_without_fluid,
            )  # fmt: skip

    def check_surface_thickness(self):
        surfaces_without_thickness = self._entities_without_property(
            "surface_thickness",
            "surfaces",
        )

        if surfaces_without_thickness:
            raise errors.InvalidModelSetupError(
                f"You should assign the surface thickness for surfaces {surfaces_without_thickness} "
                "to proceed with the analysis solution.",
                surfaces=surfaces_without_thickness,
            )  # fmt: skip

    def check_contains_volumes(self):
        return
        mesh = self.model.mesh

        if not mesh.are_there_volumes_in_geometry():
            raise errors.InvalidGeometryError(
                "The selected geometry does not contain volumes, "
                "therefore, it is invalid for the current analysis."
            )  # fmt: skip

    def check_frequency_varying_fluid_properties_for_modal_analysis(self):
        properties = self.model.properties
        pm_exists = properties.is_the_volume_property_present_in_the_model("porous_material_model")
        vt_exists = properties.is_the_volume_property_present_in_the_model("viscous_thermal_model")

        if pm_exists or vt_exists:
            raise errors.InvalidModelSetupError(
                "A frequency-varying fluid property was detected in the acoustic model. The modal "
                "analysis can only be solved for fluid properties that are constant or proportional "
                "to frequency. Consider reconfiguring the acoustic model to proceed with the "
                "acoustic modal analysis solution."
            )  # fmt: skip

    def check_acoustic_harmonic_excitations(self):
        if self._any_true_property_attributed(
            "acoustic_pressure",
            "surface_velocity",
            "mass_flow_rate",
            "incident_plane_wave",
            "mass_source",
            "compressor_excitation_spectrum",
            "compressor_excitation_waveform",
            "reciprocating_compressor_excitation",
        ):
            return

        raise errors.InvalidModelExcitationError(
            "Enter a valid acoustic model excitation to proceed "
            "with the acoustic harmonic analysis solution."
        )  # fmt: skip

    def check_structural_harmonic_excitations(self):
        if self._any_true_property_attributed(
            "prescribed_dof",
            "nodal_loads",
            "distributed_loads",
            "normal_pressure_load",
        ):
            return

        raise errors.InvalidModelExcitationError(
            "Enter a valid structural model excitation to proceed "
            "with the structural harmonic analysis solution."
        )  # fmt: skip

    def check_mode_superposition_prescribed_dof_criterion(self):
        if self._any_true_property_attributed("prescribed_dof"):
            return

        raise errors.InvalidModelExcitationError(
            "Harmonic analysis using the modal superposition method cannot be solved if "
            "there are any nonzero prescribed degrees of freedom."
        )  # fmt: skip

    def _any_property_attributed(self, *property_names: str):
        for _, prop_label, _, data in self.model.properties.iterate_properties():
            if prop_label in property_names:
                return True
        return False

    def _any_true_property_attributed(self, *property_names: str):
        for _, prop_label, _, data in self.model.properties.iterate_properties():
            if prop_label not in property_names:
                continue

            if not isinstance(data, dict):
                continue

            values = list()
            for value in data.get("values", list()):
                if isinstance(value, Number):
                    values.append(value != 0)
                elif isinstance(value, np.ndarray):
                    values.append(np.any(value))

            if np.sum(values):
                return True

        return False

    def _entities_without_property(self, property_name: str, entity_name: str):
        properties = self.model.properties
        geometry_information = self.model.mesh.geometry_information
        entities = geometry_information.get(entity_name, list())

        kwargs = {
            entity_name: entities,
        }

        return properties.get_entities_without_property(
            property_name,
            **kwargs,
        )
