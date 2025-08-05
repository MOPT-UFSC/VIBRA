# Use this to allow type hints without circular imports
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vibra.interface.application import Application

# copying the version from pyproject.toml
__version__ = "0.3.2"
__release_date__ = "June 24th 2024"

from pathlib import Path

from PySide6.QtWidgets import QApplication

VIBRA_DIR = Path(__file__).parent
PROJECT_DIR = Path(__file__).parents[1]

ICON_DIR = VIBRA_DIR / "interface/data/icons/"
UI_DIR = VIBRA_DIR / "interface/data/ui_files/"
SYMBOLS_DIR = VIBRA_DIR / "interface/data/symbols/"
EXAMPLES_DIR = VIBRA_DIR / "interface/data/examples/"

USER_PATH = Path().home()
TEMP_PROJECT_DIR = USER_PATH / "temp_vibra"
TEMP_PROJECT_FILE = TEMP_PROJECT_DIR / "tmp.vibra"

SUPPORTED_GEOMETRY_EXTENSIONS = [
    "iges",
    "IGES",
    "igs",
    "IGS",
    "step",
    "STEP",
    "stp",
    "STP",
]

SUPPORTED_MESH_EXTENSIONS = [
    "bdf",
    "BDF",
    "nas",
    "NAS",
]

production = True

def change_prod_dev() -> bool:
    global production
    production = not production
    return production

def app() -> "Application":
    return QApplication.instance()
