# Use this to allow type hints without circular imports
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from vibra.interface.application import Application

from importlib.metadata import version
# copying the version from pyproject.toml
__version__ = version('vibra')
__release_date__ = 'July 22th 2024'

from PyQt5.QtWidgets import QApplication
from pathlib import Path

VIBRA_DIR = Path(__file__).parent
ICON_DIR = VIBRA_DIR / "interface/data/icons/"
UI_DIR = VIBRA_DIR / "interface/data/ui_files/"
SYMBOLS_DIR = VIBRA_DIR / "interface/data/symbols/"
EXAMPLES_DIR = VIBRA_DIR / "interface/data/examples/"

USER_PATH = Path().home()
TEMP_PROJECT_DIR = USER_PATH / "temp_vibra"
TEMP_PROJECT_FILE = str(TEMP_PROJECT_DIR / "tmp.vibra") 

def app() -> "Application":
    return QApplication.instance()
