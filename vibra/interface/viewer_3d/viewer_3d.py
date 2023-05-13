import vtk
from PyQt5.QtWidgets import QFrame, QVBoxLayout
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from vibra.interface.viewer_3d.arcball_camera import (
    vtkInteractorStyleArcballCamera,
)
from vibra.interface.viewer_3d.model_renderer import ModelRenderer


class Viewer3D(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.model_renderer = ModelRenderer()
        self.render_interactor = QVTKRenderWindowInteractor(self)

        self.render_interactor.GetRenderWindow().AddRenderer(self.model_renderer)
        self.render_interactor.Initialize()
        self.render_interactor.SetInteractorStyle(vtkInteractorStyleArcballCamera())

        layout = QVBoxLayout()
        layout.addWidget(self.render_interactor)
        self.setLayout(layout)

        self.model_renderer.create_axes()
        self.model_renderer.create_scale_bar()

    def set_theme(self, theme):
        self.model_renderer.set_theme(theme)

    def save_png(self, path):
        imageFilter = vtk.vtkWindowToImageFilter()
        imageFilter.SetInput(self.render_interactor.GetRenderWindow())
        writer = vtk.vtkPNGWriter()
        writer.SetFileName(path)
        writer.SetInputConnection(imageFilter.GetOutputPort())
        writer.Write()
