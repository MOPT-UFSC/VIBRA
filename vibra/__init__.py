# Use this to allow type hints without circular imports
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from vibra.interface.application import Application

import pkg_resources

# copying the version from pyproject.toml
__version__ = pkg_resources.get_distribution('vibra').version
__release_date__ = 'August 1st 2024'

from PyQt5.QtWidgets import QApplication
from pathlib import Path

VIBRA_DIR = Path(__file__).parent
ICON_DIR = VIBRA_DIR / "interface/data/icons/"
UI_DIR = VIBRA_DIR / "interface/data/ui_files/"
SYMBOLS_DIR = VIBRA_DIR / "interface/data/symbols/"

def app() -> "Application":
    return QApplication.instance()
