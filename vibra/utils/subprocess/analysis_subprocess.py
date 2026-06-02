import logging
import sys
import traceback

from vibra import TEMP_PROJECT_DIR
from vibra.engine.project import Project

logging.basicConfig(
    level=logging.INFO,
    format="VIBRA_LOG|%(levelname)s|%(message)s",
    stream=sys.stdout,
)


def main():
    project = Project(TEMP_PROJECT_DIR)
    project.read_from_working_dir()
    project.run_analysis()


if __name__ == "__main__":
    try:
        logging.info("Starting solver subprocess...")
        main()
    except Exception:
        logging.error("Solver subprocess failed.")
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
    else:
        logging.info("Solver subprocess complete")
