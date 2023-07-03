import vtk
from PyQt5.QtWidgets import QFrame, QStackedLayout
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from vibra.interface.viewer_3d.interactor_styles.arcball_camera import (
    vtkInteractorStyleArcballCamera,
)


class CommonRenderWidget(QFrame):
    """
    This class is needed show vtk renderers in pyqt.

    A vtk widget must always have a renderer, even if it is empty.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.renderer = vtk.vtkRenderer()
        self.style = vtkInteractorStyleArcballCamera()
        self.render_interactor = QVTKRenderWindowInteractor(self)

        self.render_interactor.Initialize()
        self.render_interactor.GetRenderWindow().AddRenderer(self.renderer)
        self.render_interactor.SetInteractorStyle(self.style)
        self.renderer.ResetCamera()

        layout = QStackedLayout()
        layout.addWidget(self.render_interactor)
        self.setLayout(layout)

    def update_plot(self):
        pass

    def update(self):
        ren_win = self.render_interactor.GetRenderWindow()
        if ren_win is not None:
            ren_win.Render()

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

    def create_scale_bar(self):
        self.scale_bar = vtk.vtkLegendScaleActor()
        self.scale_bar.AllAxesOff()

        title_property = self.scale_bar.GetLegendTitleProperty()
        title_property.SetFontSize(14)
        title_property.ShadowOff()
        title_property.ItalicOff()
        title_property.SetLineOffset(-35)
        title_property.SetVerticalJustificationToTop()

        label_property = self.scale_bar.GetLegendLabelProperty()
        label_property.SetFontSize(12)
        label_property.ShadowOff()
        label_property.ItalicOff()
        label_property.BoldOff()
        label_property.SetLineOffset(-25)

        self.renderer.AddActor(self.scale_bar)

    #
    def set_theme(self, theme):
        if theme == "dark":
            self.renderer.GradientBackgroundOn()
            self.renderer.SetBackground(0.06, 0.08, 0.12)
            self.renderer.SetBackground2(0, 0, 0)
        elif theme == "light":
            self.renderer.GradientBackgroundOn()
            self.renderer.SetBackground(0.5, 0.5, 0.65)
            self.renderer.SetBackground2(1, 1, 1)
        else:
            NotImplemented

    def show_points(self):
        pass

    def show_lines(self):
        pass

    def show_faces(self):
        pass

    #
    def set_custom_view(self, position, view_up):
        self.renderer.GetActiveCamera().SetPosition(position)
        self.renderer.GetActiveCamera().SetViewUp(view_up)
        self.renderer.GetActiveCamera().SetParallelProjection(True)
        self.renderer.ResetCamera(*self.renderer.ComputeVisiblePropBounds())

        if self.renderer.GetRenderWindow() is not None:
            self.renderer.GetRenderWindow().Render()

    def set_top_view(self):
        x, y, z = self.renderer.GetActiveCamera().GetFocalPoint()
        position = (x, y + 1, z)
        view_up = (0, 0, -1)
        self.set_custom_view(position, view_up)

    def set_bottom_view(self):
        x, y, z = self.renderer.GetActiveCamera().GetFocalPoint()
        position = (x, y - 1, z)
        view_up = (0, 0, 1)
        self.set_custom_view(position, view_up)

    def set_left_view(self):
        x, y, z = self.renderer.GetActiveCamera().GetFocalPoint()
        position = (x - 1, y, z)
        view_up = (0, 1, 0)
        self.set_custom_view(position, view_up)

    def set_right_view(self):
        x, y, z = self.renderer.GetActiveCamera().GetFocalPoint()
        position = (x + 1, y, z)
        view_up = (0, 1, 0)
        self.set_custom_view(position, view_up)

    def set_front_view(self):
        x, y, z = self.renderer.GetActiveCamera().GetFocalPoint()
        position = (x, y, z + 1)
        view_up = (0, 1, 0)
        self.set_custom_view(position, view_up)

    def set_back_view(self):
        x, y, z = self.renderer.GetActiveCamera().GetFocalPoint()
        position = (x, y, z - 1)
        view_up = (0, 1, 0)
        self.set_custom_view(position, view_up)

    def set_isometric_view(self):
        x, y, z = self.renderer.GetActiveCamera().GetFocalPoint()
        position = (x + 1, y + 1, z + 1)
        view_up = (0, 1, 0)
        self.set_custom_view(position, view_up)
