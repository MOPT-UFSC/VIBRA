import logging
from pathlib import Path
from time import sleep

from vibra.engine.model import Model
from vibra.utils import ProgressStatus


class Project:
    model: Model
    save_path: Path | None
    materials_list: list

    def load(cls, path):
        logging.info(f"Loading {path}")

    def save(self):
        logging.info(f"Saving project in my/save/path")
        print("SALVANDO")

    def long_function(self):
        for i in range(20):
            logging.info("long_function" + ProgressStatus(i, 20))

            print(i)
            sleep(0.1)
