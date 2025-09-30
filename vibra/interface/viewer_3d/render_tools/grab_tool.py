from vibra.interface.viewer_3d.render_tools.render_tool import RenderTool


class GrabTool(RenderTool):

    def __init__(self):
        super().__init__()
    
    def left_button_press_event(self, obj, event):
        self.is_panning = True

        x, y, *_ = self.GetInteractor().GetEventPosition()
        self.FindPokedRenderer(x, y)

    def mouse_move_event(self, obj, event):
        if self.is_panning:
            self.Pan()
            self.OnMouseMove()
        else:
            super().mouse_move_event(obj, event)
    
    def left_button_release_event(self, obj, event):
        self.is_panning = False