from .faces_actor import FacesActor


class GhostActor(FacesActor):
    def __init__(self, mesh):
        super().__init__(mesh, allow_hidding=False)
    
    def configure_appearance(self):
        self.GetProperty().SetOpacity(0.05)
        self.GetProperty().LightingOff()
        self.PickableOff()
        self.clear_colors()
