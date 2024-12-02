import numpy as np
from vtkmodules.vtkFiltersSources import vtkArrowSource
from vtkmodules.vtkRenderingCore import vtkRenderer

from vibra.interface.viewer_3d.actors.symbols.symbols_common import (
    SymbolActorFixedSize,
    SymbolTranform,
)


class ForceSymbol(SymbolActorFixedSize):
    def __init__(self, renderer: vtkRenderer):
        source = self.get_source()
        transforms = self.get_transforms()
        super().__init__(transforms, source)

        self.configure_appearance()

    def get_source(self):
        source = vtkArrowSource()
        source.SetTipLength(0.25)
        source.Update()
        return source.GetOutput()

    def get_transforms(self):
        transforms: list[SymbolTranform] = list()

        for i in range(10):
            t = SymbolTranform(position=(i / 10, 0, 0), orientation=(i - 3, 2 - i, 0), size=i / 10)
            transforms.append(t)

        return transforms

    def configure_appearance(self):
        self.GetProperty().SetColor(1, 0, 0)
        self.GetProperty().LightingOff()
