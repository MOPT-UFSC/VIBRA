from PySide6.QtCore import Signal, QObject
from vibra import app

class SelectionHandler(QObject):
    selection_changed = Signal()
    
    def __init__(self):
        super().__init__()
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
        self.set_geometry_selection()
        self.set_mesh_selection()

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

    def calculate_volumes_to_hide(self):
        mesh = app().project.model.mesh
        volumes_to_hide = set()
        if self.geometry_volumes:
            volumes_to_hide |= self.geometry_volumes

        elif self.geometry_surfaces:
            for surface in self.geometry_surfaces:
                volumes_to_hide |= set(mesh.volumes_from_surface[surface])

        elif self.mesh_solids:
            for element in self.mesh_solids:
                volumes_to_hide.add(mesh.get_volume_from_element(element))
        return volumes_to_hide


