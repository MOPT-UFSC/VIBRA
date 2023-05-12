import vtk
from PyQt5.QtWidgets import QFrame, QVBoxLayout
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from vibra.interface.viewer_3d.model_renderer import ModelRenderer


class Viewer3D(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.model_renderer = ModelRenderer()
        self.render_interactor = QVTKRenderWindowInteractor(self)

        self.render_interactor.GetRenderWindow().AddRenderer(self.model_renderer)
        self.render_interactor.Initialize()
        self.render_interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())

        layout = QVBoxLayout()
        layout.addWidget(self.render_interactor)
        self.setLayout(layout)
