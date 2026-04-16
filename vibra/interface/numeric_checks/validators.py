from PySide6.QtGui import QDoubleValidator


class StrictDoubleValidator(QDoubleValidator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self, string: str, pos: int):
        string = string.replace(",", ".")

        if string.count(".") > 1:
            return QDoubleValidator.State.Invalid, string, pos

        if not is_numeric(string):
            return super().validate(string, pos)

        value = float(string)
        if value < self.bottom() or value > self.top():
            return QDoubleValidator.State.Intermediate, string, pos

        return super().validate(string, pos)


def is_numeric(value: str):
    try:
        float(value)
        return True
    except Exception:
        return False
