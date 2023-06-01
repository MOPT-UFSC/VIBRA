import vtk
from PyQt5.QtCore import QCoreApplication, pyqtSignal
from PyQt5.QtWidgets import QFrame, QStackedLayout
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from vibra.interface.viewer_3d.arcball_camera import (
    vtkInteractorStyleArcballCamera,
)
from vibra.interface.viewer_3d.example_renderer import ExampleRenderer
from vibra.interface.viewer_3d.model_renderer import ModelRenderer
from vibra.interface.viewer_3d.selection_interactor import SelectionInteractor


class VTKWidget(QFrame):
    '''
    This class is needed show vtk renderers in pyqt.

    A vtk widget must always have a renderer, even if it is empty.
    '''

    def __init__(self, parent=None):
        super().__init__(parent)

        self.renderer = vtk.vtkRenderer()
        self.style = SelectionInteractor()

        self.render_interactor = QVTKRenderWindowInteractor(self)
        self.render_interactor.Initialize()
        self.render_interactor.SetInteractorStyle(self.style)

        layout = QStackedLayout()
        layout.addWidget(self.render_interactor)
        self.setLayout(layout)

        self.style.AddObserver("SelectionEvent", self.selection_callback)
        self.create_axes()

    def set_renderer(self, renderer):
        if renderer == self.renderer:
            return

        self.render_interactor.GetRenderWindow().RemoveRenderer(self.renderer)
        self.render_interactor.GetRenderWindow().AddRenderer(renderer)
        renderer.ResetCamera()
        self.renderer = renderer

    def update_plot(self):
        if self.renderer is None:
            return
        self.renderer.update_actors()

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
        if self.renderer is None:
            return

        try:
            self.renderer.selection_callback(obj, event)
        except AttributeError:
            pass  # if renderer don't have this method just ignore

    def set_theme(self, theme):
        if self.renderer is None:
            return
    
        try:
            self.renderer.set_theme(theme)
        except AttributeError:
            pass  # if renderer don't have this method just ignore

    # 
    def show_points(self):
        try:
            self.renderer.show_points()
        except AttributeError:
            pass  # if renderer don't have this method just ignore

    def show_lines(self):
        try:
            self.renderer.show_lines()
        except AttributeError:
            pass  # if renderer don't have this method just ignore

    def show_faces(self):
        try:
            self.renderer.show_faces()
        except AttributeError:
            pass  # if renderer don't have this method just ignore

    # 
    def set_custom_view(self, position, view_up):
        self.renderer.GetActiveCamera().SetPosition(position)
        self.renderer.GetActiveCamera().SetViewUp(view_up)
        self.renderer.GetActiveCamera().SetParallelProjection(True)
        self.renderer.ResetCamera(*self.renderer.ComputeVisiblePropBounds())

        if self.renderer.GetRenderWindow() is not None:
            self.renderer.GetRenderWindow().Render()

    def set_view_up(self):        
        x, y, z = self.renderer.GetActiveCamera().GetFocalPoint()
        position = (x, y + 1, z)
        view_up = (0, 0, -1)
        self.set_custom_view(position, view_up)

    def set_view_down(self):
        x, y, z = self.renderer.GetActiveCamera().GetFocalPoint()
        position = (x, y - 1, z)
        view_up = (0, 0, 1)
        self.set_custom_view(position, view_up)

    def set_view_left(self):
        x, y, z = self.renderer.GetActiveCamera().GetFocalPoint()
        position = (x - 1, y, z)
        view_up = (0, 1, 0)
        self.set_custom_view(position, view_up)

    def set_view_right(self):        
        x, y, z = self.renderer.GetActiveCamera().GetFocalPoint()
        position = (x + 1, y, z)
        view_up = (0, 1, 0)
        self.set_custom_view(position, view_up)

    def set_view_front(self):
        x, y, z = self.renderer.GetActiveCamera().GetFocalPoint()
        position = (x, y, z + 1)
        view_up = (0, 1, 0)
        self.set_custom_view(position, view_up)

    def set_view_back(self):
        x, y, z = self.renderer.GetActiveCamera().GetFocalPoint()
        position = (x, y, z - 1)
        view_up = (0, 1, 0)
        self.set_custom_view(position, view_up)

    def set_view_orthogonal(self):
        x, y, z = self.renderer.GetActiveCamera().GetFocalPoint()
        position = (x + 1, y + 1, z + 1)
        view_up = (0, 1, 0)
        self.set_custom_view(position, view_up)
