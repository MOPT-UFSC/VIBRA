import numpy as np
from vtkmodules.vtkFiltersSources import vtkArrowSource
from vtkmodules.vtkRenderingCore import vtkRenderer

from vibra.interface.viewer_3d.actors.symbols.symbols_common import (
    X_VECTOR,
    Y_VECTOR,
    Z_VECTOR,
    SymbolActorCommon,
    load_symbol,
)


class ForceSymbol(SymbolActorCommon):
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
        positions: list[tuple[float, float, float]] = list()
        orientations: list[tuple[float, float, float]] = list()

        for i in range(10):
            pos = (i/100, 0, 0)
            vec = (i-3, 2-i, 0)
            positions.append(pos)
            orientations.append(vec)

        return positions, orientations

    def configure_appearance(self):
        self.GetProperty().SetColor(1, 0, 0)
        self.GetProperty().LightingOff()
