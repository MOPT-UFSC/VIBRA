import gmsh

class GeometryEditor:
    def __init__(self):
        gmsh.initialize()
        self.occ = gmsh.model.occ
        pass
    
    def add_callback(self):
        pass

    def add_box(self, start: tuple, deltas: tuple):
        self.occ.addBox(*start, *deltas)

