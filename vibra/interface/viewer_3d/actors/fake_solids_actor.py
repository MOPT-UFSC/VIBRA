from .faces_actor import FacesActor


class FakeSolidsActor(FacesActor):
    def create_geometry(self):
        super().create_geometry()
        # update cell_indexes to point to solid elements
    
    def configure_appearance(self):
        super().configure_appearance()
        self.set_color((255, 255, 0))
    
    def paint_cells(self, color, solids: list[int]):
        faces = []  # convert solids to faces
        return super().paint_cells(color, faces)
