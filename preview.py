import os
import runpy
import sys
from pathlib import Path

import numpy as np
from molde import Color
from molde.render_widgets import CommonRenderWidget
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QMainWindow
from vtkmodules.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray
from vtkmodules.vtkCommonCore import vtkPoints, vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper

from vibra.engine.model import Model
from vibra.engine.project import Project
from vibra.engine.properties import Fluid, Material


class MeshActor(vtkActor):
    def __init__(self, model: Model):
        self.model = model

        self.points = None
        self.colors = None

    def build_mesh(self): 
        if self.model.mesh is None:
            return

        coords = self.model.mesh.nodal_coordinates
        face_connectivity = self.model.mesh.faces_connectivity

        self.points = vtkPoints()
        self.points.SetData(numpy_to_vtk(coords[:, 1:]))

        triangles = face_connectivity[:, 4:]
        helper = np.insert(triangles, 0, triangles.shape[1], axis=1)  # Add a "len" column at the start, as expected by VTK
        vtk_id_array = numpy_to_vtkIdTypeArray(helper.flatten())

        cells = vtkCellArray()
        cells.SetCells(len(triangles), vtk_id_array)

        data = vtkPolyData()
        data.SetPoints(self.points)
        data.SetPolys(cells)

        self.colors = vtkUnsignedCharArray()
        self.colors.SetName("color")
        self.colors.SetNumberOfComponents(3)
        self.colors.SetNumberOfTuples(data.GetNumberOfCells())
        data.GetCellData().SetScalars(self.colors)

        mapper = vtkPolyDataMapper()
        mapper.SetInputData(data)
        self.SetMapper(mapper)

        self.clear_colors()

    def clear_colors(self):
        for v in self.model.properties.volume_properties.values():
            if isinstance(v, Fluid | Material):
                self.set_color(Color.from_rgb(*v.color))
                return
        self.set_color(Color(255, 255, 255))

    def set_color(self, color: Color):
        rgb = color.to_rgb()
        for i in range(self.colors.GetNumberOfComponents()):
            self.colors.FillComponent(i, rgb[i])

    def paint_surfaces(self, surfaces: np.ndarray[int]):
        pass

    def paint_volumes(self, volumes: np.ndarray[int]):
        pass


class PreviewRenderWidget(CommonRenderWidget):
    def __init__(self):
        super().__init__()
        self.create_axes()
        self.model = None

    def update_plot(self):
        if self.model is None:
            return

        self.remove_all_actors()
        self.mesh = MeshActor(self.model)
        self.mesh.build_mesh()
        self.add_actors(self.mesh)

        self.renderer.ResetCamera()
        self.update()


class MainWindow(QMainWindow):
    def __init__(self, *, script_path):
        super().__init__()

        self.script_path = Path(script_path)

        self.render_widget = PreviewRenderWidget()
        self.setCentralWidget(self.render_widget)
        self.setBaseSize(800, 450)

        self.last_modification_time = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(16)

    def update(self):
        modification_time = self._modification_time(self.script_path)
        if modification_time <= self.last_modification_time:
            return
        self.last_modification_time = modification_time

        print("\033[H\033[2J", end="")
        script_variables = runpy.run_path(self.script_path)
        for var in script_variables.values():
            if isinstance(var, Project):
                self.render_widget.model = var.model
                self.setWindowTitle(var.model.name)
                break
        else:
            return

        self.render_widget.update_plot()

    def _modification_time(self, path: Path) -> float:
        return Path(path).stat().st_mtime


if __name__ == "__main__":
    # Make the window scale evenly for every monitor
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_QPA_PLATFORM"] = "xcb"

    if len(sys.argv) < 2:
        print("You need to add the script path")

    app = QApplication(sys.argv)
    main_window = MainWindow(script_path=sys.argv[1])
    main_window.show()

    sys.exit(app.exec())
