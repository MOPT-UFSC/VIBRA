from vibra.interface.viewer_3d.render_tools.render_tool import RenderTool

from vibra import ICON_DIR

class RotationTool(RenderTool):

    def __init__(self):
        super().__init__()
        self.update_mouse_cursor_in_render_widgets(ICON_DIR/"cursors/rotation_cursor.png")

    def left_button_press_event(self, obj, event):
        super().start_rotating()
    
    def left_button_release_event(self, obj, event):
        super().stop_rotating()
