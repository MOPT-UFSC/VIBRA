from collections.abc import Sequence

from PySide6.QtCore import QObject, Signal

from vibra.engine.model import Model


class EntityVisibilityHandler(QObject):
    changed = Signal()

    def __init__(self, model: Model):
        super().__init__()

        self.model = model

        self._surfaces_to_hide = set()
        self._volumes_to_hide = set()

    def set_model(self, model: Model):
        self.model = model

    def get_visible_nodes(self) -> set[int]:
        # This is terribly slow. Use numpy instead.

        mesh = self.model.mesh
        if mesh is None:
            return set()

        visible_nodes = set()
        for volume_id in self.get_visible_volumes():
            nodes = mesh.get_nodes_from_volume(volume_id)
            if nodes is not None:
                visible_nodes |= set(nodes.tolist())

        if mesh.faces_connectivity is not None:
            visible_nodes -= set(mesh.faces_connectivity[:, 4:].ravel().tolist())

        for surface_id in self.get_visible_surfaces():
            nodes = mesh.get_nodes_from_surface(surface_id)
            if nodes is not None:
                visible_nodes |= set(nodes.tolist())

        return visible_nodes

    def get_hidden_nodes(self) -> set[int]:
        mesh = self.model.mesh
        if mesh is None:
            return set()

        all_nodes = mesh.all_node_ids()
        return all_nodes - self.get_visible_nodes()

    def get_visible_surfaces(self) -> set[int]:
        mesh = self.model.mesh
        if mesh is None:
            return set()

        _visible_surfaces = set()
        for volume, surfaces in mesh.surfaces_from_volume.items():
            if volume not in self._volumes_to_hide:
                _visible_surfaces |= set(surfaces)

        _visible_surfaces -= self._surfaces_to_hide
        return _visible_surfaces

    def get_hidden_surfaces(self) -> set[int]:
        mesh = self.model.mesh
        if mesh is None:
            return set()

        all_surfaces = mesh.all_surface_ids()
        return all_surfaces - self.get_visible_surfaces()

    def get_hidden_volumes(self) -> set[int]:
        return set(self._volumes_to_hide)

    def get_visible_volumes(self) -> set[int]:
        mesh = self.model.mesh
        if mesh is None:
            return set()

        all_volumes = mesh.all_volume_ids()
        return all_volumes - self.get_hidden_volumes()

    def hide_surfaces(self, surfaces: Sequence[int]):
        self._surfaces_to_hide |= set(surfaces)
        if surfaces:
            self.changed.emit()

    def hide_volumes(self, volumes: Sequence[int]):
        self._volumes_to_hide |= set(volumes)
        if volumes:
            self.changed.emit()

    def has_hidden_entity(self) -> bool:
        return bool(self._surfaces_to_hide) or bool(self._volumes_to_hide)

    def unhide_all(self):
        # This is only to avoid unnecessary callbacks
        if not any((self._surfaces_to_hide, self._volumes_to_hide)):
            return

        self._surfaces_to_hide.clear()
        self._volumes_to_hide.clear()
        self.changed.emit()
