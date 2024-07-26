import logging
from pathlib import Path
from time import sleep

from vibra import app
from vibra.engine.model import Model
from vibra.engine.assemblers.acoustic_assembler import AcousticAssembler
from vibra.engine.assemblers.structural_assembler import StructuralAssembler
from vibra.engine.solvers.acoustic_harmonic_solver import AcousticHarmonicSolver
from vibra.engine.solvers.acoustic_modal_solver import AcousticModalSolver
from vibra.engine.solvers.structural_modal_solver import StructuralModalSolver
from vibra.utils.progress_status import ProgressStatus


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

        self.analysis_data = None
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

    def reset_solutions(self):

        if self.static_solver is not None:
            self.static_solver.reset_variables()

        if self.acoustic_modal_solver is not None:
            self.acoustic_modal_solver.reset_variables()

        if self.structural_modal_solver is not None:
            self.structural_modal_solver.reset_variables()

        if self.acoustic_harmonic_solver is not None:
            self.acoustic_harmonic_solver.reset_variables()

        if self.structural_modal_solver is not None:
            self.structural_modal_solver.reset_variables()

        if self.structural_harmonic_solver is not None:
            self.structural_harmonic_solver.reset_variables()

        if self.analysis_data is None:
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

    def set_acoustic_pressure(self, data, surface):
        self.model.set_acoustic_pressure(data, surface)

    def set_mass_flow_rate(self, data, surface):
        self.model.set_mass_flow_rate(data, surface)

    def set_volume_velocity(self, data, surface):
        self.model.set_volume_velocity(data, surface)

    def set_surface_velocity(self, data, surface):
        self.model.set_surface_velocity(data, surface)

    def set_specific_impedance(self, data, surface):
        self.model.set_specific_impedance(data, surface)

    def set_dissipation_model(self, data, volume):
        self.model.set_dissipation_model_data(data, volume=volume)

    def set_porous_material_model(self, data, **kwargs):
        self.model.set_porous_material_model_data(data, **kwargs)

    def set_lrf_eq_model_data(self, data, group=None, volume=None):
        self.model.set_lrf_eq_model_data(data, group=group, volume=volume)

    def set_analysis_data(self, data):
        self.analysis_data = data
        self.acoustic_assembler.set_analysis_data(data)
        self.structural_assembler.set_analysis_data(data)

    def set_frequencies(self, frequencies, f_min, f_max, f_step, imported_table):

        analysis_data = self.analysis_data

        if isinstance(analysis_data, dict):
            analysis_data["frequencies"] = frequencies
            analysis_data["f_min"] = f_min
            analysis_data["f_max"] = f_max
            analysis_data["f_step"] = f_step

        else:
            analysis_data = {   
                            "frequencies": frequencies,
                            "f_min": f_min,
                            "f_max": f_max,
                            "f_step": f_step
                           }

        if imported_table:
            analysis_data["imported_table"] = imported_table

        self.set_analysis_data(analysis_data)

    def create_solver(self):
        """ """

        data = self.analysis_data
        if "analysis_id" in data.keys():
            # structural harmonic analysis - direct method
            if data["analysis_id"] == 0:
                print("Structural harmonic analysis (direct method) not implemented")
                raise NotImplementedError("Not implemented solver")

            # structural harmonic analysis - mode superposition method
            elif data["analysis_id"] == 1:
                print("Structural harmonic analysis (mode superposition method) not implemented")
                raise NotImplementedError("Not implemented solver")

            # structural modal analysis
            elif data["analysis_id"] == 2:
                self.set_structural_element_to_model()
                self.structural_modal_solver = StructuralModalSolver(self.structural_assembler, analysis_data=data)
           
            # acoustic harmonic analysis
            elif data["analysis_id"] == 3:
                self.set_acoustic_element_to_model()
                self.acoustic_harmonic_solver = AcousticHarmonicSolver(self.acoustic_assembler, analysis_data=data)
            
            # acoustic modal analysis
            elif data["analysis_id"] == 4:
                self.set_acoustic_element_to_model()
                self.acoustic_modal_solver = AcousticModalSolver(self.acoustic_assembler, analysis_data=data)
            
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
        self.model.get_lrf_eq_data(modal=True)
        self.acoustic_assembler.process_assemble()
        self.acoustic_modal_solver.solve()
        app().main_window.file.write_results_data_in_file()
        app().main_window.advanced_results_menu.disable_advanced_acoustic_plots_buttons(True)

    def solve_structural_modal_analysis(self):
        self.structural_assembler.process_assemble()
        self.structural_modal_solver.solve()
        app().main_window.file.write_results_data_in_file()
        app().main_window.advanced_results_menu.disable_advanced_acoustic_plots_buttons(True)

    def solve_acoustic_harmonic_analysis(self):
        self.model.get_lrf_eq_data()
        self.model.process_lrf_properties(self.analysis_data["frequencies"])
        self.model.process_porous_material_properties(self.analysis_data["frequencies"])
        self.acoustic_assembler.process_assemble()
        self.acoustic_harmonic_solver.solve()
        app().main_window.file.write_results_data_in_file()
        app().main_window.advanced_results_menu.disable_advanced_acoustic_plots_buttons(False)

    def long_function(self):
        for i in range(20):
            logging.info("long_function" + ProgressStatus(i, 20))
            sleep(0.1)