from vtkmodules.vtkFiltersSources import vtkArrowSource

from molde.colors import Color
from .new_symbols_common import SymbolActorFixedSize


class NewSymbolsActor(SymbolActorFixedSize):
    def __init__(self):
        super().__init__()
        self._register_shapes()
        self.build()

    def build(self):
        self.add_symbol(
            "arrow",
            position=(0, 0, 0),
            orientation=(1, 0, 0),
            color=Color(255, 0, 0),
        )

        self.add_symbol(
            "arrow",
            position=(0, 0, 0),
            orientation=(-1, 1, 0),
            color=Color(255, 255, 0),
        )

        super().build()

    def _register_shapes(self):
        self.register_shape("arrow", self._get_arrow_source())
        # TODO: add the following shapes
        # sphere
        # cone
        # spring
        # loadGenericOBJ
        # loadGenericSTL

    def _get_arrow_source(self):
        source = vtkArrowSource()
        source.SetTipLength(0.25)
        source.Update()
        return source.GetOutput()
