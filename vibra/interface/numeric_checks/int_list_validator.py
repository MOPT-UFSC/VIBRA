import re

from PySide6.QtGui import QValidator


class IntListValidator(QValidator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._re = re.compile(r"\s*\d+\s*(,\s*\d+\s*)*,?\s*")

    def validate(self, string: str, pos: int):
        if string == "":
            return QValidator.State.Intermediate, string, pos

        if not self._re.fullmatch(string):
            return QValidator.State.Invalid, string, pos

        for i in string.strip(", ").split(","):
            try:
                int(i)
            except Exception:
                return QValidator.State.Intermediate, string, pos

        return QValidator.State.Acceptable, string, pos
