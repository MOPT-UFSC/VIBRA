# Use this to allow type hints without circular imports
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vibra.interface.application import Application

# copying the version from pyproject.toml
__version__ = "0.3.2"
__release_date__ = "June 24th 2024"

from pathlib import Path

from PySide6.QtWidgets import QApplication
from molde import Color

VIBRA_DIR = Path(__file__).parent
PROJECT_DIR = Path(__file__).parents[1]

DEVELOPER_MODE = False

ICON_DIR = VIBRA_DIR / "interface/data/icons/"
TEXTURE_DIR = VIBRA_DIR / "interface/data/textures/"
UI_DIR = VIBRA_DIR / "interface/data/ui_files/"
SYMBOLS_DIR = VIBRA_DIR / "interface/data/symbols/"
EXAMPLES_DIR = VIBRA_DIR / "interface/data/examples/"

USER_PATH = Path().home()
TEMP_PROJECT_DIR = USER_PATH / "temp_vibra"

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

SUPPORTED_OUTPUT_DATA_EXTENSIONS = [
    "dat",
    "txt",
    "csv",
    "xls",
    "xlsx",
]

LIGHT_ICON_COLOR = Color("#1a73e8")
DARK_ICON_COLOR = Color("#5F9AF4")

def app() -> "Application":
    return QApplication.instance()
