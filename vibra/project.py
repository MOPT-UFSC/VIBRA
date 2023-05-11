import logging
from pathlib import Path

from vibra.engine.model import Model


class Project:
    model: Model
    save_path: Path | None
    materials_list: list

    def load(cls, path):
        logging.info(f"Loading {path}")

    def save(self):
        logging.info(f"Saving project in my/save/path")
        print("SALVANDO")
