from PySide6.QtCore import Signal, QObject

from vibra import app
from vibra.engine import AnalysisID
from vibra.engine.model import Model
from vibra.engine.assemblers.acoustic_assembler import AcousticAssembler
from vibra.engine.assemblers.structural_assembler import StructuralAssembler

from vibra.engine.postprocessing import StructuralPostprocessing, AcousticPostprocessing
from vibra.engine.solvers.harmonic_solver import HarmonicSolver
from vibra.engine.solvers.modal_solver import ModalSolver
from vibra.engine.checkers.analysis_requirements_checker import AnalysisRequirementsChecker

from vibra.interface.process_analysis import ProcessAnalysis
from vibra.interface.model_inputs.general.mesher_setup_inputs import MesherSetupInputs
from vibra.interface.loading_window import LoadingWindow

import logging
from time import sleep, time

from vibra.project_files.project_file import ProjectFile


class Project(QObject):

    can_resume_solution_changed = Signal(bool)

    def __init__(self, project_file: ProjectFile | None = None):
        super().__init__()
        self.project_file = project_file
        self.can_resume_solution = False
        self.reset_variables()

    def __setattr__(self, key, value):
        self.__dict__[key] = value
        if key == 'can_resume_solution':
            self.can_resume_solution_changed.emit(value)

    def reset_variables(self):

        self.name = "Project"
        self.fluid_list_path = ""
        self.material_list_path = ""

        self.thumbnail = None
        self.save_path = None

        self.analysis_setup = dict()
        self.analysis_id = AnalysisID.NO_ANALYSIS

        def disable_resume_callback():
            self.can_resume_solution = False


        self.model = Model(disable_resume_callback)
        self.acoustic_assembler = AcousticAssembler(self.model)
        self.structural_assembler = StructuralAssembler(self.model)
        self.acoustic_postprocessing = AcousticPostprocessing(self)
        self.structural_postprocessing = StructuralPostprocessing(self)

        self.static_solver = None
        self.acoustic_modal_solver = None
        self.structural_modal_solver = None
        self.acoustic_harmonic_solver = None
        self.structural_harmonic_solver = None

        self.dissipation_model = None

    def reset_solutions(self):

        if self.static_solver is not None:
            self.static_solver.reset_variables()

        if self.acoustic_modal_solver is not None:
            self.acoustic_modal_solver.reset_variables()

        if self.structural_modal_solver is not None:
            self.structural_modal_solver.reset_variables()

        if self.acoustic_harmonic_solver is not None:
            self.acoustic_harmonic_solver.reset_variables()

        if self.structural_harmonic_solver is not None:
            self.structural_harmonic_solver.reset_variables()

        if len(self.analysis_setup) == 0:
            return

        self.create_solver()

    def load_project_without_process_mesh(self, path: str, geometry_file: bool):
        self.model.set_geometry_path(path)
        self.model.initialize_mesh()
        self.generated_mesh = True
        self.model.mesh.geometry_imported = geometry_file

    def import_geometry(self, path : str):
        self.model.set_geometry_path(path)
        logging.info("Importing geometry file...")
        return self.model.process_visual_geometry_mesh(path)

    def import_mesh(self, path : str):
        self.model.set_geometry_path(path)
        logging.info("Importing mesh file...")
        return self.model.process_mesh_data(path)

    def get_fluid_list_path(self):
        return self.fluid_list_path

    def get_material_list_path(self):
        return self.material_list_path

    def set_fluid_list_path(self, path):
        self.fluid_list_path = path

    def set_material_list_path(self, path):
        self.material_list_path = path

    def set_mesh_setup(self, mesh_setup):
        self.model.set_mesh_setup(mesh_setup)

    def generate_mesh(self):
        if self.model is None:
            return
        self.model.process_mesh()

    def set_analysis_setup(self, data: dict):
        self.analysis_setup = data
        self.model.set_analysis_setup(data)

    def is_analysis_setup_complete(self):

        analysis_setup = app().file.read_analysis_setup_from_file()
        if isinstance(analysis_setup, dict):
            analysis_id = analysis_setup.get("analysis_id", AnalysisID.NO_ANALYSIS)

            if analysis_id in [
                AnalysisID.STRUCTURAL_MODAL,
                AnalysisID.ACOUSTIC_MODAL,
            ]:
                if "modes_number" in analysis_setup.keys():
                    if not isinstance(analysis_setup["modes_number"], int):
                        return False
                else:
                    return False

                if "sigma_factor" in analysis_setup.keys():
                    if not isinstance(analysis_setup["sigma_factor"], int | float):
                        return False
                else:
                    return False

                return True

            elif analysis_id in [AnalysisID.STRUCTURAL_HARMONIC, AnalysisID.ACOUSTIC_HARMONIC]:
                for f_type in ["f_min", "f_max", "f_step"]:    
                    if f_type in analysis_setup.keys():
                        if not isinstance(analysis_setup[f_type], int | float):
                            return False
                    else:
                        return False
                return True

        return False

    def create_solver(self):
        """ """

        data = self.analysis_setup
        if "analysis_id" in data.keys():

            # structural harmonic analysis (both methods)
            if data["analysis_id"] == AnalysisID.STRUCTURAL_HARMONIC:
                self.structural_harmonic_solver = HarmonicSolver(self.structural_assembler, self.project_file)
                self.analysis_id = AnalysisID.STRUCTURAL_HARMONIC

            # structural modal analysis
            elif data["analysis_id"] == AnalysisID.STRUCTURAL_MODAL:
                self.structural_modal_solver = ModalSolver(self.structural_assembler)
                self.analysis_id = AnalysisID.STRUCTURAL_MODAL

            # acoustic harmonic analysis
            elif data["analysis_id"] == AnalysisID.ACOUSTIC_HARMONIC:
                self.acoustic_harmonic_solver = HarmonicSolver(self.acoustic_assembler, self.project_file)
                self.analysis_id = AnalysisID.ACOUSTIC_HARMONIC

            # acoustic modal analysis
            elif data["analysis_id"] == AnalysisID.ACOUSTIC_MODAL:
                self.acoustic_modal_solver = ModalSolver(self.acoustic_assembler)
                self.analysis_id = AnalysisID.ACOUSTIC_MODAL

            # coupled harmonic analysis (both methods)
            elif data["analysis_id"] == AnalysisID.COUPLED_HARMONIC:
                print("Coupled harmonic analysis (direct method) not implemented")
                raise NotImplementedError("Not implemented solver")

            # static analysis
            elif data["analysis_id"] == AnalysisID.STRUCTURAL_STATIC:
                print("Static analysis not implemented")
                raise NotImplementedError("Not implemented solver")

            else:
                raise NotImplementedError("Not implemented solver")

    def solve_acoustic_modal_analysis(self):
        self.acoustic_postprocessing.get_min_max_values_of_pressures.cache_clear()
        self.model.reset_dissipation_model_properties()
        self.acoustic_assembler.process_assemble()

        if self.model.stop_processing:
            return

        t0 = time()
        self.acoustic_modal_solver.solve()
        dt = time() - t0
        print(f"Elapsed time to solve modal analysis: {dt : .6f} [s]")

        app().main_window.disable_advanced_acoustic_plots_buttons(True)

    def solve_structural_modal_analysis(self):
        self.structural_postprocessing.get_max_min_values_of_displacements.cache_clear()
        self.structural_assembler.process_assemble()

        if self.model.stop_processing:
            return

        t0 = time()
        self.structural_modal_solver.solve()
        dt = time() - t0
        print(f"Elapsed time to solve structural modal analysis: {dt : .6f} [s]")

        app().main_window.disable_advanced_acoustic_plots_buttons(True)

    def solve_acoustic_harmonic_analysis(self, is_resume: bool = False):
        self.acoustic_postprocessing.get_min_max_values_of_pressures.cache_clear()
        self.model.reset_dissipation_model_properties()
        self.model.process_porous_material_properties()
        self.model.process_viscous_thermal_model_properties()
        self.model.process_perforated_plate_impedance()
        self.acoustic_assembler.process_assemble()

        if self.model.stop_processing:
            return

        t0 = time()
        self.acoustic_harmonic_solver.solve_direct(is_resume=is_resume)
        dt = time() - t0
        print(f"Elapsed time to solve harmonic analysis: {dt : .6f} [s]")

        app().main_window.disable_advanced_acoustic_plots_buttons(False)

    def solve_structural_harmonic_analysis(self):
        analisys_id = self.analysis_setup.get("analysis_id")
        analysis_method = self.analysis_setup.get("analysis_method")
        if analisys_id != AnalysisID.STRUCTURAL_HARMONIC:
            return

        self.structural_postprocessing.get_max_min_values_of_displacements.cache_clear()
        self.structural_assembler.process_assemble()
        if self.model.stop_processing:
            return

        t0 = time()
        if analysis_method == "direct":
            self.structural_harmonic_solver.solve_direct()
        else:
            self.structural_harmonic_solver.solve_mode_superposition(is_proportionally_damped=True)
        dt = time() - t0
        print(f"Elapsed time to solve harmonic analysis: {dt : .6f} [s]")

    def run_analysis(self, is_resume: bool = False):

        if not self.model.generated_mesh:
            obj = MesherSetupInputs(close_after_generate=True)
            if obj.complete:
                app().main_window.update_plots()
            else:
                return

        if len(self.analysis_setup) == 0:
            return

        analysis = ProcessAnalysis()
        analysis_id = self.analysis_setup.get("analysis_id", AnalysisID.NO_ANALYSIS)

        checker = AnalysisRequirementsChecker()
        interrupt_function = app().project.model.toggle_processing_callback

        if analysis_id in [AnalysisID.STRUCTURAL_HARMONIC]:
            if checker.check_structural_harmonic_analysis():
                return True

            LoadingWindow(
                analysis.process_structural_harmonic_analysis,
                interrupt_function,
            ).run()

        elif analysis_id == AnalysisID.STRUCTURAL_MODAL:
            if checker.check_structural_modal_analysis():
                return True

            LoadingWindow(analysis.process_structural_modal_analysis).run()

        elif analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            if checker.check_acoustic_harmonic_analysis():
                return True
            LoadingWindow(
                analysis.process_acoustic_harmonic_analysis,
                interrupt_function,    
            ).run(is_resume)

        elif analysis_id == AnalysisID.ACOUSTIC_MODAL:
            if checker.check_acoustic_modal_analysis():
                return True

            LoadingWindow(analysis.process_acoustic_modal_analysis).run()

        else:
            raise NotImplementedError("Not implemented analysis")

        app().main_window.results_viewer_widget.results_viewer_items.update_items()

    def is_there_a_valid_solution(self):

        analysis_setup = app().file.read_analysis_setup_from_file()
        if analysis_setup is None:
            return

        solvers = [
                    self.structural_harmonic_solver, 
                    self.structural_modal_solver, 
                    self.acoustic_modal_solver, 
                    self.acoustic_harmonic_solver
                    ]

        if not any(solvers):
            return False

        analysis_id = analysis_setup.get("analysis_id", AnalysisID.NO_ANALYSIS)

        if analysis_id in [AnalysisID.STRUCTURAL_HARMONIC]:
            if self.structural_harmonic_solver is None:
                return

            solution  = self.structural_harmonic_solver.solution
            if solution is not None:
                return True

        elif analysis_id == AnalysisID.STRUCTURAL_MODAL:
            if self.structural_modal_solver is None:
                return

            solution  = self.structural_modal_solver.solution
            if solution is not None:
                return True

        elif analysis_id == AnalysisID.ACOUSTIC_MODAL:
            if self.acoustic_modal_solver is None:
                return

            solution  = self.acoustic_modal_solver.solution
            if solution is not None:
                return True

        elif analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            if self.acoustic_harmonic_solver is None:
                return

            solution  = self.acoustic_harmonic_solver.solution
            if solution is not None:
                return True

        return False

    def get_analysis_type_and_physical_domain(self):

        analysis_setup = app().file.read_analysis_setup_from_file()
        if not isinstance(analysis_setup, dict):
            return "", ""

        analysis_id = analysis_setup.get("analysis_id", AnalysisID.NO_ANALYSIS)
        if analysis_id == AnalysisID.NO_ANALYSIS:
            return "", ""

        if analysis_id in [AnalysisID.STRUCTURAL_HARMONIC, AnalysisID.ACOUSTIC_HARMONIC, AnalysisID.COUPLED_HARMONIC]:
            analysis_type = "harmonic"

        elif analysis_id == AnalysisID.STRUCTURAL_STATIC:
            analysis_type = "static"

        else:
            analysis_type = "modal"

        if analysis_id in [AnalysisID.ACOUSTIC_HARMONIC, AnalysisID.ACOUSTIC_MODAL]:
            physical_domain = "acoustic"

        elif analysis_id in [AnalysisID.COUPLED_HARMONIC]:
            physical_domain = "coupled"

        else:
            physical_domain = "structural"

        return analysis_type, physical_domain

    def is_there_a_valid_analysis_setup(self, **kwargs):

        current_analysis_id = kwargs.get("current_analysis_id", None)

        analysis_setup = app().file.read_analysis_setup_from_file()
        if analysis_setup is None:
            return False

        analysis_id = analysis_setup.get("analysis_id", AnalysisID.NO_ANALYSIS)
        if analysis_id == AnalysisID.NO_ANALYSIS:
            return False

        if isinstance(current_analysis_id, int):
            if analysis_id != current_analysis_id:
                return False

        if analysis_id in [AnalysisID.ACOUSTIC_HARMONIC, AnalysisID.STRUCTURAL_HARMONIC, AnalysisID.COUPLED_HARMONIC]:
            for key in ["f_min", "f_max", "f_step"]:
                if key not in analysis_setup.keys():
                    return False
            return True

        elif analysis_id in [
                             AnalysisID.ACOUSTIC_MODAL, 
                             AnalysisID.STRUCTURAL_MODAL
                             ]:
            for key in ["modes_number", "sigma_factor"]:
                if key not in analysis_setup.keys():
                    return False
            return True

    def long_function(self):
        for i in range(20):
            logging.info(f"long_function [{i}/20]")
            sleep(0.1)