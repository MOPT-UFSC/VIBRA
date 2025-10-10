from PySide6.QtGui import QColor
from PySide6.QtCore import Qt

from vibra.interface.formatters.icons import get_error_icon, get_warning_icon
from vibra.interface.ui_generated.messages.exception_message_ui import (
    ExceptionMessage_UI,
)
from vibra.utils.text_utils import pascal_to_spaced_case
from traceback import format_tb


class ExceptionMessage(ExceptionMessage_UI):
    def __init__(self, exception: Exception, stack_trace = None):
        super().__init__()
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)

        if isinstance(exception, Warning):
            self.setWindowIcon(get_warning_icon())
            self.setWindowTitle("Warning")
        else:
            self.setWindowIcon(get_error_icon(QColor(255, 0, 0, 200)))
            self.setWindowTitle("Error")


        if stack_trace is None:
            self.stack_trace_text_browser.hide()
        else:
            traceback = "\n".join(format_tb(stack_trace, limit=2))
            self.stack_trace_text_browser.setText(
                "<code>"
                + "Traceback (most recent call last):\n"
                + traceback
                + "</code>"
            )

        title = pascal_to_spaced_case(exception.__class__.__name__)
        self.title_label.setText(title)

        message = " ".join(str(i) for i in exception.args)
        self.error_message.setText(message)
        
        self.ok_button.clicked.connect(self.close)
