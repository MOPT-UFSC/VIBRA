from __future__ import annotations

import logging
import sys
from typing import TYPE_CHECKING
from multiprocessing.shared_memory import SharedMemory
import numpy as np
from vibra.engine.project import Project

if TYPE_CHECKING:
    from pathlib import Path


logging.basicConfig(
    level=logging.INFO,
    format="VIBRA_LOG|%(levelname)s|%(message)s",
    stream=sys.stdout,
)


def main(working_dir: Path, shm_name: str):
    project = Project(working_dir)
    project.read_from_working_dir()

    project.reload_solution_from_working_dir()

    structural_postprocessing = project.get_structural_postprocessing()
    stresses = structural_postprocessing.recover_nodal_averaged_structural_stresses()

    shared_mem = SharedMemory(name=shm_name, track=False)
    try:
        if shared_mem.size < stresses.nbytes:
            raise ValueError(f"Shared memory too small: {shared_mem.size} < {stresses.nbytes} bytes")

        target = np.ndarray(stresses.shape, stresses.dtype, shared_mem.buf)
        target[:] = stresses
        del target
    finally:
        shared_mem.close()

