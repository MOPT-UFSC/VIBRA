from __future__ import annotations

import logging
from pathlib import Path
from tempfile import TemporaryDirectory
from time import perf_counter
from typing import Optional

from PIL.Image import Image

from vibra import errors
from vibra.engine import AnalysisID, HarmonicAnalysisSetup, ModalAnalysisSetup
from vibra.engine.assemblers import AcousticAssembler, StructuralAssembler
from vibra.engine.checkers.analysis_checker import AnalysisChecker
from vibra.engine.mesher.mesh import Mesh
from vibra.engine.mesher.mesh_setup import MeshSetup
from vibra.engine.model import Model
from vibra.engine.postprocessing import AcousticPostprocessing, StructuralPostprocessing
from vibra.engine.serialization.project_reader import ProjectReader
from vibra.engine.serialization.project_writer import ProjectWriter
from vibra.engine.solvers import HarmonicSolver, ModalSolver


class NewProject:
    def __init__(self, working_directory: Optional[Path | str] = None):
        self.reset_variables()
        self.create_connections()

        self._tmp_dir = TemporaryDirectory(prefix="vibra_project_")
        self.working_directory = working_directory

    def reset_variables(self):
        self.name: str = "Project"
        self.thumbnail: Optional[Image] = None
        self.save_path: Optional[Path] = None
        self.needs_saving: bool = False

        self.model = Model()
        self.current_analysis_id: AnalysisID = AnalysisID.NO_ANALYSIS

        self.mesh_setup: Optional[MeshSetup] = None
        self.assembler: Optional[AcousticAssembler | StructuralAssembler] = None
        self.solver: Optional[HarmonicSolver | ModalSolver] = None
        self.postprocessing: Optional[AcousticPostprocessing | StructuralPostprocessing] = None

    def reset_solution(self):
        self.assembler = None
        self.solver = None
        self.postprocessing = None
        self.project_writer.delete_results_data()

    def create_connections(self):
        return
        self.model.properties.modified.connect(self.update_model_properties_file)
        self.model.analysis_setup_modified.connect(self.update_project_setup_file)

    @property
    def mesh(self) -> Optional[Mesh]:
        return self.model.mesh

    @mesh.setter
    def mesh(self, mesh: Optional[Mesh]):
        self.model.mesh = mesh

    @property
    def working_directory(self) -> Path:
        return self._working_directory

    @working_directory.setter
    def working_directory(self, path: Optional[Path | str]):
        if path is None:
            self._working_directory = Path(self._tmp_dir.name)
        else:
            self._working_directory = Path(path)

        self.project_reader = ProjectReader(self._working_directory)
        self.project_writer = ProjectWriter(self._working_directory)

    def set_thumbnail(self, thumbnail: Image):
        self.thumbnail = thumbnail
        self.project_writer.write_thumbnail(thumbnail)

    def clear_working_directory(self):
        self.project_writer.project_paths.clear_data()

    def run_analysis(self):
        match self.current_analysis_id:
            case AnalysisID.STRUCTURAL_MODAL:
                return self.solve_structural_modal_analysis()
            case AnalysisID.STRUCTURAL_HARMONIC:
                return self.solve_structural_harmonic_analysis()
            case AnalysisID.ACOUSTIC_MODAL:
                return self.solve_acoustic_modal_analysis()
            case AnalysisID.ACOUSTIC_HARMONIC:
                return self.solve_acoustic_harmonic_analysis()
            case _:
                raise NotImplementedError(f'Analysis type "{self.current_analysis_id.name}" is not implemented.')

    def load_project(
        self,
        path: Path | str,
    ) -> NewProject:
        """
        Unpacks the vibra file into the working directory and reads data from it.
        """
        self.project_reader.read_file(path)
        self.project_reader.read_project(self)
        self.save_path = Path(path)
        self.create_connections()
        return self

    def sync_with_working_dir(self) -> NewProject:
        """
        Reload project data from the working directory.
        """
        return self.project_reader.read_project(self)

    def save_project(
        self,
        path: Path | str,
        name: str = "Project",
    ):
        """
        Packs the data from the working directory into a .vibra file.
        """
        self.save_path = Path(path)
        self.name = name
        if self.project_writer.project_paths.is_empty():
            self.project_writer.write_project(self)
        self.project_writer.write_file(path)

    def import_mesh(self, path: Path | str):
        """
        Loads a complete mesh from a file.

        The supported mesh formats are:
            - *.msh
        """
        mesh = Mesh().load_mesh(path)
        self.model.mesh = mesh
        self.project_writer.write_mesh(mesh)

    def import_geometry(self, path: Path | str):
        """
        Loads a geometry from a file.
        This geometry can be used to create a mesh later.

        The supported geometry formats are:
            - *.step
            - *.iges
        """
        path = Path(path)
        self.model.geometry_path = path
        # self.model.geometry = Geometry(path)
        self.project_writer.write_geometry(path)

    def update_model_properties_file(self):
        self.project_writer.write_model_properties(self.model.properties)

    def update_project_setup_file(self):
        self.project_writer.write_project_setup(self)

    def configure_mesh(self, mesh_setup: MeshSetup):
        """
        Configures how to create a mesh from a geometry.
        This method might be called before or after loading a geometry.
        """
        self.mesh_setup = mesh_setup
        self.update_project_setup_file()

    def generate_mesh(self) -> Mesh:
        """
        Generates a mesh from the loaded geometry and the
        parameters set using the configure_mesh method.

        It might raise an error if the geometry is not loaded
        or if the mesh configuration is not set.
        """
        if self.model.geometry_path is None:
            raise errors.InvalidMeshSetupError("The geometry has not been loaded yet.")

        if self.mesh_setup is None:
            raise errors.InvalidMeshSetupError("The mesh setup has not been configured yet.")

        mesh = Mesh().new_load_cad(
            self.model.geometry_path,
            self.mesh_setup,
        )

        # if mesh.disconnected_nodes:
        #     raise errors.MeshException(
        #         "The generated mesh contains disconnected nodes.",
        #         "Please check the mesh setup and try again.",
        #         nodes=mesh.disconnected_nodes,
        #     )

        if mesh.collapsed_1d_elements or mesh.collapsed_2d_elements or mesh.collapsed_3d_elements:
            message = "The generated mesh contains collapsed elements."
            message += "Please check the mesh setup and try again.\n"
            message += "Collapsed 1d elements: " + ", ".join(mesh.collapsed_1d_elements) + "\n"
            message += "Collapsed 2d elements: " + ", ".join(mesh.collapsed_2d_elements) + "\n"
            message += "Collapsed 3d elements: " + ", ".join(mesh.collapsed_3d_elements)

            raise errors.MeshException(
                message,
                edges=mesh.collapsed_1d_elements,
                faces=mesh.collapsed_2d_elements,
                solids=mesh.collapsed_3d_elements,
            )

        self.reset_solution()
        self.model.mesh = mesh
        self.project_writer.write_mesh(mesh)
        return mesh

    def generate_visual_mesh(self):
        if self.model.geometry_path is None:
            raise errors.InvalidMeshSetupError("The geometry has not been loaded yet.")

        self.model.process_visual_geometry_mesh(self.model.geometry_path)

    def generate_mesh_from_geometry(
        self,
        geometry_path: Path | str,
        mesh_setup: MeshSetup,
    ):
        self.import_geometry(geometry_path)
        self.configure_mesh(mesh_setup)
        self.generate_mesh()

    def configure_analysis(
        self,
        analysis_id: AnalysisID,
        analysis_setup: HarmonicAnalysisSetup | ModalAnalysisSetup,
    ):
        self.reset_solution()
        self.current_analysis_id = analysis_id
        self.model.new_set_analysis_setup(analysis_setup)
        self.update_project_setup_file()

    def solve_structural_modal_analysis(self):
        self.current_analysis_id = AnalysisID.STRUCTURAL_MODAL
        self.update_project_setup_file()

        checker = AnalysisChecker(self.model)
        checker.check_structural_modal_analysis()

        self.assembler = StructuralAssembler(self.model)
        self.solver = ModalSolver(self.assembler)
        self.postprocessing = StructuralPostprocessing(self)

        self.assembler.process_assemble()

        t0 = perf_counter()
        _, solution = self.solver.solve()
        self.project_writer.write_modal_solution(self.solver)
        dt = perf_counter() - t0
        logging.info(f"Elapsed time to solve structural modal analysis: {dt: .6f} [s]")

        return solution

    def solve_structural_harmonic_analysis(self):
        self.current_analysis_id = AnalysisID.STRUCTURAL_HARMONIC
        self.update_project_setup_file()

        checker = AnalysisChecker(self.model)
        checker.check_structural_harmonic_analysis()

        self.assembler = StructuralAssembler(self.model)
        self.solver = HarmonicSolver(self.assembler, project=self)
        self.postprocessing = StructuralPostprocessing(self)

        self.assembler.process_assemble()

        t0 = perf_counter()

        analysis_method = self.model.new_analysis_setup.analysis_method
        if analysis_method == "direct":
            solution = self.solver.solve_direct()
        elif analysis_method == "mode_superposition":
            solution = self.solver.solve_mode_superposition(is_proportionally_damped=True)
        else:
            raise ValueError(f"Unsupported analysis method: {analysis_method}")

        dt = perf_counter() - t0
        logging.info(f"Elapsed time to solve harmonic analysis: {dt: .6f} [s]")

        return solution

    def solve_acoustic_modal_analysis(self):
        self.current_analysis_id = AnalysisID.ACOUSTIC_MODAL
        self.update_project_setup_file()

        checker = AnalysisChecker(self.model)
        checker.check_acoustic_modal_analysis()

        self.assembler = AcousticAssembler(self.model)
        self.solver = ModalSolver(self.assembler)
        self.postprocessing = AcousticPostprocessing(self)

        self.assembler.process_assemble()

        t0 = perf_counter()
        _, solution = self.solver.solve()
        self.project_writer.write_modal_solution(self.solver)
        dt = perf_counter() - t0
        logging.info(f"Elapsed time to solve modal analysis: {dt: .6f} [s]")

        return solution

    def solve_acoustic_harmonic_analysis(self):
        self.current_analysis_id = AnalysisID.ACOUSTIC_HARMONIC
        self.update_project_setup_file()

        checker = AnalysisChecker(self.model)
        checker.check_acoustic_harmonic_analysis()

        self.assembler = AcousticAssembler(self.model)
        self.solver = HarmonicSolver(self.assembler, project=self)
        self.postprocessing = AcousticPostprocessing(self)

        self.model.reset_dissipation_model_properties()
        self.model.process_porous_material_properties()
        self.model.process_viscous_thermal_model_properties()
        self.model.process_perforated_plate_impedance()
        self.assembler.process_assemble()

        t0 = perf_counter()

        analysis_method = self.model.new_analysis_setup.analysis_method
        if analysis_method == "direct":
            solution = self.solver.solve_direct()
        elif analysis_method == "mode_superposition":
            solution = self.solver.solve_mode_superposition()
        else:
            raise ValueError(f"Unsupported analysis method: {analysis_method}")

        self.project_writer.write_harmonic_solution(self.solver)

        dt = perf_counter() - t0
        logging.info(f"Elapsed time to solve harmonic analysis: {dt: .6f} [s]")

        return solution

    def is_analysis_id_valid(self, analysis_id: Optional[AnalysisID]) -> bool:
        if analysis_id is None:
            analysis_id = self.current_analysis_id

        if analysis_id.is_harmonic() and isinstance(self.model.new_analysis_setup, HarmonicAnalysisSetup):
            return True

        if analysis_id.is_modal() and isinstance(self.model.new_analysis_setup, ModalAnalysisSetup):
            return True

        return False

    def is_analysis_setup_complete(self):        
        try:
            AnalysisChecker(self.model).check_analysis_id(self.current_analysis_id)
        except Exception:
            return False
        else:
            return True

    def is_there_a_valid_solution(self) -> bool:
        if self.current_analysis_id.is_acoustic() and not isinstance(self.assembler, AcousticAssembler):
            return False

        if self.current_analysis_id.is_structural() and not isinstance(self.assembler, StructuralAssembler):
            return False

        if self.current_analysis_id.is_harmonic() and not isinstance(self.solver, HarmonicSolver):
            return False

        if self.current_analysis_id.is_modal() and not isinstance(self.solver, ModalSolver):
            return False

        if self.solver is None:
            return False

        if self.solver.solution is None:
            return False

        return self.solver.solution.size > 0

    def get_analysis_type_and_physical_domain(self) -> tuple[str, str]:
        analysis_type = ""
        physical_domain = ""

        if self.current_analysis_id.is_harmonic():
            analysis_type = "harmonic"
        elif self.current_analysis_id.is_modal():
            analysis_type = "modal"
        elif self.current_analysis_id.is_static():
            physical_domain = "static"

        if self.current_analysis_id.is_acoustic():
            physical_domain = "acoustic"
        elif self.current_analysis_id.is_structural():
            physical_domain = "structural"
        elif self.current_analysis_id.is_coupled():
            analysis_type = "coupled"

        return analysis_type, physical_domain

    def mark_project_as_modified(self):
        self.needs_saving = True
