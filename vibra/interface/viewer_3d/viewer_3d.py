import vtk
from PyQt5.QtWidgets import QFrame, QVBoxLayout
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from vibra.interface.viewer_3d.arcball_camera import (
    vtkInteractorStyleArcballCamera,
)
from vibra.interface.viewer_3d.model_renderer import ModelRenderer
from vibra.interface.viewer_3d.example_renderer import ExampleRenderer


class Viewer3D(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.example_renderer = ExampleRenderer()
        self.model_renderer = ModelRenderer()
        self.render_interactor = QVTKRenderWindowInteractor(self)

        self.render_interactor.GetRenderWindow().AddRenderer(self.model_renderer)
        self.render_interactor.Initialize()
        self.render_interactor.SetInteractorStyle(vtkInteractorStyleArcballCamera())

        layout = QVBoxLayout()
        layout.addWidget(self.render_interactor)
        self.setLayout(layout)

        self.create_axes()

    def set_theme(self, theme):
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
