import logging
from pathlib import Path
from time import sleep

from vibra.engine.assemblers.modal_assembler import ModalAssembler
from vibra.engine.model import Model
from vibra.engine.assemblers.acoustic_modal_assembler import AcousticModalAssembler
from vibra.engine.assemblers.structural_modal_assembler import StructuralModalAssembler
from vibra.engine.solvers.modal_solver import ModalSolver
from vibra.engine.solvers.example_solver import ExampleSolver
from vibra.engine.solvers.modal_solver import ModalSolver
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
        #
        self.model = Model()
        self.acoustic_modal_assembler = AcousticModalAssembler(self.model)
        self.structural_modal_assembler = StructuralModalAssembler(self.model)
        self.acoustic_modal_solver = ModalSolver(self.acoustic_modal_assembler)
        self.structural_modal_solver = ModalSolver(self.structural_modal_assembler)

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

    def generate_mesh(self):
        if self.model is None:
            return
        self.model.process_mesh()

    def set_analysis_data(self, data):
        self.analysis_data = data
        if data["analysis_id"] == 2:
            self.structural_modal_solver = ModalSolver(self.structural_modal_assembler, analysis_data=data)
        elif data["analysis_id"] == 4:
            self.acoustic_modal_solver = ModalSolver(self.acoustic_modal_assembler, analysis_data=data)
        else:
            raise NotImplementedError("Not implemented solver")

    def set_element_formulation(self, element):
        self.acoustic_modal_assembler.set_element_formulation(element)

    def solve_modal_acoustic(self):
        self.acoustic_modal_assembler.assemble_global_matrices()
        self.acoustic_modal_solver.solve()

    def long_function(self):
        for i in range(20):
            logging.info("long_function" + ProgressStatus(i, 20))

            # print(i)
            sleep(0.1)
