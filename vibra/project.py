import logging
from pathlib import Path
from time import sleep

from vibra.engine.model import Model
from vibra.engine.solvers.example_solver import ExampleSolver
from vibra.utils.progress_status import ProgressStatus


class Project:
    def __init__(self):
        self.name = "Project"
        self.geometry_path = ""
        self.model = None

        self.example_solver = ExampleSolver()

    @classmethod
    def load(cls, path):
        logging.info(f"Loading {path}")

    def save(self, path):
        logging.info(f"Saving project in my/save/path")

    def set_model(self, model):
        self.model = model
        self.example_solver.set_model(model)

    def import_geometry(self, path):
        self.model = Model()
        self.geometry_path = Path(path)
        self.model.set_geometry_path(Path(path))
        logging.info(f"Importing geometry at {path}")
        self.model.process_visual_geometry_mesh()
        self.set_model(self.model)

    def set_mesh_setup(self, mesh_setup):
        self.model.set_mesh_setup(mesh_setup)

    def generate_mesh(self):
        logging.info(f"Generating mesh {self.geometry_path}")
        self.model.load_mesh()
        self.set_model(self.model)

    def solve_example(self):
        self.example_solver.set_model(self.model)
        self.example_solver.solve()

    def long_function(self):
        for i in range(20):
            logging.info("long_function" + ProgressStatus(i, 20))

            print(i)
            sleep(0.1)
