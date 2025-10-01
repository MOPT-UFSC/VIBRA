import numpy as np
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingCore import vtkPropPicker

from molde.actors import RoundPointsActor


class ArcballCameraInteractorStyle(vtkInteractorStyleTrackballCamera):
    """
    Interactor style that rotates and zooms around the cursor.
    """

    def __init__(self):

        self.center_of_rotation = None
        self.default_center_of_rotation = None

        self.is_rotating = False
        self.is_panning = False
        self.is_zooming = False

        self.mid_button_click_position = (0, 0)
        # cor = center of rotation
        self.cor_actor = self._make_default_cor_actor()
        self._create_observers()

    def set_default_center_of_rotation(self, center):
        self.default_center_of_rotation = center

    def set_cor_actor(self, actor):
        self.cor_actor = actor

    def _create_observers(self):
        self.AddObserver("LeftButtonPressEvent", self.left_button_press_event)
        self.AddObserver("LeftButtonReleaseEvent", self.left_button_release_event)
        self.AddObserver("RightButtonPressEvent", self.right_button_press_event)
        self.AddObserver("RightButtonReleaseEvent", self.right_button_release_event)
        self.AddObserver("MouseMoveEvent", self.mouse_move_event)
        self.AddObserver("MouseWheelForwardEvent", self.mouse_wheel_forward_event)
        self.AddObserver("MouseWheelBackwardEvent", self.mouse_wheel_backward_event)
        self.AddObserver("MiddleButtonPressEvent", self.click_mid_button_press_event)
        self.AddObserver("MiddleButtonReleaseEvent", self.click_mid_button_release_event)

    def left_button_press_event(self, obj, event):
       pass

    def left_button_release_event(self, obj, event):
        pass

    def right_button_press_event(self, obj, event):
        self.start_rotating()

    def right_button_release_event(self, obj, event):
        self.stop_rotating()

    def click_mid_button_press_event(self, obj, event):
        zoom = self.GetInteractor().GetControlKey()

        if zoom:
            self.start_zooming()
        else:
            self.start_panning()

    def click_mid_button_release_event(self, obj, event):
        self.stop_panning()
        self.stop_zooming()

    def mouse_move_event(self, obj, event):
        if self.is_zooming:
            self.update_zoom()

        elif self.is_rotating:
            self.update_rotation()

        elif self.is_panning:
            self.update_panning()

        self.OnMouseMove()

    def mouse_wheel_forward_event(self, obj, event):
        self.zoom_in()

    def mouse_wheel_backward_event(self, obj, event):
        self.zoom_out()
    
    def start_panning(self):
        self.is_panning = True
        cursor = self.GetInteractor().GetEventPosition()
        self.mid_button_click_position = cursor
        self.FindPokedRenderer(cursor[0], cursor[1])
    
    def update_panning(self):
        self.Pan()
    
    def stop_panning(self):
        self.is_panning = False
    
    def start_zooming(self):
        self.is_zooming = True
        cursor = self.GetInteractor().GetEventPosition()
        self.mid_button_click_position = cursor
        self.FindPokedRenderer(cursor[0], cursor[1])
    
    def stop_zooming(self):
        self.is_zooming = False
     
    def zoom_out(self):
        int_pos = self.GetInteractor().GetEventPosition()

        self.FindPokedRenderer(int_pos[0], int_pos[1])

        if self.GetCurrentRenderer() is None:
            return

        motion_factor = 10
        mouse_motion_factor = 1

        factor = motion_factor * -0.2 * mouse_motion_factor

        self.dolly(1.1**factor)

        self.ReleaseFocus()
    
    def update_zoom(self):
    # Implementation based on this link
        # https://github.com/Kitware/VTK/blob/4c4cd48244eaf1a74e0b096aae773c5498f7a782/Interaction/Style/vtkInteractorStyleTrackballCamera.cxx#L352
        y0 = self.GetInteractor().GetLastEventPosition()[1]
        y1 = self.GetInteractor().GetEventPosition()[1]

        dyf = 10 * (y1 - y0) / self.GetCurrentRenderer().GetCenter()[1]
        factor = 1.1 ** dyf
        self.dolly_on_point(factor, *self.mid_button_click_position)
    
    def zoom_in(self):
        int_pos = self.GetInteractor().GetEventPosition()

        self.FindPokedRenderer(int_pos[0], int_pos[1])

        if self.GetCurrentRenderer() is None:
            return

        motion_factor = 10
        mouse_motion_factor = 1

        factor = motion_factor * 0.2 * mouse_motion_factor

        self.dolly(1.1**factor)

        self.ReleaseFocus()
    
    def start_rotating(self):
        self.is_rotating = True

        cursor = self.GetInteractor().GetEventPosition()
        self.FindPokedRenderer(cursor[0], cursor[1])

        renderer = self.GetCurrentRenderer() or self.GetDefaultRenderer()
        camera = renderer.GetActiveCamera()

        if renderer is None:
            return

        picker = vtkPropPicker()
        picker.Pick(cursor[0], cursor[1], 0, renderer)
        pos = picker.GetPickPosition()

        if pos != (0, 0, 0):
            self.center_of_rotation = pos

        elif self.default_center_of_rotation is not None:
            self.center_of_rotation = self.default_center_of_rotation

        else:
            x0, x1, y0, y1, z0, z1 = renderer.ComputeVisiblePropBounds()
            self.center_of_rotation = [(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2]

        dx, dy, dz = np.array(camera.GetPosition()) - np.array(camera.GetFocalPoint())
        distance_factor = np.sqrt(dx**2 + dy**2 + dz**2)

        self.cor_actor.SetPosition(self.center_of_rotation)
        self.cor_actor.SetScale((distance_factor / 3.5, distance_factor / 3.5, distance_factor / 3.5))
        renderer.AddActor(self.cor_actor)

    def update_rotation(self):
        renderer = self.GetDefaultRenderer() or self.GetCurrentRenderer()
        if renderer is None:
            return

        rwi = self.GetInteractor()
        delta_mouse = np.array(rwi.GetEventPosition()) - np.array(rwi.GetLastEventPosition())
        size = np.array(renderer.GetRenderWindow().GetSize())
        motion_factor = 10
        elevation_azimuth = -20 / size
        rotation_factor = delta_mouse * motion_factor * elevation_azimuth

        camera = renderer.GetActiveCamera()

        self.rotate_around_center(rotation_factor[0], rotation_factor[1])

        camera.OrthogonalizeViewUp()

        renderer.ResetCameraClippingRange()

        if rwi.GetLightFollowCamera():
            renderer.UpdateLightsGeometryToFollowCamera()

        rwi.Render()

    def rotate_around_center(self, anglex, angley):
        renderer = self.GetDefaultRenderer() or self.GetCurrentRenderer()
        camera = renderer.GetActiveCamera()

        transform_camera = vtkTransform()
        transform_camera.Identity()

        axis = [
            -camera.GetViewTransformObject().GetMatrix().GetElement(0, 0),
            -camera.GetViewTransformObject().GetMatrix().GetElement(0, 1),
            -camera.GetViewTransformObject().GetMatrix().GetElement(0, 2),
        ]

        saved_view_up = camera.GetViewUp()
        transform_camera.RotateWXYZ(angley, axis)
        new_view_up = transform_camera.TransformPoint(camera.GetViewUp())
        camera.SetViewUp(new_view_up)
        transform_camera.Identity()

        cor = self.center_of_rotation

        transform_camera.Translate(+cor[0], +cor[1], +cor[2])
        transform_camera.RotateWXYZ(anglex, camera.GetViewUp())
        transform_camera.RotateWXYZ(angley, axis)
        transform_camera.Translate(-cor[0], -cor[1], -cor[2])

        new_camera_position = transform_camera.TransformPoint(camera.GetPosition())
        camera.SetPosition(new_camera_position)

        new_focal_point = transform_camera.TransformPoint(camera.GetFocalPoint())
        camera.SetFocalPoint(new_focal_point)

        camera.SetViewUp(saved_view_up)

        camera.Modified()
    
    def stop_rotating(self):
        self.is_rotating = False
        renderer = self.GetDefaultRenderer() or self.GetCurrentRenderer()
        renderer.RemoveActor(self.cor_actor)
        self.GetInteractor().Render()
        self.EndDolly()

    def dolly(self, factor):
        cursor = self.GetInteractor().GetEventPosition()
        self.dolly_on_point(factor, *cursor)

    def dolly_on_point(self, factor, x, y):
        renderer = self.GetDefaultRenderer() or self.GetCurrentRenderer()
        camera = renderer.GetActiveCamera()

        view_center = np.array(renderer.GetSize()) / 2
        distance_to_center = (x, y) - view_center
        dx, dy = distance_to_center * (1 - 1 / factor)
        self.move_viewport(dx, dy)

        if camera.GetParallelProjection():
            camera.SetParallelScale(camera.GetParallelScale() / factor)
        else:
            camera.Dolly(factor)
            if self.GetAutoAdjustCameraClippingRange():
                renderer.ResetCameraClippingRange()

        if self.GetInteractor().GetLightFollowCamera():
            renderer.UpdateLightsGeometryToFollowCamera()

        self.GetInteractor().Render()

    def move_viewport(self, dx, dy):
        """
        Moves the viewport in view coordinates by some amount of pixels.

        Further explanations on this link:
        https://github.com/open-pulse/OpenPulse/blob/5f7bd4719527383b2d3ea078e5f29f214f35128d/doc/code_explanation/move_viewport.pdf
        """

        renderer = self.GetDefaultRenderer() or self.GetCurrentRenderer()
        camera = renderer.GetActiveCamera()
        width, heigth = renderer.GetSize()

        if camera.GetParallelProjection():
            view_height = 2 * camera.GetParallelScale()
        else:
            correction = camera.GetDistance()
            view_height = 2 * correction * np.tan(0.5 * camera.GetViewAngle() / 57.296)
        scale = view_height / heigth

        focal_point = np.array(camera.GetFocalPoint())
        camera_position = np.array(camera.GetPosition())
        camera_up = np.array(camera.GetViewUp())
        camera_in = np.array(camera.GetDirectionOfProjection())
        camera_right = np.cross(camera_in, camera_up)

        camera_displacement = scale * (camera_right * dx + camera_up * dy)
        camera.SetPosition(camera_position + camera_displacement)
        camera.SetFocalPoint(focal_point + camera_displacement)

    def _make_default_cor_actor(self):
        actor = RoundPointsActor([(0, 0, 0)])
        actor.appear_in_front(True)
        actor.GetProperty().SetColor(1, 0, 0)
        actor.GetProperty().SetPointSize(10)
        return actor
