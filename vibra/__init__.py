from time import perf_counter

INTIAL_TIME = perf_counter()  # this need to be at the start of the file

# Use this to allow type hints without circular imports
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vibra.interface.application import Application

from pathlib import Path

from molde import Color
from PySide6.QtWidgets import QApplication

__version__ = "0.6.0"
__release_date__ = "Jul 2026"

VERSION = __version__
RELEASE_DATE = __release_date__

APP_ID = f"mopt.vibra.{VERSION}"

VIBRA_DIR = Path(__file__).parent
PROJECT_DIR = Path(__file__).parents[1]

DEVELOPER_MODE = True

ICON_DIR = VIBRA_DIR / "interface/data/icons"
LOGO_DIR = VIBRA_DIR / "interface/data/logos"
TEXTURE_DIR = VIBRA_DIR / "interface/data/textures/"
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

SUPPORTED_TEXT_EXTENSIONS = [
    "dat",
    "txt",
    "csv"
]

SUPPORTED_SPREADSHEET_EXTENSIONS = [
    "xls",
    "xlsx"
]

SUPPORTED_OUTPUT_DATA_EXTENSIONS = SUPPORTED_TEXT_EXTENSIONS + SUPPORTED_SPREADSHEET_EXTENSIONS

SUPPORTED_ANIMATION_EXTENSIONS = [
    "webp",
    "gif"
]

SUPPORTED_VIDEO_EXTENSIONS = [
    "mp4",
]


LIGHT_ICON_COLOR = Color("#0051A2")
DARK_ICON_COLOR = Color("#84AAFF")


def app() -> "Application":
    return QApplication.instance()
