import numpy as np

from vibra.engine.solvers.solver import Solver


class ExampleSolver(Solver):
    def __init__(self):
        self._model = None
        self.tensions = None

    def set_model(self, model):
        self._model = model

    def set_analysis_data(self, data):
        self.analysis_data = data
        print(data)

    def solve(self):
        if not self.model_ready():
            raise Exception("Incomplete Model")

        n_nodes = len(self._model.mesh.nodal_coordinates)
        self.tensions = np.random.normal(size=n_nodes)

    def model_ready(self) -> bool:
        return self._model is not None
