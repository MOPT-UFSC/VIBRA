from typing import override

import h5py

from vibra.engine import AnalysisID
from vibra.engine.serialization.project_paths import ProjectPaths
from vibra.utils.lazy_array import LazyArray

from .harmonic_solution import HarmonicSolution


class LazyHarmonicSolution(HarmonicSolution):
    def __init__(self, project_paths: ProjectPaths):
        self.project_paths = project_paths

        hs = self.project_paths.harmonic_solution_filepath
        if not hs.exists():
            msg = "LazyHarmonicSolution can not be created without a harmonic solution file"
            raise FileExistsError(msg)

        self.frequencies: LazyArray = LazyArray(hs, "frequencies")
        # self.nodal_solution: LazyArray = LazyArray(hs, "solution")
        self.status: LazyArray = LazyArray(hs, "solution_status")

    @property
    @override
    def analysis_id(self) -> AnalysisID:
        from vibra.engine.serialization.project_reader import ProjectReader

        reader = ProjectReader(self.project_paths)
        return reader.read_current_analysis_id()

    @property
    @override
    def structural_solution(self) -> LazyArray | None:  # pyright: ignore[reportIncompatibleVariableOverride]
        hs = self.project_paths.harmonic_solution_filepath
        with h5py.File(hs, "r") as f:
            if "structural_solution" not in f:
                return None
        return LazyArray(hs, "structural_solution")

    @property
    @override
    def acoustic_solution(self) -> LazyArray | None:  # pyright: ignore[reportIncompatibleVariableOverride]
        hs = self.project_paths.harmonic_solution_filepath
        with h5py.File(hs, "r") as f:
            if "acoustic_solution" not in f:
                return None
        return LazyArray(hs, "acoustic_solution")

    @property
    @override
    def coupled_solution(self) -> LazyArray | None:  # pyright: ignore[reportIncompatibleVariableOverride]
        hs = self.project_paths.harmonic_solution_filepath
        with h5py.File(hs, "r") as f:
            if "coupled_solution" not in f:
                return None
        return LazyArray(hs, "coupled_solution")

    @property
    @override
    def displacement_dof(self) -> LazyArray | None:  # pyright: ignore[reportIncompatibleVariableOverride]
        hs = self.project_paths.harmonic_solution_filepath
        with h5py.File(hs, "r") as f:
            if "displacement_dof" not in f:
                return None
        return LazyArray(hs, "displacement_dof")

    def is_valid(self) -> bool:
        arrays = (
            self.frequencies,
            self.structural_solution,
            self.acoustic_solution,
            self.coupled_solution,
            self.status,
            self.displacement_dof,
        )

        for i in arrays:
            if isinstance(i, LazyArray) and not i.is_valid():
                return False

        return True

    @override
    def copy(self) -> HarmonicSolution:
        disp = self.displacement_dof
        if disp is not None:
            disp = disp.copy()

        return HarmonicSolution(
            analysis_id=self.analysis_id,
            frequencies=self.frequencies.copy(),
            status=self.status.copy(),
            structural_solution=self.structural_solution.copy() if isinstance(self.structural_solution, LazyArray) else self.structural_solution,
            acoustic_solution=self.acoustic_solution.copy() if isinstance(self.acoustic_solution, LazyArray) else self.acoustic_solution,
            coupled_solution=self.coupled_solution.copy() if isinstance(self.coupled_solution, LazyArray) else self.coupled_solution,
            displacement_dof=self.displacement_dof.copy() if isinstance(self.displacement_dof, LazyArray) else self.displacement_dof,
        )
