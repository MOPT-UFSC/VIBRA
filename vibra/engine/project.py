from __future__ import annotations

import logging
from pathlib import Path
from time import perf_counter
from typing import Optional

import numpy as np
from PIL.Image import Image

from vibra import errors
from vibra.engine.analysis_info import AnalysisID, AnalysisSetup, AnalysisType, HarmonicAnalysisSetup, ModalAnalysisSetup, PhysicalDomain
from vibra.engine.assemblers import AcousticAssembler, StructuralAssembler
from vibra.engine.checkers.analysis_checker import AnalysisChecker
from vibra.engine.mesher.mesh import Mesh
from vibra.engine.mesher.mesh_setup import MeshSetup
from vibra.engine.model import Model
from vibra.engine.postprocessing import AcousticPostprocessing, StructuralPostprocessing
from vibra.engine.properties import FluidLibrary, MaterialLibrary
from vibra.engine.serialization.project_paths import ProjectPaths
from vibra.engine.serialization.project_reader import ProjectReader
from vibra.engine.serialization.project_writer import ProjectWriter
from vibra.engine.solution import HarmonicSolution, ModalSolution
from vibra.engine.solvers import HarmonicSolver, ModalSolver


class Project:
    def __init__(self, working_directory: Optional[Path | str] = None):
        self.project_paths = ProjectPaths(working_directory)
        self.reset_variables()

    def reset_variables(self):
        self.model = Model()
        self.project_reader = ProjectReader(self.project_paths)
        self.project_writer = ProjectWriter(self.project_paths)

        self.save_path: Optional[Path] = None
        self.needs_saving: bool = False

        # TODO: Store the Solution, not the solvers and assemblers.
        # Except if it is used to cache a few matrices somehow.
        self.assembler: Optional[AcousticAssembler | StructuralAssembler] = None
        self.solver: Optional[HarmonicSolver | ModalSolver] = None
        self.postprocessing: Optional[AcousticPostprocessing | StructuralPostprocessing] = None

    def reset_solution(self):
        self.assembler = None
        self.solver = None
        self.postprocessing = None
        self.project_writer.delete_results_data()
        self.model.reset_current_solution()
        self.needs_saving = True

    def reset_project(self):
        self.clear_working_directory()
        self.reset_variables()

    @property
    def mesh(self) -> Optional[Mesh]:
        return self.model.mesh

    @property
    def analysis_id(self):
        return self.model.analysis_id

    @property
    def analysis_setup(self):
        return self.model.analysis_setup

    @property
    def fluid_library(self) -> FluidLibrary:
        return self.model.properties.fluid_library

    @property
    def material_library(self) -> MaterialLibrary:
        return self.model.properties.material_library

    @property
    def can_resume_solution(self) -> bool:
        solution = self.model.solution

        if not isinstance(solution, HarmonicSolution):
            return False

        try:
            return not np.all(solution.status)
        except Exception:
            return False

    @property
    def working_directory(self) -> Path:
        return self.project_paths.working_directory

    @working_directory.setter
    def working_directory(self, path: Optional[Path | str]):
        if hasattr(self, "project_paths"):
            self.project_paths.set_working_directory(path)
        else:
            self.project_paths = ProjectPaths(path)

    def set_thumbnail(self, thumbnail: Image):
        """
        Set the thumbnail of the model and updates it in the working directory.
        """
        self.model.thumbnail = thumbnail
        self.project_writer.write_thumbnail(thumbnail)
        self.mark_project_as_modified()

    def clear_working_directory(self):
        """
        Empties the working directory folder.
        """
        self.project_paths.clear_data()
        self.mark_project_as_modified()

    def run_analysis(self, is_resume: bool = False, print_log: bool = False):
        """
        It performs the solution of the currently configured model.
        It might raise errors if the analysis is not propperly configured.
        """
        match self.model.analysis_id:
            case AnalysisID.STRUCTURAL_MODAL:
                return self.solve_structural_modal_analysis(is_resume=is_resume, print_log=print_log)
            case AnalysisID.STRUCTURAL_HARMONIC:
                return self.solve_structural_harmonic_analysis(is_resume=is_resume, print_log=print_log)
            case AnalysisID.ACOUSTIC_MODAL:
                return self.solve_acoustic_modal_analysis(is_resume=is_resume, print_log=print_log)
            case AnalysisID.ACOUSTIC_HARMONIC:
                return self.solve_acoustic_harmonic_analysis(is_resume=is_resume, print_log=print_log)
            case AnalysisID.NO_ANALYSIS:
                raise errors.IncompleteSetupError("No AnalysisID was provided.")
            case _:
                raise NotImplementedError(f'Analysis type "{self.model.analysis_id.name}" is not implemented.')

    def load_project(
        self,
        path: Path | str,
    ) -> Project:
        """
        Unpacks the vibra file into the working directory and reads data from it.
        """
        logging.info("Loading the project data... [25%]")
        path = Path(path)
        self.reset_solution()
        self.project_reader.unpack_into_working_directory(path)
        self.model = self.project_reader.read_model(self.model)
        self.assembler, self.solver = self.project_reader.read_assembler_and_solver(self.model)
        self.model.name = path.stem
        self.save_path = path
        self.needs_saving = False
        return self

    def read_from_working_dir(self) -> Project:
        """
        Reload project data from the working directory.
        """
        logging.info("Loading the project data... [15%]")
        self.model = self.project_reader.read_model(self.model)
        return self

    def reload_solution_from_working_dir(self):
        """
        Reload solution data written by another process.
        """
        self.model.solution = self.project_reader.read_solution(self.model)
        self.assembler, self.solver = self.project_reader.read_assembler_and_solver(self.model)
        self.update_post_processing()

    def write_to_working_dir(self):
        """
        Writes project data to the working directory.
        """
        self.project_writer.write_model(self.model)
        self.mark_project_as_modified()

    # TODO: use only "write_to_working_dir"
    def update_model_properties_file(self):
        self.mark_solution_as_outdated()
        self.project_writer.write_model_properties(self.model.properties)
        self.mark_project_as_modified()

    def update_project_setup_file(self):
        self.project_writer.write_project_setup(self.model)
        self.mark_project_as_modified()

    def save_project(
        self,
        path: Path | str,
        name: str = "Project",
    ):
        """
        Packs the data from the working directory into a `.vibra` file.
        """
        self.save_path = Path(path)
        self.model.name = name
        self.write_to_working_dir()
        self.project_writer.write_file(path)
        self.needs_saving = False

    def import_mesh(self, path: Path | str) -> Mesh:
        """
        Loads a complete mesh from a file.

        The supported mesh formats are:
            - *.bdf
            - *.nas
            - *.msh
        """
        mesh = Mesh().load_mesh(path)
        self.model.mesh = mesh
        self.model.geometry_path = path  # keeping previous file organization
        self.write_to_working_dir()
        return mesh

    def import_geometry(self, path: Path | str):
        """
        Loads a geometry from a file.
        This geometry can be used to create a mesh later.

        The supported geometry formats are:
            - *.step
            - *.iges
        """
        path = Path(path)
        # self.model.geometry = Geometry(path)
        self.model.geometry_path = path
        self.write_to_working_dir()

    def configure_mesh(self, mesh_setup: MeshSetup):
        """
        Configures how to create a mesh from a geometry.
        This method might be called before or after loading a geometry.
        """
        self.model.set_mesh_setup(mesh_setup)
        self.update_project_setup_file()

    def generate_mesh(self, mesh_setup: MeshSetup) -> Mesh:
        """
        Generates a mesh from the loaded geometry and the
        parameters set using the configure_mesh method.

        It might raise an error if the geometry is not loaded
        or if the mesh configuration is not set.
        """
        if self.model.geometry_path is None:
            raise errors.InvalidMeshSetupError("The geometry has not been loaded yet.")

        if not isinstance(mesh_setup, MeshSetup):
            raise errors.InvalidMeshSetupError("The mesh setup has not been configured yet.")

        mesh = Mesh().load_cad(self.model.geometry_path, mesh_setup)

        if mesh.collapsed_elements_data:
            collapsed_1d_elements = mesh.collapsed_elements_data.get("collpased_1d_elements")
            collapsed_2d_elements = mesh.collapsed_elements_data.get("collpased_2d_elements")
            collapsed_3d_elements = mesh.collapsed_elements_data.get("collpased_3d_elements")

            message = "The generated mesh contains collapsed elements."
            message += "Please check the mesh setup and try again.\n"
            message += "Collapsed 1d elements: " + ", ".join(collapsed_1d_elements) + "\n"
            message += "Collapsed 2d elements: " + ", ".join(collapsed_2d_elements) + "\n"
            message += "Collapsed 3d elements: " + ", ".join(collapsed_3d_elements)

            raise errors.MeshException(
                message,
                edges=collapsed_1d_elements,
                faces=collapsed_2d_elements,
                solids=collapsed_3d_elements,
            )

        self.model.mesh = mesh
        self.configure_mesh(mesh_setup)
        self.model.process_degrees_of_freedom_decoupling()

        self.reset_solution()
        self.project_writer.write_mesh(mesh)
        self.mark_project_as_modified()

        return mesh

    def generate_visual_mesh(self) -> Mesh:
        """
        Utility method to create a fast mesh intended to be used only for visualization purposes.
        """
        if self.model.geometry_path is None:
            raise errors.InvalidMeshSetupError("The geometry has not been loaded yet.")

        self.model.process_visual_geometry_mesh(self.model.geometry_path)
        self.project_writer.write_mesh(self.model.mesh)
        return self.model.mesh

    def generate_mesh_from_geometry(
        self,
        geometry_path: Path | str,
        mesh_setup: MeshSetup,
    ) -> Mesh:
        """
        Loads a geometry and uses it to generate a mesh.
        """
        self.import_geometry(geometry_path)
        self.configure_mesh(mesh_setup)
        return self.generate_mesh()

    def configure_analysis(
        self,
        analysis_setup: Optional[AnalysisSetup],
    ):
        """
        Defines the `AnalysisID` and the `AnalysisSetup` required to
        execute a analysis.
        """
        self.reset_solution()
        self.model.set_analysis_setup(analysis_setup)
        self.update_project_setup_file()

    def solve_structural_modal_analysis(self, is_resume: bool = False, print_log: bool = False) -> ModalSolution:

        self.update_project_setup_file()

        checker = AnalysisChecker(self.model)
        checker.check_analysis_requirements()

        self.assembler = StructuralAssembler(self.model)
        self.solver = ModalSolver(self.assembler)
        self.postprocessing = StructuralPostprocessing(self.model)

        self.assembler.assemble_global_matrices(print_log=print_log)

        t0 = perf_counter()
        self.model.solution = self.solver.solve(print_log=print_log)
        self.project_writer.write_modal_solution(self.model.solution)
        self.mark_project_as_modified()
        dt = perf_counter() - t0

        print(f"Elapsed time to solve structural modal analysis: {dt: .6f} [s]")
        logging.info(f"Elapsed time to solve structural modal analysis: {dt: .6f} [s]")

        return self.model.solution

    def solve_structural_harmonic_analysis(self, is_resume: bool = False, print_log: bool = False) -> HarmonicSolution:

        self.update_project_setup_file()

        checker = AnalysisChecker(self.model)
        checker.check_analysis_requirements()

        self.assembler = StructuralAssembler(self.model)
        self.solver = HarmonicSolver(self.assembler, self.project_paths)
        self.postprocessing = StructuralPostprocessing(self.model)

        self.assembler.assemble_global_matrices_and_excitations(print_log=print_log)

        t0 = perf_counter()

        analysis_method = self.model.analysis_setup.analysis_method
        if analysis_method == "direct":
            self.model.solution = self.solver.solve_direct(print_log=print_log, is_resume=is_resume)
        elif analysis_method == "mode_superposition":
            self.model.solution = self.solver.solve_mode_superposition(
                is_proportionally_damped=True,
                is_resume=is_resume,
                print_log=print_log,
            )
        else:
            raise ValueError(f"Unsupported analysis method: {analysis_method}")

        self.project_writer.write_harmonic_solution(self.model.solution)
        self.mark_project_as_modified()
        dt = perf_counter() - t0

        print(f"Elapsed time to solve structural harmonic analysis: {dt: .6f} [s]")
        logging.info(f"Elapsed time to solve structural harmonic analysis: {dt: .6f} [s]")

        return self.model.solution

    def solve_acoustic_modal_analysis(self, is_resume: bool = False, print_log: bool = False) -> ModalSolution:

        self.update_project_setup_file()

        checker = AnalysisChecker(self.model)
        checker.check_analysis_requirements()

        self.assembler = AcousticAssembler(self.model)
        self.solver = ModalSolver(self.assembler)
        self.postprocessing = AcousticPostprocessing(self.model)

        self.assembler.assemble_global_matrices(print_log=print_log)

        t0 = perf_counter()
        self.model.solution = self.solver.solve(print_log=print_log)
        self.project_writer.write_modal_solution(self.model.solution)
        self.mark_project_as_modified()
        dt = perf_counter() - t0

        print(f"Elapsed time to solve acoustic modal analysis: {dt: .6f} [s]")
        logging.info(f"Elapsed time to solve acoustic modal analysis: {dt: .6f} [s]")

        return self.model.solution

    def solve_acoustic_harmonic_analysis(self, is_resume: bool = False, print_log: bool = False) -> HarmonicSolution:

        self.update_project_setup_file()

        checker = AnalysisChecker(self.model)
        checker.check_analysis_requirements()

        self.assembler = AcousticAssembler(self.model)
        self.solver = HarmonicSolver(self.assembler, self.project_paths)
        self.postprocessing = AcousticPostprocessing(self.model)

        self.model.reset_dissipation_model_properties()
        self.model.process_porous_material_properties()
        self.model.process_viscous_thermal_model_properties()
        self.model.process_perforated_plate_impedance()
        self.assembler.assemble_global_matrices_and_excitations(print_log=print_log)

        t0 = perf_counter()

        analysis_method = self.model.analysis_setup.analysis_method
        if analysis_method == "direct":
            self.model.solution = self.solver.solve_direct(print_log=print_log, is_resume=is_resume)
        elif analysis_method == "mode_superposition":
            self.model.solution = self.solver.solve_mode_superposition(print_log=print_log, is_resume=is_resume)
        else:
            raise ValueError(f"Unsupported analysis method: {analysis_method}")

        if self.solver.project_paths is None:
            self.project_writer.write_harmonic_solution(self.model.solution)

        self.mark_project_as_modified()
        dt = perf_counter() - t0

        print(f"Elapsed time to solve acoustic harmonic analysis: {dt: .6f} [s]")
        logging.info(f"Elapsed time to solve acoustic harmonic analysis: {dt: .6f} [s]")

        return self.model.solution

    def update_post_processing(self):
        self.postprocessing = None
        if AnalysisID(self.model.analysis_id).is_acoustic():
            self.postprocessing = AcousticPostprocessing(self.model)
        elif AnalysisID(self.model.analysis_id).is_structural():
            self.postprocessing = StructuralPostprocessing(self.model)

    def get_acoustic_postprocessing(self) -> AcousticPostprocessing:
        if not isinstance(self.postprocessing, AcousticPostprocessing):
            self.update_post_processing()
        return self.postprocessing

    def get_structural_postprocessing(self) -> StructuralPostprocessing:
        if not isinstance(self.postprocessing, StructuralPostprocessing):
            self.update_post_processing()
        return self.postprocessing

    def is_mesh_configured(self) -> bool:
        """
        Checks if the mesh is configured.
        """
        return isinstance(self.model.mesh_setup, MeshSetup)

    def is_analysis_id_valid(self, analysis_id: AnalysisID) -> bool:
        """
        Checks if the provided AnalysisID corresponds to the current model AnalysisSetup.
        """

        if analysis_id.is_harmonic() and isinstance(self.model.analysis_setup, HarmonicAnalysisSetup):
            return True

        if analysis_id.is_modal() and isinstance(self.model.analysis_setup, ModalAnalysisSetup):
            return True

        return False

    def is_analysis_setup_complete(self) -> bool:
        """
        Checks if the current model setup is ready to be executed.
        """

        try:
            AnalysisChecker(self.model).check_analysis_requirements()
        except Exception:
            return False
        else:
            return True

    def is_there_a_valid_solution(self) -> bool:
        """
        Check if is there a valid analysis solution.
        """

        if self.model.analysis_id.is_acoustic() and not isinstance(self.assembler, AcousticAssembler):
            return False

        if self.model.analysis_id.is_structural() and not isinstance(self.assembler, StructuralAssembler):
            return False

        if self.model.analysis_id.is_harmonic() and not isinstance(self.solver, HarmonicSolver):
            return False

        if self.model.analysis_id.is_modal() and not isinstance(self.solver, ModalSolver):
            return False

        if self.solver is None:
            return False

        return isinstance(self.model.solution, ModalSolution | HarmonicSolution)

    def get_analysis_type(self) -> AnalysisType:
        """
        Gets the current analysis typs as a string according
        to the `AnalysisID` provided in the model.
        """

        if self.model.analysis_id.is_harmonic():
            return AnalysisType.HARMONIC
        elif self.model.analysis_id.is_modal():
            return AnalysisType.MODAL
        elif self.model.analysis_id.is_static():
            return AnalysisType.STATIC
        else:
            return AnalysisType.NO_ANALYSIS_TYPE

    def get_physical_domain(self) -> PhysicalDomain:
        """
        Gets the current physical domain as a string according
        to the `AnalysisID` provided in the model.
        """

        if self.model.analysis_id.is_acoustic():
            return PhysicalDomain.ACOUSTIC
        elif self.model.analysis_id.is_structural():
            return PhysicalDomain.STRUCTURAL
        elif self.model.analysis_id.is_coupled():
            return PhysicalDomain.COUPLED
        else:
            return PhysicalDomain.NO_PHYSICAL_DOMAIN

    def mark_project_as_modified(self):
        """
        Indicates that something was modified and that the project need to be saved.
        """
        self.needs_saving = True

    def mark_solution_as_outdated(self, reset: bool = False):
        solution_exists = isinstance(self.model.solution, HarmonicSolution | ModalSolution)
        solution_outdated = not reset and solution_exists

        analysis_setup = self.model.analysis_setup
        if isinstance(analysis_setup, HarmonicAnalysisSetup | ModalAnalysisSetup):
            analysis_setup.outdated_solution = solution_outdated
            self.model.set_analysis_setup(analysis_setup)
            self.update_project_setup_file()
