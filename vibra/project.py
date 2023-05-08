from vibra.engine.model import Model
from pathlib import Path


class Project:
    model: Model
    save_path: Path | None
    materials_list: list

    def load(cls):
        pass

    def save(self):
        pass
    