from enum import StrEnum, auto

import numpy as np
import xxhash

from vibra.engine.mesher.mesh import Mesh
from vibra.engine.solvers import HarmonicSolver, ModalSolver


class HashEnum(StrEnum):
    MESH = auto()
    HARMONIC_SOLUTION = auto()
    MODAL_SOLUTION = auto()
    TABLES = auto()


class ProjectHasher:
    @staticmethod
    def hash_mesh(mesh: Mesh) -> str:
        hasher = xxhash.xxh128()
        hasher.update(mesh.lines_connectivity.flatten())
        hasher.update(mesh.faces_connectivity.flatten())
        hasher.update(mesh.solids_connectivity.flatten())
        hasher.update(mesh.nodal_coordinates.flatten())

        if mesh.has_decoupling():
            hasher.update(mesh.cache_lines_connectivity.flatten())
            hasher.update(mesh.cache_faces_connectivity.flatten())
            hasher.update(mesh.cache_solids_connectivity.flatten())

        for i, normals in mesh.normals_surface.items():
            hasher.update(normals.flatten())

        for i, curvatures in mesh.curvatures_surface.items():
            hasher.update(curvatures.flatten())

        return hasher.hexdigest()

    @staticmethod
    def hash_harmonic_solution(solver: HarmonicSolver) -> str:
        hasher = xxhash.xxh128()
        hasher.update(solver.frequencies.flatten())
        hasher.update(solver.nodal_solution.flatten())
        return hasher.hexdigest()

    @staticmethod
    def hash_modal_solution(solver: ModalSolver) -> str:
        hasher = xxhash.xxh128()
        hasher.update(solver.natural_frequencies.flatten())
        hasher.update(solver.nodal_solution.flatten())
        return hasher.hexdigest()

    @staticmethod
    def hash_tables(
        acoustic_tables: dict[str, np.ndarray],
        structural_tables: dict[str, np.ndarray],
    ) -> str:
        hasher = xxhash.xxh128()

        for name, array in acoustic_tables.items():
            hasher.update(name)
            hasher.update(array.flatten())

        for name, array in structural_tables.items():
            hasher.update(name)
            hasher.update(array.flatten())

        return hasher.hexdigest()
