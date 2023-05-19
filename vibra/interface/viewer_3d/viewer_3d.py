import vtk
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QFrame, QVBoxLayout
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from vibra.interface.viewer_3d.arcball_camera import (
    vtkInteractorStyleArcballCamera,
)
from vibra.interface.viewer_3d.selection_interactor import SelectionInteractor
from vibra.interface.viewer_3d.example_renderer import ExampleRenderer
from vibra.interface.viewer_3d.model_renderer import ModelRenderer


class Viewer3D(QFrame):
    def __init__(self, parent=None, project=None):
        super().__init__(parent)

        self.project = project
        self.example_renderer = ExampleRenderer()
        self.model_renderer = ModelRenderer()

        # Use only to access the current renderer easily
        self.current_renderer = None

        self.style = SelectionInteractor()
        self.render_interactor = QVTKRenderWindowInteractor(self)
        self.render_interactor.Initialize()
        self.render_interactor.SetInteractorStyle(self.style)
        self.set_renderer(self.model_renderer)
        self.style.AddObserver("SelectionEvent", self.selection_callback)

        layout = QVBoxLayout()
        layout.addWidget(self.render_interactor)
        self.setLayout(layout)

        self.create_axes()

    def show_example_renderer(self):
        self.set_renderer(self.example_renderer)

    def show_model_renderer(self):
        self.set_renderer(self.model_renderer)

    def set_project(self, project):
        self.project = project
        self.model_renderer.set_project(project)

    def set_renderer(self, renderer):
        if renderer == self.current_renderer:
            return

        if self.current_renderer is not None:
            self.render_interactor.GetRenderWindow().RemoveRenderer(self.current_renderer)

        self.render_interactor.GetRenderWindow().AddRenderer(renderer)
        renderer.ResetCamera()
        self.current_renderer = renderer

    def set_theme(self, theme):
        self.example_renderer.set_theme(theme)
        self.model_renderer.set_theme(theme)

    def save_png(self, path):
        imageFilter = vtk.vtkWindowToImageFilter()
        imageFilter.SetInput(self.render_interactor.GetRenderWindow())
        writer = vtk.vtkPNGWriter()
        writer.SetFileName(path)
        writer.SetInputConnection(imageFilter.GetOutputPort())
        writer.Write()

    def create_axes(self):
        axes_actor = vtk.vtkAxesActor()

        x_property = axes_actor.GetXAxisCaptionActor2D().GetCaptionTextProperty()
        y_property = axes_actor.GetYAxisCaptionActor2D().GetCaptionTextProperty()
        z_property = axes_actor.GetZAxisCaptionActor2D().GetCaptionTextProperty()

        for i in [x_property, y_property, z_property]:
            i.ItalicOff()
            i.BoldOff()

        self.axes = vtk.vtkOrientationMarkerWidget()
        self.axes.SetOrientationMarker(axes_actor)
        self.axes.SetInteractor(self.render_interactor)
        self.axes.EnabledOn()
        self.axes.InteractiveOff()

    def selection_callback(self, obj, event):
        if self.current_renderer == self.model_renderer:
            self.model_renderer.update_selection(obj)

    def update(self):
        super().update()
        self.model_renderer.update_actors()
        self.example_renderer.update_actors()
