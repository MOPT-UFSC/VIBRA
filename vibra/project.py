from pathlib import Path

from vibra.engine.model import Model


class Project:
    model: Model
    save_path: Path | None
    materials_list: list

    def load(cls):
        print("CARREGANDO")

    def save(self):
        print("SALVANDO")
