
from vibra import app
from vibra.engine import AnalysisID
from vibra.engine.model import Model
from vibra.engine.assemblers.acoustic_assembler import AcousticAssembler
from vibra.engine.assemblers.structural_assembler import StructuralAssembler
from vibra.engine.solvers.acoustic_harmonic_solver import AcousticHarmonicSolver
from vibra.engine.solvers.acoustic_modal_solver import AcousticModalSolver
from vibra.engine.solvers.structural_modal_solver import StructuralModalSolver
from vibra.engine.solvers.structural_harmonic_solver import StructuralHarmonicSolver
from vibra.engine.checkers.analysis_requirements_checker import AnalysisRequirementsChecker

from vibra.interface.process_analysis import ProcessAnalysis
from vibra.interface.mesh.mesher_inputs import MesherInputs
from vibra.interface.loading_window import LoadingWindow

import logging
from time import sleep, time


class Project:
    def __init__(self):
        self.reset_variables()

    def reset_variables(self):

        self.name = "Project"
        self.fluid_list_path = ""
        self.material_list_path = ""

        self.thumbnail = None
        self.save_path = None

        self.analysis_data = dict()
        self.analysis_id = AnalysisID.NO_ANALYSIS

        self.model = Model()
        self.acoustic_assembler = AcousticAssembler(self.model)
        self.structural_assembler = StructuralAssembler(self.model)

        self.static_solver = None
        self.acoustic_modal_solver = None
        self.structural_modal_solver = None
        self.acoustic_harmonic_solver = None
        self.structural_harmonic_solver = None

        self.last_analysis = None
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

        if len(self.analysis_data) == 0:
            return

        self.create_solver()

    def import_geometry(self, path : str):
        self.model.set_geometry_path(path)
        logging.info("Importing geometry file...")
        return self.model.process_visual_geometry_mesh(path)

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

    def set_acoustic_element_to_model(self):
        self.model.set_acoustic_element(self.acoustic_assembler.get_element())

    def set_structural_element_to_model(self):
        self.model.set_structural_element(self.structural_assembler.get_element())

    def generate_mesh(self):
        if self.model is None:
            return
        self.model.process_mesh()

    def set_analysis_data(self, data: dict):
        self.analysis_data = data
        self.model.set_frequency_setup(data)

    def is_analysis_setup_complete(self):

        analysis_setup = app().file.read_analysis_setup_from_file()
        if isinstance(analysis_setup, dict):
            analysis_id = analysis_setup.get("analysis_id", AnalysisID.NO_ANALYSIS)

            if analysis_id in [
                AnalysisID.STRUCTURAL_MODAL,
                AnalysisID.ACOUSTIC_MODAL,
            ]:
                if "modes" in analysis_setup.keys():
                    if not isinstance(analysis_setup["modes"], int):
                        return False
                else:
                    return False

                if "sigma_factor" in analysis_setup.keys():
                    if not isinstance(analysis_setup["sigma_factor"], int | float):
                        return False
                else:
                    return False

                return True

            elif analysis_id in [
                AnalysisID.STRUCTURAL_HARMONIC_DIRECT_METHOD,
                AnalysisID.STRUCTURAL_HARMONIC_MODE_SUPERPOSITION,
                AnalysisID.ACOUSTIC_HARMONIC,
            ]:
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

        data = self.analysis_data
        if "analysis_id" in data.keys():

            # structural harmonic analysis - direct method
            if data["analysis_id"] == AnalysisID.STRUCTURAL_HARMONIC_DIRECT_METHOD:
                self.set_structural_element_to_model()
                self.structural_harmonic_solver = StructuralHarmonicSolver(self.structural_assembler, analysis_data=data)
                self.analysis_id = AnalysisID.STRUCTURAL_HARMONIC_DIRECT_METHOD

            # structural harmonic analysis - mode superposition method
            elif data["analysis_id"] == AnalysisID.STRUCTURAL_HARMONIC_MODE_SUPERPOSITION:
                print("Structural harmonic analysis (mode superposition method) not implemented")
                raise NotImplementedError("Not implemented solver")

            # structural modal analysis
            elif data["analysis_id"] == AnalysisID.STRUCTURAL_MODAL:
                self.set_structural_element_to_model()
                self.structural_modal_solver = StructuralModalSolver(self.structural_assembler, analysis_data=data)
                self.analysis_id = AnalysisID.STRUCTURAL_MODAL

            # acoustic harmonic analysis
            elif data["analysis_id"] == AnalysisID.ACOUSTIC_HARMONIC:
                self.set_acoustic_element_to_model()
                self.acoustic_harmonic_solver = AcousticHarmonicSolver(self.acoustic_assembler, analysis_data=data)
                self.analysis_id = AnalysisID.ACOUSTIC_HARMONIC

            # acoustic modal analysis
            elif data["analysis_id"] == AnalysisID.ACOUSTIC_MODAL:
                self.set_acoustic_element_to_model()
                self.acoustic_modal_solver = AcousticModalSolver(self.acoustic_assembler, analysis_data=data)
                self.analysis_id = AnalysisID.ACOUSTIC_MODAL

            # coupled harmonic analysis (direct method)
            elif data["analysis_id"] == AnalysisID.COUPLED_HARMONIC_DIRECT_METHOD:
                print("Coupled harmonic analysis (direct method) not implemented")
                raise NotImplementedError("Not implemented solver")

            # coupled harmonic analysis (mode superposition method)
            elif data["analysis_id"] == AnalysisID.COUPLED_HARMONIC_MODE_SUPERPOSITION:
                print("Coupled harmonic analysis (mode superposition method) not implemented")
                raise NotImplementedError("Not implemented solver")

            # static analysis
            elif data["analysis_id"] == AnalysisID.STATIC_ANALYSIS:
                print("Static analysis not implemented")
                raise NotImplementedError("Not implemented solver")

            else:
                raise NotImplementedError("Not implemented solver")

    def set_element_formulation(self, element):
        self.acoustic_assembler.set_element_formulation(element)
        self.structural_assembler.set_element_formulation(element)

    def solve_acoustic_modal_analysis(self):
        self.model.reset_dissipation_model_properties()
        self.acoustic_assembler.process_assemble()
        t0 = time()
        self.acoustic_modal_solver.solve()
        dt = time() - t0
        print(f"Elapsed time to solve modal analysis: {round(dt, 6)} [s]")
        self.last_analysis = "Modal Acoustic"
        app().file.write_results_data_in_file()
        app().main_window.disable_advanced_acoustic_plots_buttons(True)

    def solve_structural_modal_analysis(self):
        self.structural_assembler.process_assemble()
        self.structural_modal_solver.solve()
        self.last_analysis = "Modal Structural"
        app().file.write_results_data_in_file()
        app().main_window.disable_advanced_acoustic_plots_buttons(True)

    def solve_acoustic_harmonic_analysis(self):
        self.model.reset_dissipation_model_properties()
        self.model.process_porous_material_properties(self.model.frequencies)
        self.model.process_viscous_thermal_model_properties(self.model.frequencies)
        self.model.process_perforated_plate_impendace(self.model.frequencies)
        self.acoustic_assembler.process_assemble()
        t0 = time()
        self.acoustic_harmonic_solver.solve()
        dt = time() - t0
        self.last_analysis = "Harmonic Acoustic"
        print(f"Elapsed time to solve harmonic analysis: {round(dt, 6)} [s]")
        app().file.write_results_data_in_file()
        app().main_window.disable_advanced_acoustic_plots_buttons(False)

    def solve_structural_harmonic_analysis(self):
        self.structural_assembler.process_assemble()
        t0 = time()
        if self.analysis_data["analysis_id"] == AnalysisID.STRUCTURAL_HARMONIC_DIRECT_METHOD:
            self.structural_harmonic_solver.solve_direct_method()
        else:
            self.structural_harmonic_solver.solve_mode_superposition_method()
            return
        dt = time() - t0
        self.last_analysis = "Harmonic Structural"
        print(f"Elapsed time to solve harmonic analysis: {round(dt, 6)} [s]")
        app().file.write_results_data_in_file()
    
    def run_analysis(self):

        if not self.model.generated_mesh:
            obj = MesherInputs(close_after_generate=True)
            if obj.complete:
                app().main_window.update_plots()
            else:
                return

        if len(self.analysis_data) == 0:
            return

        analysis = ProcessAnalysis()
        analysis_id = self.analysis_data.get("analysis_id", AnalysisID.NO_ANALYSIS)

        checker = AnalysisRequirementsChecker()

        if analysis_id in [
            AnalysisID.STRUCTURAL_HARMONIC_DIRECT_METHOD,
            AnalysisID.STRUCTURAL_HARMONIC_MODE_SUPERPOSITION,
        ]:
            if checker.check_structural_harmonic_analysis():
                return True
            LoadingWindow(analysis.process_structural_harmonic_analysis).run()

        elif analysis_id == AnalysisID.STRUCTURAL_MODAL:
            if checker.check_structural_modal_analysis():
                return True
            LoadingWindow(analysis.process_structural_modal_analysis).run()

        elif analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            if checker.check_acoustic_harmonic_analysis():
                return True
            LoadingWindow(analysis.process_acoustic_harmonic_analysis).run()

        elif analysis_id == AnalysisID.ACOUSTIC_MODAL:
            if checker.check_acoustic_modal_analysis():
                return True
            LoadingWindow(analysis.process_acoustic_modal_analysis).run()

        else:
            raise NotImplementedError("Not implemented analysis")

        app().main_window.results_viewer_widget.results_viewer_items.update_items()

    def long_function(self):
        for i in range(20):
            logging.info(f"long_function [{i}/20]")
            sleep(0.1)
