from __future__ import annotations

import logging
import sys
from typing import TYPE_CHECKING

from vibra.engine.project import Project

if TYPE_CHECKING:
    from pathlib import Path


logging.basicConfig(
    level=logging.INFO,
    format="VIBRA_LOG|%(levelname)s|%(message)s",
    stream=sys.stdout,
)


def main(working_dir: Path):
    project = Project(working_dir)
    project.read_from_working_dir()

    project.reload_solution_from_working_dir()

    structural_postprocessing = project.get_structural_postprocessing()
    stresses = structural_postprocessing.recover_nodal_averaged_structural_stresses()

    project.project_writer.write_structural_stresses(stresses)