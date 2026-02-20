from enum import StrEnum, auto

import numpy as np
import xxhash

from vibra.engine.mesher.mesh import Mesh
from vibra.engine.solvers import HarmonicSolver


class HashEnum(StrEnum):
    MESH = auto()
    HARMONIC_SOLUTION = auto()
    MODAL_SOLUTION = auto()
    TABLES = auto()


class ProjectHasher:
    @staticmethod
    def hash_mesh(mesh: Mesh) -> str:
        hasher = xxhash.xxh128()
        hasher.update(mesh.lines_connectivity)
        hasher.update(mesh.faces_connectivity)
        hasher.update(mesh.solids_connectivity)
        hasher.update(mesh.nodal_coordinates)
        return hasher.hexdigest()

    @staticmethod
    def hash_harmonic_solution(solver: HarmonicSolver) -> str:
        hasher = xxhash.xxh128()
        hasher.update(solver.frequencies)
        hasher.update(solver.solution)
        return hasher.hexdigest()

    @staticmethod
    def hash_modal_solution(solver: HarmonicSolver) -> str:
        hasher = xxhash.xxh128()
        hasher.update(solver.natural_frequencies)
        hasher.update(solver.solution)
        return hasher.hexdigest()

    @staticmethod
    def hash_tables(
        acoustic_tables: dict[str, np.ndarray],
        structural_tables: dict[str, np.ndarray],
    ) -> str:
        hasher = xxhash.xxh128()

        for name, array in acoustic_tables.items():
            hasher.update(name)
            hasher.update(array)

        for name, array in structural_tables.items():
            hasher.update(name)
            hasher.update(array)

        return hasher.hexdigest()
