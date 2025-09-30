from vibra.interface.viewer_3d.render_tools.render_tool import RenderTool


class GrabTool(RenderTool):

    def __init__(self):
        super().__init__()

        self._create_connections()

    def _create_connections(self):
        self.tool_signals.click_event.connect(self.start_panning)
        self.tool_signals.position_changed.connect(self.update_panning)
        self.tool_signals.release_event.connect(self.stop_panning)
    
    def start_panning(self, x: int, y: int):
        self.is_panning = True
        self.FindPokedRenderer(x, y)

    def update_panning(self):
        if self.is_panning:
            self.Pan()
            self.OnMouseMove()
        else:
            super().mouse_move_event(None, None)
    
    def stop_panning(self):
        self.is_panning = False