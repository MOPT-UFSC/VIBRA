from vibra.interface.viewer_3d.render_tools.render_tool import RenderTool


class GrabTool(RenderTool):

    def __init__(self):
        super().__init__()
        self.cursor_path = ":/icons/cursors/pan_cursor.png"
    
    def left_button_press_event(self, obj, event):
        super().start_panning()
    
    def left_button_release_event(self, obj, event):
        super().stop_panning()
