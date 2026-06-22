from typing import Sequence

from PySide6.QtCore import QObject, Signal

from vibra.engine.project import Project


class EntityVisibilityHandler(QObject):
    changed = Signal()

    def __init__(self, project: Project):
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
                _visible_surfaces |= surfaces

        _visible_surfaces -= self._surfaces_to_hide
        return _visible_surfaces

    def get_hidden_surfaces(self) -> set[int]:
        mesh = self.project.mesh
        if mesh is None:
            return set()

        all_surfaces = mesh.all_surface_ids()
        return all_surfaces - self.get_visible_surfaces()

    def hide_surfaces(self, surfaces: Sequence[int]):
        self._surfaces_to_hide |= set(surfaces)
        if surfaces:
            self.changed.emit()

    def hide_volumes(self, volumes: Sequence[int]):
        self._volumes_to_hide |= set(volumes)
        if volumes:
            self.changed.emit()

    def unhide_all(self):
        self._surfaces_to_hide.clear()
        self._volumes_to_hide.clear()
        self.changed.emit()
