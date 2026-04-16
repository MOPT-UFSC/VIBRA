import re

from PySide6.QtGui import QValidator


class IntListValidator(QValidator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._re = re.compile(r"^\d+(\s*,\s*\d+)*,?$")

    def validate(self, string: str, pos: int):
        if string == "":
            return QValidator.State.Intermediate, string, pos

        if self._re.fullmatch(string):
            return QValidator.State.Acceptable, string, pos

        return QValidator.State.Invalid, string, pos
