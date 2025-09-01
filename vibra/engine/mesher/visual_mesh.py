import numpy as np
from pathlib import Path


class VisualMesh:
    def __init__(self):
        self.clear()

    def clear(self):
        self.coords = np.zeros((0, 3))
        self.vertices = np.zeros((0, 1))
        self.segments = np.zeros((0, 2))
        self.triangles = np.zeros((0, 3))

    def load_file(self, path: str | Path):
        pass
