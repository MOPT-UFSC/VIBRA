from typing import Sequence

from PySide6.QtCore import QObject, Signal

from vibra.engine.project import Project


class EntityVisibilityHandler(QObject):
    changed = Signal()

    def __init__(self, project: Project):
        super().__init__()

        self.project = project

        self._surfaces_to_hide = set()
        self._volumes_to_hide = set()

    def get_visible_surfaces(self) -> set[int]:
        mesh = self.project.mesh
        if mesh is None:
            return set()

        _visible_surfaces = set()
        for volume, surfaces in mesh.surfaces_from_volume.items():
            if volume not in self._volumes_to_hide:
                _visible_surfaces |= set(surfaces)

        _visible_surfaces -= self._surfaces_to_hide
        return _visible_surfaces

    def get_hidden_surfaces(self) -> set[int]:
        mesh = self.project.mesh
        if mesh is None:
            return set()

        all_surfaces = mesh.all_surface_ids()
        return all_surfaces - self.get_visible_surfaces()

    def get_hidden_volumes(self) -> set[int]:
        return set(self._volumes_to_hide)

    def get_visible_volumes(self) -> set[int]:
        mesh = self.project.mesh
        if mesh is None:
            return set()

        all_volumes = mesh.all_solid_ids()
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
