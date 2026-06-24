from PySide6.QtCore import QObject, Signal

from vibra.engine.project import Project


class SelectionHandler(QObject):
    selection_changed = Signal()

    def __init__(self, project: Project):
        super().__init__()
        self.project = project
        self.mesh_nodes = set()
        self.mesh_faces = set()
        self.mesh_solids = set()
        self.geometry_points = set()
        self.geometry_lines = set()
        self.geometry_surfaces = set()
        self.geometry_volumes = set()
        self.volume_selection_mode = False

    @property
    def surface_of_selected_volumes(self):
        mesh = self.project.mesh
        if mesh is None:
            return set()

        surfaces = set()
        for volume in self.geometry_volumes:
            surfaces |= set(mesh.surfaces_from_volume.get(volume, []))

        return surfaces

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

    def invert_selection(self):
        mesh = self.project.model.mesh

        geometry_selection_active = any(
            [
                self.geometry_points,
                self.geometry_lines,
                self.geometry_surfaces,
                self.geometry_volumes,
            ]
        )
        mesh_selection_active = any(
            [
                self.mesh_nodes,
                self.mesh_faces,
                self.mesh_solids,
            ]
        )

        if not geometry_selection_active and not mesh_selection_active:
            return

        if geometry_selection_active:
            new_geometry_selection = {}
            if self.geometry_points:
                new_geometry_selection["points"] = mesh.all_point_ids() - self.geometry_points
            if self.geometry_lines:
                new_geometry_selection["lines"] = mesh.all_line_ids() - self.geometry_lines
            if self.geometry_surfaces:
                new_geometry_selection["surfaces"] = mesh.all_surface_ids() - self.geometry_surfaces
            if self.geometry_volumes:
                new_geometry_selection["volumes"] = mesh.all_solid_ids() - self.geometry_volumes
            if new_geometry_selection:
                self.set_geometry_selection(**new_geometry_selection)

        elif mesh_selection_active:
            new_mesh_selection = {}
            if self.mesh_nodes:
                new_mesh_selection["nodes"] = mesh.all_node_ids() - self.mesh_nodes
            if self.mesh_faces:
                new_mesh_selection["faces"] = mesh.all_face_element_ids() - self.mesh_faces
            if self.mesh_solids:
                new_mesh_selection["solids"] = mesh.all_solid_element_ids() - self.mesh_solids
            if new_mesh_selection:
                self.set_mesh_selection(**new_mesh_selection)
