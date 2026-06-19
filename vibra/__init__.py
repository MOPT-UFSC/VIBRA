from time import perf_counter

INTIAL_TIME = perf_counter()  # this need to be at the start of the file

# Use this to allow type hints without circular imports
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vibra.interface.application import Application

from pathlib import Path

from molde import Color
from PySide6.QtWidgets import QApplication

__version__ = "0.5.3"
__release_date__ = "May 2026"

VERSION = __version__
APP_ID = f"mopt.vibra.{VERSION}"

VIBRA_DIR = Path(__file__).parent
PROJECT_DIR = Path(__file__).parents[1]

DEVELOPER_MODE = True

ICONS_ROOT = VIBRA_DIR / "interface/data/icons"
LIGHT_ICONS_DIR = ICONS_ROOT / "light_theme"
DARK_ICONS_DIR = ICONS_ROOT / "dark_theme"
ICON_DIR = DARK_ICONS_DIR
TEXTURE_DIR = VIBRA_DIR / "interface/data/textures/"
UI_DIR = VIBRA_DIR / "interface/data/ui_files/"
SYMBOLS_DIR = VIBRA_DIR / "interface/data/symbols/"
EXAMPLES_DIR = VIBRA_DIR / "interface/data/examples/"

USER_PATH = Path().home()
TEMP_PROJECT_DIR = USER_PATH / "temp_vibra"

SUPPORTED_GEOMETRY_EXTENSIONS = [
    "iges",
    "igs",
    "step",
    "stp",
]

SUPPORTED_MESH_EXTENSIONS = [
    "msh",
    "bdf",
    "nas",
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

def update_icons_dir(theme: str) -> None:
    if theme.lower() == "light":
        ICON_DIR = LIGHT_ICONS_DIR
    else:
        ICON_DIR = DARK_ICONS_DIR

def app() -> "Application":
    return QApplication.instance()
