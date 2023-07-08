import logging
from pathlib import Path
from time import sleep

from vibra.engine.assemblers.modal_assembler import ModalAssembler
from vibra.engine.model import Model
from vibra.engine.assemblers.modal_assembler import ModalAssembler
from vibra.engine.solvers.modal_solver import ModalSolver
from vibra.engine.solvers.example_solver import ExampleSolver
from vibra.engine.solvers.modal_solver import ModalSolver
from vibra.utils.progress_status import ProgressStatus



class Project:
    def __init__(self):
        self.reset_variables()
        self.model = Model()
        self.example_solver = ExampleSolver()
        self.modal_assembler = ModalAssembler(self.model)
        self.modal_solver = ModalSolver(self.modal_assembler)

    def reset_variables(self):
        self.name = "Project"
        self.geometry_path = ""
        self.fluid_list_path = ""
        self.material_list_path = ""

        self.model = Model()
        self.modal_assembler = ModalAssembler(self.model)
        self.example_solver = ExampleSolver()
        self.modal_solver = ModalSolver(self.modal_assembler)
        self.analysis_data = {}

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
        self.example_solver.set_analysis_data(data)

    def solve_example(self):
        pass
        # self.example_solver.solve()

    def set_element_formulation(self, element):
        self.modal_assembler.set_element_formulation(element)

    def solve_modal_acoustic(self):
        self.modal_assembler.assemble_global_matrices()
        self.modal_solver.solve(modes=10)

    def long_function(self):
        for i in range(20):
            logging.info("long_function" + ProgressStatus(i, 20))

            # print(i)
            sleep(0.1)
