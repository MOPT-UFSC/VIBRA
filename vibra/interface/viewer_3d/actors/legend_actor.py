from molde import MOLDE_DIR, Color
from molde.colors import Color, color_names
from vtkmodules.vtkCommonCore import VTK_FONT_FILE, vtkPoints, vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import VTK_VERTEX, vtkPlane, vtkPolyData
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingAnnotation import vtkLegendBoxActor
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper, vtkTextProperty

from vibra import app
from vibra.utils.vtk_utils import fill_array, transform_polydata


class LegendActor(vtkLegendBoxActor):
    def __init__(self):
        self.BorderOff()
        self.ScalarVisibilityOn()
        self.number_of_entries = 0

        font_file = MOLDE_DIR / "fonts/IBMPlexMono-Regular.ttf"
        text_property: vtkTextProperty = self.GetEntryTextProperty()
        text_property.SetFontFamily(VTK_FONT_FILE)
        text_property.SetFontFile(font_file)

    def add_item(self, text: str, color: Color):
        n_spaces = 35 - len(text)
        if n_spaces > 0:
            text += n_spaces * " "

        position = len(self)
        self.SetNumberOfEntries(position + 1)

        sphere = self._create_sphere(color)

        self.SetEntryString(position, text)
        if app().config.user_preferences.interface_theme == "dark":
            text_color = [1, 1, 1]
        else:
            text_color = [0, 0, 0]

        self.SetEntryColor(position, text_color)
        self.SetEntrySymbol(position, sphere)
        self.number_of_entries += 1
        self.set_legend_position()

    def clear_legend(self):
        self.SetNumberOfEntries(0)
        pass

    def remove_item(self, position: int):
        pass

    def __len__(self) -> int:
        return self.GetNumberOfEntries()

    def set_font_size(self):
        pass

    def _create_sphere(self, color: Color):
        sphere = vtkSphereSource()
        sphere.Update()

        bounds = sphere.GetOutput().GetBounds()

        center_x = (bounds[0] + bounds[1]) / 2.0
        center_y = (bounds[2] + bounds[3]) / 2.0
        center_z = (bounds[4] + bounds[5]) / 2.0
        vertical_alignment = 0.5

        transform = vtkTransform()
        transform.Translate(-center_x, -center_y + vertical_alignment, -center_z)

        data = transform_polydata(
            sphere.GetOutput(),
            position=(-center_x, -center_y + vertical_alignment, -center_z),
        )

        colors = vtkUnsignedCharArray()
        colors.SetNumberOfComponents(3)
        colors.SetName("Colors")
        colors.InsertNextTuple3(*color.to_rgb())

        for _ in range(data.GetNumberOfPoints()):
            colors.InsertNextTuple(color.to_rgb())
        data.GetPointData().SetScalars(colors)

        return data

    def set_legend_position(self):
        x_pos = 0.8
        y_pos = 0.1
        width = 0.25
        height = 0.1 * self.number_of_entries
        self.LockBorderOff()
        self.GetPositionCoordinate().SetValue(x_pos, y_pos)
        self.GetPosition2Coordinate().SetValue(width, height)
