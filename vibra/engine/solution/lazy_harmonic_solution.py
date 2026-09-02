from typing import Optional, override

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

    def get_nodal_displacement_at_column(self, column_index: int):
        """
        It is VERY important to get the columns first.
        Otherwise the whole file will be loaded to extract a single column.
        """
        col = self.get_column(column_index)
        return col[self.displacement_dof]

    def is_valid(self) -> bool:
        for i in (self.frequencies, self.nodal_solution, self.status):
            if not i.is_valid():
                return False

        if isinstance(self.displacement_dof, LazyArray) and not self.displacement_dof.is_valid():
            return False

        return True

    def copy(self) -> HarmonicSolution:
        disp = self.displacement_dof
        if disp is not None:
            disp = disp.copy()

        return HarmonicSolution(
            analysis_id=self.analysis_id,
            frequencies=self.frequencies.copy(),
            nodal_solution=self.nodal_solution.copy(),
            status=self.status.copy(),
            displacement_dof=disp,
        )
