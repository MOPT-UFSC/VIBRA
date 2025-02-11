import logging
from pathlib import Path
from time import sleep, time

from vibra import app
from vibra.engine.model import Model
from vibra.engine.assemblers.acoustic_assembler import AcousticAssembler
from vibra.engine.assemblers.structural_assembler import StructuralAssembler
from vibra.engine.solvers.acoustic_harmonic_solver import AcousticHarmonicSolver
from vibra.engine.solvers.acoustic_modal_solver import AcousticModalSolver
from vibra.engine.solvers.structural_modal_solver import StructuralModalSolver
from vibra.engine.solvers.structural_harmonic_solver import StructuralHarmonicSolver
from vibra.utils.progress_status import ProgressStatus

import numpy as np

class Project:
    def __init__(self):
        self.reset_variables()

    def reset_variables(self):
        #
        self.name = "Project"
        self.thumbnail = None
        #
        self.save_path = None

        self.fluid_list_path = ""
        self.material_list_path = ""

        self.analysis_data = dict()
        self.dissipation_model = None
        #
        self.model = Model()
        self.acoustic_assembler = AcousticAssembler(self.model)
        self.structural_assembler = StructuralAssembler(self.model)
        #
        self.static_solver = None
        self.acoustic_modal_solver = None
        self.structural_modal_solver = None
        self.acoustic_harmonic_solver = None
        self.structural_harmonic_solver = None
        #
        self.last_analysis = None

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

    def get_fluid_list_path(self):
        return self.fluid_list_path

    def get_material_list_path(self):
        return self.material_list_path

    def set_fluid_list_path(self, path):
        self.fluid_list_path = path

    def set_material_list_path(self, path):
        self.material_list_path = path

    def import_geometry(self, path : str):
        self.model.set_geometry_path(path)
        logging.info(f"Importing geometry file...")
        return self.model.process_visual_geometry_mesh(path)

    def set_fluid(self, fluid, **kwargs):
        self.model.set_fluid(fluid, **kwargs)

    def set_material(self, material, **kwargs):
        self.model.set_material(material, **kwargs)

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

    def set_structural_boundary_condition(self, data, line, surface):
        self.model.set_structural_boundary_condition(data, line, surface)

    def set_dissipation_model(self, data, volume):
        self.model.set_dissipation_model_data(data, volume=volume)

    def set_porous_material_model(self, data, **kwargs):
        self.model.set_porous_material_model_data(data, **kwargs)

    def set_viscous_thermal_model(self, data, **kwargs):
        self.model.set_viscous_thermal_model_data(data, **kwargs)

    def set_analysis_data(self, data: dict):
        self.analysis_data = data
        self.model.set_frequency_setup(data)

    def create_solver(self):
        """ """

        data = self.analysis_data
        if "analysis_id" in data.keys():

            # structural harmonic analysis - direct method
            if data["analysis_id"] == 0:
                self.set_structural_element_to_model()
                self.structural_harmonic_solver = StructuralHarmonicSolver(self.structural_assembler, analysis_data=data)

            # structural harmonic analysis - mode superposition method
            elif data["analysis_id"] == 1:
                print("Structural harmonic analysis (mode superposition method) not implemented")
                raise NotImplementedError("Not implemented solver")

            # structural modal analysis
            elif data["analysis_id"] == 2:
                self.set_structural_element_to_model()
                self.structural_modal_solver = StructuralModalSolver(self.structural_assembler, analysis_data=data)
                self.last_analysis = "Modal Structural"
           
            # acoustic harmonic analysis
            elif data["analysis_id"] == 3:
                self.set_acoustic_element_to_model()
                self.acoustic_harmonic_solver = AcousticHarmonicSolver(self.acoustic_assembler, analysis_data=data)
                self.last_analysis = "Harmonic Acoustic"
            
            # acoustic modal analysis
            elif data["analysis_id"] == 4:
                self.set_acoustic_element_to_model()
                self.acoustic_modal_solver = AcousticModalSolver(self.acoustic_assembler, analysis_data=data)
                self.last_analysis = "Modal Acoustic"
            
            # couled harmonic analysis (direct method)
            elif data["analysis_id"] == 5:
                print("Coupled harmonic analysis (direct method) not implemented")
                raise NotImplementedError("Not implemented solver")

            # couled harmonic analysis (mode superposition method)
            elif data["analysis_id"] == 6:
                print("Coupled harmonic analysis (mode superposition method) not implemented")
                raise NotImplementedError("Not implemented solver")

            # static analysis
            elif data["analysis_id"] == 7:
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
        app().project.last_analysis = "Modal Acoustic"
        app().file.write_results_data_in_file()
        app().main_window.disable_advanced_acoustic_plots_buttons(True)

    def solve_structural_modal_analysis(self):
        self.structural_assembler.process_assemble()
        self.structural_modal_solver.solve()
        app().project.last_analysis = "Modal Structural"
        app().file.write_results_data_in_file()
        app().main_window.disable_advanced_acoustic_plots_buttons(True)

    def solve_acoustic_harmonic_analysis(self):
        self.model.reset_dissipation_model_properties()
        self.model.process_porous_material_properties(self.model.frequencies)
        self.model.process_viscous_thermal_model_properties(self.model.frequencies)
        self.acoustic_assembler.process_assemble()
        t0 = time()
        self.acoustic_harmonic_solver.solve()
        dt = time() - t0
        app().project.last_analysis = "Harmonic Acoustic"
        print(f"Elapsed time to solve harmonic analysis: {round(dt, 6)} [s]")
        app().file.write_results_data_in_file()
        app().main_window.disable_advanced_acoustic_plots_buttons(False)

    def solve_structural_harmonic_analysis(self):
        self.structural_assembler.process_assemble()
        t0 = time()
        if self.analysis_data["analysis_id"] == 0:
            self.structural_harmonic_solver.solve_direct_method()
        else:
            self.structural_harmonic_solver.solve_mode_superposition_method()
            return
        dt = time() - t0
        print(f"Elapsed time to solve harmonic analysis: {round(dt, 6)} [s]")
        app().file.write_results_data_in_file()

    def long_function(self):
        for i in range(20):
            logging.info("long_function" + ProgressStatus(i, 20))
            sleep(0.1)