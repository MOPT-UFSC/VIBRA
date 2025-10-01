from vibra.interface.viewer_3d.render_tools.render_tool import RenderTool


class ZoomTool(RenderTool):

    def __init__(self):
        super().__init__()
    
    def left_button_press_event(self, obj, event):
        super().start_zooming()
    
    def left_button_release_event(self, obj, event):
        super().stop_zooming()
        