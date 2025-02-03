from dataclasses import dataclass
from enum import IntEnum

from vibra import ICON_DIR
from vibra.interface.general.print_message_input import PrintMessageInput

window_title = "Error"


@dataclass
class VisualizationFilter:
    points: bool = False
    lines: bool = False
    faces: bool = False
    solids: bool = False
    acoustic_symbols: bool = False
    structural_symbols: bool = False

    @classmethod
    def all_false(cls):
        # It is dumb, but it works
        args = [False] * 6
        return cls(*args)

    @classmethod
    def all_true(cls):
        # It is dumb, but it works
        args = [True] * 6
        return cls(*args)
