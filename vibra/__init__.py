from time import perf_counter

INTIAL_TIME = perf_counter()  # this need to be at the start of the file

# Use this to allow type hints without circular imports
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vibra.interface.application import Application

from pathlib import Path


__version__ = "0.6.1"
__release_date__ = "Aug 2026"

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


def __getattr__(name: str):
    if name == "Color":
        from molde import Color

        globals()[name] = Color
        return Color

    colors = {
        "LIGHT_ICON_COLOR": "#0051A2",
        "DARK_ICON_COLOR": "#84AAFF",
    }
    if name in colors:
        from molde import Color

        value = Color(colors[name])
        globals()[name] = value
        return value

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

def app() -> "Application":
    from PySide6.QtWidgets import QApplication
    return QApplication.instance()
