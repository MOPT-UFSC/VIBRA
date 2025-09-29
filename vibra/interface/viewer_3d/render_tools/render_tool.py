from PySide6.QtCore import Signal
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera


class RenderTool(vtkInteractorStyleTrackballCamera):

    click_event = Signal(int, int)
    release_event = Signal(int, int)
    position_changed = Signal(int, int)

    def __init__(self):
        self._create_observers()
    
    def _create_observers(self):
        self.AddObserver("LeftButtonPressEvent", self.click_event_callback)
        self.AddObserver("LeftButtonReleaseEvent", self.release_event_callback)
        self.AddObserver("MouseMoveEvent", self.move_event_callback)
    
    def click_event_callback(self):
        x, y, *_ = self.GetEventPosition()
        self.click_event.emit(x, y)
    
    def release_event_callback(self):
        x, y, *_ = self.GetEventPosition()
        self.release_event.emit(x, y)
    
    def move_event_callback(self):
        x, y, *_ = self.GetEventPosition()
        self.position_changed.emit(x, y)
    
    
