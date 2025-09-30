from PySide6.QtCore import QObject, Signal
from vibra.interface.viewer_3d.render_tools.arcball_camera_style import ArcballCameraInteractorStyle


class ToolSignals(QObject):
    click_event = Signal(int, int)
    release_event = Signal()
    position_changed = Signal()

class RenderTool(ArcballCameraInteractorStyle):

    def __init__(self):
        super().__init__()

        self.tool_signals = ToolSignals()
        self._configure_observers()
    
    def _configure_observers(self):
        events = ["LeftButtonPressEvent", "LeftButtonReleaseEvent", "MouseMoveEvent"]
        for event in events:
            self.RemoveObservers(event)

        self.AddObserver("LeftButtonPressEvent", self.click_event_callback)
        self.AddObserver("LeftButtonReleaseEvent", self.release_event_callback)
        self.AddObserver("MouseMoveEvent", self.move_event_callback)
    
    def click_event_callback(self, obj, event):
        x, y, *_ = self.GetInteractor().GetEventPosition()
        self.tool_signals.click_event.emit(x, y)
    
    def release_event_callback(self, obj, event):
        self.tool_signals.release_event.emit()
    
    def move_event_callback(self, obj, event):
        self.tool_signals.position_changed.emit()
    
    
