import logging
from pathlib import Path
from time import sleep

from vibra.engine.mesh import Mesh
from vibra.engine.model import Model
from vibra.utils import ProgressStatus


class Project:
    def __init__(self):
        self.name = "Project"
        self.mesh = None

        # things that might be usefull
        model: Model
        save_path: Path | None
        materials_list: list

    @classmethod
    def load(cls, path):
        logging.info(f"Loading {path}")

    def save(self):
        logging.info(f"Saving project in my/save/path")
        print("SALVANDO")

    def import_geometry(self, path):
        logging.info(f"Importing geometry at {path}")

        path = Path(path)
        mesh = Mesh.from_file(path)
        self.mesh = mesh

    def long_function(self):
        for i in range(20):
            logging.info("long_function" + ProgressStatus(i, 20))

            print(i)
            sleep(0.1)
