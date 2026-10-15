from __future__ import annotations

from multiprocessing.shared_memory import SharedMemory
from typing import TYPE_CHECKING

import numpy as np

from vibra.utils.subprocess.subprocess_handler import SubProcessHandler, SubProcessStatus

if TYPE_CHECKING:
    from pathlib import Path



def recover_structural_stresses_in_subprocess(working_dir: Path, shape: tuple[int, ...]) -> np.ndarray | None:
    dtype = np.dtype(complex)
    shm = SharedMemory(create=True, size=max(1, int(np.prod(shape)) * dtype.itemsize))
    try:
        command = SubProcessHandler.get_executable(True) + [
            "--recover-structural-stresses", str(working_dir),
            "--shm-name", shm.name,
        ]
        if SubProcessHandler(command).run() != SubProcessStatus.SUCCESS:
            return None
        return np.ndarray(shape, dtype=dtype, buffer=shm.buf).copy()
    finally:
        shm.close()
        shm.unlink()
