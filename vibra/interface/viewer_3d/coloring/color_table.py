import numpy as np
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkRenderingCore import vtkColorTransferFunction

from molde.colors import Color
from . import color_palettes


class ColorTable(vtkLookupTable):
    def __init__(
        self,
        values_vector=None,
        min_value=None,
        max_value=None,
        colormap="jet",
    ):
        self.set_data(values_vector, min_value, max_value)
        self.set_colormap(colormap)

    def set_data(
        self,
        values_vector: np.ndarray,
        min_value: int | None = None,
        max_value: int | None = None,
    ):
        self.values_vector = values_vector

        if min_value is None:
            self.min_value: float = np.min(self.values_vector)

        if max_value is None:
            self.max_value: float = np.max(self.values_vector)

        self.SetTableRange(min_value, max_value)

    def set_colormap(self, colormap: str):
        # just to make sure it has no uppercases or extra spaces
        self.colormap = colormap.strip().lower()

        if self.colormap == "grayscale":
            self._set_colors(color_palettes.grey_colors)
        elif self.colormap == "jet":
            self._set_colors(color_palettes.jet_colors)
        elif self.colormap == "viridis":
            self._set_colors(color_palettes.viridis_colors)
        elif self.colormap == "inferno":
            self._set_colors(color_palettes.inferno_colors)
        elif self.colormap == "magma":
            self._set_colors(color_palettes.magma_colors)
        elif self.colormap == "plasma":
            self._set_colors(color_palettes.plasma_colors)
        elif self.colormap == "bwr":
            self._set_colors(color_palettes.bwr_colors)
        elif self.colormap == "piyg":
            self._set_colors(color_palettes.PiYG_colors)
        elif self.colormap == "prgn":
            self._set_colors(color_palettes.PRGn_colors)
        elif self.colormap == "brbg":
            self._set_colors(color_palettes.BrBG_colors)
        elif self.colormap == "puor":
            self._set_colors(color_palettes.PuOR_colors)
        else:
            print(f'Invalid colormap "{self.colormap}". Using "viridis" instead.')
            self._set_colors(color_palettes.viridis_colors)

    def get_color(self, value) -> Color:
        # yes, vtk uses the list as a python pointer
        # instead of returning a tuple...
        tmp = [0, 0, 0]
        self.GetColor(np.real(value), tmp)
        return Color.from_rgb_f(*tmp)

    def _set_colors(self, colors, shades=256):
        color_transfer = vtkColorTransferFunction()
        for i, color in enumerate(colors):
            color_transfer.AddRGBPoint(i / (len(colors) - 1), *color)

        self.SetNumberOfColors(shades)
        for i in range(shades):
            interpolated_color = color_transfer.GetColor(i / (shades - 1))
            normalized_color = [i / 255 for i in interpolated_color]
            self.SetTableValue(i, *normalized_color)
        self.Build()
