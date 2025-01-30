import numpy as np
from vtkmodules.vtkFiltersSources import vtkArrowSource
from vtkmodules.vtkRenderingCore import vtkRenderer

from vibra.interface.viewer_3d.actors.symbols.symbols_common import (
    X_VECTOR,
    Y_VECTOR,
    Z_VECTOR,
    SymbolActorVariableSize,
    load_symbol,
)


class ClampSymbols(SymbolActorVariableSize):
    def __init__(self, renderer: vtkRenderer):
        source = self.get_source()
        positions, orientations = self.get_positions_orientations()
        super().__init__(positions, orientations, source, renderer)

        self.configure_appearance()

    def get_source(self):
        return load_symbol("data/symbols/grampo.obj")

    def get_positions_orientations(self):
        positions = []
        orientations = []

        for i in range(4):
            positions.append((5, 5, i))
            orientations.append((0, 0, 1))

            positions.append((i, i, 5))
            orientations.append((0, 1, 0))

        return positions, orientations

    def configure_appearance(self):
        self.GetProperty().SetColor(1, 0.78, 0.34)
        self.GetProperty().LightingOff()


class ArrowSymbols(SymbolActorVariableSize):
    def __init__(self, renderer: vtkRenderer):
        source = self.get_source()
        positions, orientations = self.get_positions_orientations()
        super().__init__(positions, orientations, source, renderer)

        self.configure_appearance()

    def get_source(self):
        return load_symbol("data/symbols/_arrow.obj")

    def get_positions_orientations(self):
        positions = []
        orientations = []

        for i in np.arange(0, np.pi, 0.1):
            positions.append((np.sin(i), 6, np.cos(i)))
            orientations.append(X_VECTOR)

            positions.append((np.sin(-i), 6, np.cos(-i)))
            orientations.append(X_VECTOR)

        return positions, orientations

    def configure_appearance(self):
        self.GetProperty().SetColor(1, 0.38, 0.27)
        self.GetProperty().LightingOff()


class ArrowSymbols2(SymbolActorVariableSize):
    def __init__(self, renderer: vtkRenderer):
        source = self.get_source()
        positions, orientations = self.get_positions_orientations()
        super().__init__(positions, orientations, source, renderer)

        self.configure_appearance()

    def get_source(self):
        source = vtkArrowSource()
        source.Update()
        return source.GetOutput()

    def get_positions_orientations(self):
        positions = []
        orientations = []

        for i in range(7):
            positions.append((i, 5, 5))
            orientations.append(X_VECTOR)

            positions.append((i, 5, 5))
            orientations.append(Y_VECTOR)

            positions.append((i, 5, 5))
            orientations.append(Z_VECTOR)

        return positions, orientations

    def configure_appearance(self):
        self.GetProperty().SetColor(0.15, 0.82, 0.74)
        self.GetProperty().LightingOff()


class ArrowSymbols3(SymbolActorVariableSize):
    def __init__(self, renderer: vtkRenderer):
        source = self.get_source()
        positions, orientations = self.get_positions_orientations()
        super().__init__(positions, orientations, source, renderer)

        self.configure_appearance()

    def get_source(self):
        return load_symbol("data/symbols/_arrow.obj")

    def get_positions_orientations(self):
        positions = []
        orientations = []

        for i in range(3):
            positions.append((5, 5, i))
            orientations.append(X_VECTOR)

        return positions, orientations

    def configure_appearance(self):
        self.GetProperty().SetColor(0, 0.53, 1)
        self.GetProperty().LightingOff()
