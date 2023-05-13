import vtk

from vibra.interface.viewer_3d.symbols_common import (
    SymbolActorCommon,
    load_symbol,
)


class SpringSymbols(SymbolActorCommon):
    def __init__(self, renderer: vtk.vtkRenderer):
        source = self.get_source()
        positions = self.get_positions()
        super().__init__(positions, source, renderer)

        self.configure_appearance()

    def get_source(self):
        return load_symbol("data/symbols/_spring.obj")

    def get_positions(self):
        return [(5, i, 0) for i in range(10)]

    def configure_appearance(self):
        self.GetProperty().SetColor(0.38, 0.01, 0.27)
        self.GetProperty().LightingOff()


class ClampSymbols(SymbolActorCommon):
    def __init__(self, renderer: vtk.vtkRenderer):
        source = self.get_source()
        positions = self.get_positions()
        super().__init__(positions, source, renderer)

        self.configure_appearance()

    def get_source(self):
        return load_symbol("data/symbols/grampo.obj")

    def get_positions(self):
        return [(0, i, 5) for i in range(10)]

    def configure_appearance(self):
        self.GetProperty().SetColor(0.89, 0.70, 0.02)
        self.GetProperty().LightingOff()


class ArrowSymbols(SymbolActorCommon):
    def __init__(self, renderer: vtk.vtkRenderer):
        source = self.get_source()
        positions = self.get_positions()
        super().__init__(positions, source, renderer)

        self.configure_appearance()

    def get_source(self):
        return load_symbol("data/symbols/_arrow.obj")

    def get_positions(self):
        return [(5, i, 5) for i in range(10)]

    def configure_appearance(self):
        self.GetProperty().SetColor(0.58, 0.09, 0.05)
        self.GetProperty().LightingOff()


class ArrowSymbols2(SymbolActorCommon):
    def __init__(self, renderer: vtk.vtkRenderer):
        source = self.get_source()
        positions = self.get_positions()
        super().__init__(positions, source, renderer)

        self.configure_appearance()

    def get_source(self):
        return load_symbol("data/symbols/_arrow.obj")

    def get_positions(self):
        return [(-5, i, 0) for i in range(10)]

    def configure_appearance(self):
        self.GetProperty().SetColor(0.06, 0.49, 0.49)
        self.GetProperty().LightingOff()


class ArrowSymbols3(SymbolActorCommon):
    def __init__(self, renderer: vtk.vtkRenderer):
        source = self.get_source()
        positions = self.get_positions()
        super().__init__(positions, source, renderer)

        self.configure_appearance()

    def get_source(self):
        return load_symbol("data/symbols/_arrow.obj")

    def get_positions(self):
        return [(0, i, -5) for i in range(10)]

    def configure_appearance(self):
        self.GetProperty().SetColor(0, 0.26, 0.66)
        self.GetProperty().LightingOff()
