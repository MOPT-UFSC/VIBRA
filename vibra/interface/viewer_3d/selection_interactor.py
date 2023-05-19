from vibra.interface.viewer_3d.arcball_camera import (
    vtkInteractorStyleArcballCamera,
)
import vtk


class SelectionInteractor(vtkInteractorStyleArcballCamera):
    def __init__(self):
        super().__init__()
        self.selection_picker = vtk.vtkCellPicker()
        self.hover_picker = vtk.vtkCellPicker()
        self.selection_picker.SetTolerance(0.002)

    def left_button_press_event(self, obj, event):
        cursor = self.GetInteractor().GetEventPosition()
        self.FindPokedRenderer(cursor[0], cursor[1])

        renderer = self.GetCurrentRenderer() or self.GetDefaultRenderer()
        if renderer is None:
            return

        self.selection_picker.Pick(cursor[0], cursor[1], 0, renderer)
        self.InvokeEvent("SelectionEvent")