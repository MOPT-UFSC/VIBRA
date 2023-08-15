import logging
from pathlib import Path
from time import sleep

from vibra.engine.model import Model
from vibra.engine.assemblers.acoustic_assembler import AcousticAssembler
from vibra.engine.assemblers.structural_assembler import StructuralAssembler
from vibra.engine.solvers.acoustic_modal_solver import AcousticModalSolver
from vibra.engine.solvers.acoustic_harmonic_solver import AcousticHarmonicSolver
from vibra.engine.solvers.structural_modal_solver import StructuralModalSolver

from vibra.project_file import ProjectFile
from vibra.utils.progress_status import ProgressStatus


class Project:
    def __init__(self):
        self.reset_variables()

    def reset_variables(self):
        #
        self.name = "Project"
        self.geometry_path = ""
        self.fluid_list_path = ""
        self.material_list_path = ""
        self.analysis_data = None
        self.dissipation_model = None
        #
        self.model = Model()
        self.file = ProjectFile()
        self.acoustic_assembler = AcousticAssembler(self.model)
        self.structural_assembler = StructuralAssembler(self.model)

        # default stuff to make the merge work
        self.acoustic_modal_solver = StructuralModalSolver(self.acoustic_assembler)
        self.structural_modal_solver = StructuralModalSolver(self.structural_assembler)
        self.acoustic_harmonic_solver = AcousticHarmonicSolver(self.acoustic_assembler)

    @classmethod
    def load(cls, path):
        logging.info(f"Loading {path}")

    def save(self, path):
        logging.info(f"Saving project in my/save/path")

    def get_fluid_list_path(self):
        return self.fluid_list_path

    def get_material_list_path(self):
        return self.material_list_path

    def set_fluid_list_path(self, path):
        self.fluid_list_path = path

    def set_material_list_path(self, path):
        self.material_list_path = path

    def import_geometry(self, path):
        self.geometry_path = Path(path)
        self.model.set_geometry_path(Path(path))
        logging.info(f"Importing geometry at {path}")
        self.model.process_visual_geometry_mesh()

    def set_fluid(self, fluid):
        self.model.set_fluid(fluid)

    def set_material(self, material):
        self.model.set_material(material)

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

    def set_structural_boundary_condition(self, data):
        self.model.set_structural_boundary_condition(data)
        self.file.add_structural_boundary_condition_to_file(data)

    def set_acoustic_pressure(self, data):
        self.model.set_acoustic_pressure(data)
        self.file.add_acoustic_pressure_to_file(data)

    def set_mass_flow_rate(self, data):
        self.model.set_mass_flow_rate(data)
        self.file.add_mass_flow_rate_to_file(data)

    def set_volume_velocity(self, data):
        self.model.set_volume_velocity(data)
        self.file.add_volume_velocity_to_file(data)

    def set_particle_velocity(self, data):
        self.model.set_particle_velocity(data)
        self.file.add_particle_velocity_to_file(data)

    def set_dissipation_model(self, data):
        self.model.set_dissipation_model_data(data)
        self.file.add_dissipation_model_data_to_file(data)

    def set_analysis_data(self, data):

        self.analysis_data = data
        self.file.add_frequency_in_file(data)

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
            self.structural_modal_solver = StructuralModalSolver(self.structural_assembler, 
                                                                 analysis_data=data)
        # acoustic harmonic analysis        
        elif data["analysis_id"] == 3:
            self.set_acoustic_element_to_model()
            self.acoustic_harmonic_solver = AcousticHarmonicSolver(self.acoustic_assembler, 
                                                                   analysis_data=data)
        # acoustic modal analysis
        elif data["analysis_id"] == 4:
            self.set_acoustic_element_to_model()
            self.acoustic_modal_solver = AcousticModalSolver(self.acoustic_assembler, 
                                                             analysis_data=data)
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

    def set_frequencies(self, frequencies, f_min, f_max, f_step):
        analysis_data = self.analysis_data
        if analysis_data is not None:
            analysis_data["frequencies"] = frequencies
            analysis_data["f_min"] = f_min
            analysis_data["f_max"] = f_max
            analysis_data["f_step"] = f_step
            self.set_analysis_data(analysis_data)
            # self.frequencies = frequencies
            # self.acoustic_assembler.set_frequencies(frequencies)
            # self.structural_assembler.set_frequencies(frequencies)

    def set_element_formulation(self, element):
        self.acoustic_assembler.set_element_formulation(element)
        self.structural_assembler.set_element_formulation(element)

    def solve_acoustic_modal_analysis(self):
        self.acoustic_assembler.assemble_global_matrices()
        self.acoustic_modal_solver.solve()

    def solve_structural_modal_analysis(self):
        self.structural_assembler.assemble_global_matrices()
        self.structural_modal_solver.solve()

    def solve_acoustic_harmonic_analysis(self):
        self.acoustic_assembler.assemble_global_matrices()
        self.acoustic_harmonic_solver.solve()

    def long_function(self):
        for i in range(20):
            logging.info("long_function" + ProgressStatus(i, 20))
            sleep(0.1)
