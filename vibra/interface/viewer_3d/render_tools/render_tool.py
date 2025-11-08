from molde.interactor_styles.arcball_camera_style import ArcballCameraInteractorStyle


class RenderTool(ArcballCameraInteractorStyle):

    def __init__(self):
        super().__init__()

    def start_rotating(self):
        if self.is_panning or self.is_zooming:
            return
        
        super().start_rotating()

    def stop_rotating(self):
        self.stop_all_actions()

    def start_panning(self):
        if self.is_rotating or self.is_zooming:
            return

        super().start_panning()
    
    def stop_panning(self):
        self.stop_all_actions()
    
    def start_zooming(self):
        if self.is_rotating or self.is_panning:
            return

        super().start_zooming()
    
    def stop_zooming(self):
        self.stop_all_actions()
    
    def left_button_release_event(self, obj, event):
        self.stop_all_actions()
    
    def stop_all_actions(self):
        super().stop_zooming()
        super().stop_panning()
        super().stop_rotating()