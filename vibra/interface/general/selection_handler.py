from PySide6.QtCore import Signal
from vibra import app

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

        self.hidden_surfaces = set()
        self.hidden_volumes = set()

    def clear_selection(self):
        pass

    def set_geometry_selection(self, *, points=None, lines=None, surfaces=None, volumes=None, join=False, remove=False):
        if points is None:
            points = set()

        if lines is None:
            lines = set()

        if surfaces is None:
            surfaces = set()

        if volumes is None:
            volumes = set()

        surfaces = set(surfaces) - set(self.hidden_surfaces)
        volumes = set(volumes) - set(self.hidden_volumes)
        mesh = app().project.model.mesh

        # Select the surfaces associated to the selected volumes
        for volume in volumes:
            volume_surfaces = mesh.surfaces_from_volume.get(volume, [])
            surfaces |= set(volume_surfaces)

        if join and remove:
            self.geometry_points ^= set(points)
            self.geometry_lines ^= set(lines)
            self.geometry_surfaces ^= set(surfaces)
            self.geometry_volumes ^= set(volumes)
        elif join:
            self.geometry_points |= set(points)
            self.geometry_lines |= set(lines)
            self.geometry_surfaces |= set(surfaces)
            self.geometry_volumes |= set(volumes)
        elif remove:
            self.geometry_points -= set(points)
            self.geometry_lines -= set(lines)
            self.geometry_surfaces -= set(surfaces)
            self.geometry_volumes -= set(volumes)
        else:
            self.geometry_points = set(points)
            self.geometry_lines = set(lines)
            self.geometry_surfaces = set(surfaces)
            self.geometry_volumes = set(volumes)

        self.selection_changed.emit()

    def set_mesh_selection(self, *, nodes=None, faces=None, solids=None, join=False, remove=False):
        if nodes is None:
            nodes = set()

        if faces is None:
            faces = set()

        if solids is None:
            solids = set()

        if join and remove:
            self.mesh_nodes ^= set(nodes)
            self.mesh_faces ^= set(faces)
            self.mesh_solids ^= set(solids)
        elif join:
            self.mesh_nodes |= set(nodes)
            self.mesh_faces |= set(faces)
            self.mesh_solids |= set(solids)
        elif remove:
            self.mesh_nodes -= set(nodes)
            self.mesh_faces -= set(faces)
            self.mesh_solids -= set(solids)
        else:
            self.mesh_nodes = set(nodes)
            self.mesh_faces = set(faces)
            self.mesh_solids = set(solids)

            # Clear the other type of selection
            self.geometry_points.clear()
            self.geometry_lines.clear()
            self.geometry_surfaces.clear()
            self.geometry_volumes.clear()

        self.selection_changed.emit()

    def action_hide_selection_callback(self):
        pass

