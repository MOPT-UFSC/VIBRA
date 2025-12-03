from vtkmodules.vtkCommonCore import vtkPoints, vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import VTK_VERTEX, vtkPlane, vtkPolyData
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper
from vtkmodules.vtkRenderingAnnotation import vtkLegendBoxActor
from molde import MOLDE_DIR, Color
from molde.colors import Color, color_names
from vtkmodules.vtkCommonCore import VTK_FONT_FILE
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vibra.utils.vtk_utils import fill_array, transform_polydata


from vibra import app
from molde import Color


class LegendActor(vtkLegendBoxActor):
    def __init__(self):
        self.BorderOff()
        self.ScalarVisibilityOn()

        text_property = self.GetEntryTextProperty()

        font_file = MOLDE_DIR / "fonts/IBMPlexMono-Regular.ttf"
        text_property.SetFontFamily(VTK_FONT_FILE)
        text_property.SetFontFile(font_file)

        pass

    def add_item(self, text: str, color: Color):
        position = len(self)
        self.SetNumberOfEntries(position + 1)

        sphere = self._create_sphere(color)

        self.SetEntryString(position, text)
        self.SetEntryColor(position, [1, 1, 1])  # TODO: change according to theme
        self.SetEntrySymbol(position, sphere)

        pass

    def clear_legend(self):
        self.SetNumberOfEntries(0)
        pass

    def remove_item(self, position: int):
        pass

    def __len__(self) -> int:
        return self.GetNumberOfEntries()

    def set_legend_position(self, x: float, y: float):
        pass

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

        # transform_filter = vtkTransformPolyDataFilter()
        # transform_filter.SetTransform(transform)
        # transform_filter.SetInputData(sphere.GetOutput())
        # transform_filter.Update()

        data = transform_polydata(
            sphere.GetOutput(),
            position=(-center_x, -center_y + vertical_alignment, -center_z),
        )

        colors = vtkUnsignedCharArray()
        colors.SetNumberOfComponents(3)
        colors.SetName("Colors")
        colors.InsertNextTuple3(*color.to_rgb())

        # data = transform_filter.GetOutput()
        for _ in range(data.GetNumberOfPoints()):
            colors.InsertNextTuple(color.to_rgb())
        data.GetPointData().SetScalars(colors)

        return data
