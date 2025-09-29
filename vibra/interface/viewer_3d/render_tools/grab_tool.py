from render_tool import RenderTool


class GrabTool(RenderTool):

    def __init__(self):
        self._create_connections()

    def _create_connections(self):
        self.click_event.connect(self.define_render_where_click_occurred)
        self.position_changed.connect(self.pan_the_camera)

    
    def define_render_where_click_occurred(self, x: int, y: int):
        self.FindPokedRenderer(x, y)

    def pan_the_camera(self):
        ...