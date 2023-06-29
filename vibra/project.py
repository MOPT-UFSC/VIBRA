import logging
from pathlib import Path
from time import sleep

from vibra.engine.mesh import Mesh
from vibra.engine.model import Model
from vibra.engine.solvers.example_solver import ExampleSolver
from vibra.utils.progress_status import ProgressStatus


class Project:
    def __init__(self):
        self.name = "Project"
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
        logging.info(f"Importing geometry at {path}")
        self.set_model(Model(path))

    def solve_example(self):
        self.example_solver.set_model(self.model)
        self.example_solver.solve()

    def long_function(self):
        for i in range(20):
            logging.info("long_function" + ProgressStatus(i, 20))

            print(i)
            sleep(0.1)
