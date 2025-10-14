import os
from pathlib import Path


def get_data_path(path: str) -> str:
    filepath = os.path.abspath(__file__)
    base_path = Path(os.path.dirname(filepath))
    return str(base_path / path)
