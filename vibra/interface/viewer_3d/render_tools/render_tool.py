from PySide6.QtCore import QObject, Signal
from vibra.interface.viewer_3d.render_tools.arcball_camera_style import ArcballCameraInteractorStyle


class RenderTool(ArcballCameraInteractorStyle):

    def __init__(self):
        super().__init__()
