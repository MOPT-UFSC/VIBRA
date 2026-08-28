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


def main(is_resume: bool, working_dir: Path):
    project = Project(working_dir)
    project.read_from_working_dir()
    project.run_analysis(is_resume)


if __name__ == "__main__":
    import traceback
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        "-r",
        "--resume",
        action="store_true",
    )
    args = parser.parse_args()

    try:
        logging.info("Starting solver subprocess...")
        main(args.resume)
    except Exception:
        logging.error("Solver subprocess failed.")
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
    else:
        logging.info("Solver subprocess complete")
