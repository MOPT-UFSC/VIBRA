from PySide6.QtCore import Signal

class SelectionHandler:
    selection_changed = Signal()
    
    def __init__(self):
        self.mesh_nodes = set()
        self.mesh_faces = set()
        self.mesh_solids = set()
        self.geometry_points = set()
        self.geometry_lines = set()
        self.geometry_surfaces = set()
        self.geometry_volumes = set()
        self.volume_selection_mode = False

    def clear_selection(self):
        pass

    def set_geometry_selection(self):
        pass

    def set_mesh_selection(self):
        pass

    def action_hide_selection_callback(self):
        pass

