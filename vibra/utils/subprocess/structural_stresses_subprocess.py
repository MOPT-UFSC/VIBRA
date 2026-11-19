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

    structural_postprocessing = project.get_structural_postprocessing()
    shape = structural_postprocessing.get_nodal_stresses_frequency_shape()
    dtype = np.dtype(complex)

    shared_mem = SharedMemory(name=shm_name, track=False)
    try:
        target = np.ndarray(shape, dtype, shared_mem.buf)
        structural_postprocessing.recover_nodal_averaged_structural_stresses_calculations(out=target)
    finally:
        shared_mem.close()

