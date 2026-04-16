from PySide6.QtGui import QDoubleValidator


class StrictDoubleValidator(QDoubleValidator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self, string: str, pos: int):
        string = string.replace(",", ".")

        if string.count(".") > 1:
            return QDoubleValidator.State.Invalid, string, pos

        if is_numeric(string):
            if float(string) < self.bottom():
                return QDoubleValidator.State.Invalid, string, pos

            if float(string) > self.top():
                return QDoubleValidator.State.Invalid, string, pos

        return super().validate(string, pos)


def is_numeric(value: str):
    try:
        float(value)
        return True
    except Exception:
        return False
