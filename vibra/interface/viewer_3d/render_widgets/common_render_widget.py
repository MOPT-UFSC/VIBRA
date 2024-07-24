import logging
from threading import Lock
from time import time

from PIL import Image
from PyQt5.QtWidgets import QFrame, QStackedLayout
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.util.numpy_support import vtk_to_numpy
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkInteractionWidgets import vtkOrientationMarkerWidget
from vtkmodules.vtkIOImage import vtkPNGWriter
from vtkmodules.vtkRenderingAnnotation import (
    vtkAxesActor,
    vtkLegendScaleActor,
    vtkScalarBarActor,
)
from vtkmodules.vtkRenderingCore import (
    vtkRenderer,
    vtkTextProperty,
    vtkWindowToImageFilter,
)

from vibra.interface.viewer_3d.interactor_styles.arcball_camera import (
    vtkInteractorStyleArcballCamera,
)
from vibra.utils.interface_functions import get_main_window


class CommonRenderWidget(QFrame):
    """
    This class is needed show vtk renderers in pyqt.

    A vtk widget must always have a renderer, even if it is empty.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.renderer = vtkRenderer()
        self.style = vtkInteractorStyleArcballCamera()
        self.render_interactor = QVTKRenderWindowInteractor(self)

        self.render_interactor.Initialize()
        self.render_interactor.GetRenderWindow().AddRenderer(self.renderer)
        self.render_interactor.SetInteractorStyle(self.style)
        self.renderer.ResetCamera()

        self.playing_animation = False
        self._animation_lock = Lock()
        self._animation_frame = 0
        self._animation_last_time = 0
        self._animation_total_frames = 30
        self._animation_fps = 30
        self._animation_timer = self.render_interactor.CreateRepeatingTimer(500)
        self.render_interactor.AddObserver("TimerEvent", self._animation_callback)

        layout = QStackedLayout()
        layout.addWidget(self.render_interactor)
        self.setLayout(layout)

    def update_plot(self, reset_camera=True):
        raise NotImplementedError("The function update_plot was not implemented")

    def update(self):
        ren_win = self.render_interactor.GetRenderWindow()
        if ren_win is not None:
            ren_win.Render()

    def update_theme(self):
        try:
            main_window = get_main_window()
        except RuntimeError as e:
            logging.warn(e)
        else:
            self.set_theme(main_window.user_config.theme)

    def get_thumbnail(self):
        image_filter = vtkWindowToImageFilter()
        image_filter.SetInput(self.render_interactor.GetRenderWindow())
        image_filter.Update()

        vtk_image = image_filter.GetOutput()
        width, height, _ = vtk_image.GetDimensions()
        vtk_array = vtk_image.GetPointData().GetScalars()
        components = vtk_array.GetNumberOfComponents()

        array = vtk_to_numpy(vtk_array).reshape(height, width, components)
        image = Image.fromarray(array).transpose(Image.FLIP_TOP_BOTTOM)

        size = min(image.width, image.height)
        box = (
            (image.width - size) // 2,
            (image.height - size) // 2,
            (image.width + size) // 2,
            (image.height + size) // 2,
        )
        image = image.crop(box=box).resize(size=(512, 512))
        return image

    def save_png(self, path):
        imageFilter = vtkWindowToImageFilter()
        imageFilter.SetInput(self.render_interactor.GetRenderWindow())
        writer = vtkPNGWriter()
        writer.SetFileName(path)
        writer.SetInputConnection(imageFilter.GetOutputPort())
        writer.Write()

    def create_axes(self):
        axes_actor = vtkAxesActor()

        x_property = axes_actor.GetXAxisCaptionActor2D().GetCaptionTextProperty()
        y_property = axes_actor.GetYAxisCaptionActor2D().GetCaptionTextProperty()
        z_property = axes_actor.GetZAxisCaptionActor2D().GetCaptionTextProperty()

        for i in [x_property, y_property, z_property]:
            i.ItalicOff()
            i.BoldOff()

        self.axes = vtkOrientationMarkerWidget()
        self.axes.SetOrientationMarker(axes_actor)
        self.axes.SetInteractor(self.render_interactor)
        self.axes.EnabledOn()
        self.axes.InteractiveOff()

    def create_scale_bar(self):
        self.scale_bar = vtkLegendScaleActor()
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

    def create_color_bar(self, lookup_table=None):
        if lookup_table is None:
            lookup_table = vtkLookupTable()
            lookup_table.Build()

        colorbar_label = vtkTextProperty()
        colorbar_label.ShadowOff()
        colorbar_label.ItalicOff()
        colorbar_label.BoldOn()
        colorbar_label.SetFontSize(12)
        colorbar_label.SetJustificationToLeft()

        self.colorbar = vtkScalarBarActor()
        self.colorbar.SetLabelTextProperty(colorbar_label)
        self.colorbar_actor.SetLookupTable(lookup_table)
        self.colorbar.SetWidth(0.02)
        self.colorbar.SetPosition(0.94, 0.07)
        self.colorbar.SetMaximumNumberOfColors(400)
        self.colorbar.UnconstrainedFontSizeOn()
        self.colorbar.SetTextPositionToPrecedeScalarBar()
        self.renderer.AddActor(self.colorbar)

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
        self.update()

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

    #
    def start_animation(self):
        if self.playing_animation:
            return

        self.playing_animation = True

    def stop_animation(self):
        if not self.playing_animation:
            return

        if self._animation_timer is None:
            return

        self.playing_animation = False

    def _animation_callback(self, obj, event):
        """
        Common function with controls that are meaningfull to
        all kinds of animations.
        """

        if not self.playing_animation:
            return

        # If the time to update the frame takes
        # longer than expected
        if self._animation_lock.locked():
            return

        # Only needed because vtk CreateRepeatingTimer(n)
        # does not work =/
        dt = time() - self._animation_last_time
        if (dt) < 1 / self._animation_fps:
            return

        with self._animation_lock:
            self._animation_frame = (self._animation_frame + 1) % self._animation_total_frames
            self.update_animation(self._animation_frame)
            self._animation_last_time = time()

    def update_animation(self, frame):
        raise NotImplementedError('The function "update_animation" was not implemented!')

    def process_animation_frames(self):
        raise NotImplementedError('The function "process_animation_frames" was not implemented!')
