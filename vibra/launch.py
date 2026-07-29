# isort: skip_file
import vibra  # this need to be at the start of the file

import logging
import os
import platform
import sys

from PySide6.QtCore import QLocale

from vibra.errors import VibraException

error_message = None


def custom_exception_hooks(exc_type, exc_value, exc_traceback):
    global error_message

    if issubclass(exc_type, KeyboardInterrupt):
        sys.exit()

    # Logs unhandled errors for future checks
    if not isinstance(exc_value, VibraException):
        logging.error("Unhandled error", exc_info=(exc_type, exc_value, exc_traceback))

    try:
        from vibra.interface.user_input.exception_message import ExceptionMessage

        if isinstance(error_message, ExceptionMessage):
            error_message.close()

        if isinstance(exc_value, VibraException) and not exc_value.show_traceback:
            exc_traceback = None

        error_message = ExceptionMessage(exc_value, stack_trace=exc_traceback)
        error_message.show()
        error_message.move_stacktrace_to_bottom()

    except Exception as e:
        logging.exception(e)


sys.excepthook = custom_exception_hooks


def configure_logs():
    """
    Configures the logging library.
    Format includes time, log level (info, debug, error and so on).

    The main level is set to NOSET, so every handler can select its
    own filters.

    All info logs are saved in the file, but only warnings or error
    are shown to users.
    """
    format = '[%(name)s] %(asctime)s | %(levelname)s | "%(message)s"'

    file_formatter = logging.Formatter(format)
    file_handler = logging.FileHandler(vibra.USER_PATH / ".vibra.log", "w+")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(file_formatter)

    stream_formatter = logging.Formatter(format)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.WARN)
    stream_handler.setFormatter(stream_formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.NOTSET)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


def main():
    """
    The main function starts the Vibra software.
    This will create the Application and also pass the terminal arguments to it.
    """
    # Import enabling compiled qt resources to be found from path `:/data/{filepath_relative_to_qrc}`
    from PySide6.QtCore import Qt
    from vtkmodules.vtkCommonCore import vtkLogger, vtkObject

    import vibra.interface.data.icons.theme_resources  # noqa: F401
    from vibra.interface.application import Application

    configure_logs()

    # disables the terrible vtk error handler and its logs
    # you may want to enable them while debugging something
    vtkObject.GlobalWarningDisplayOff()
    vtkLogger.SetStderrVerbosity(vtkLogger.VERBOSITY_OFF)

    # Make the window scale evenly for every monitor
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

    Application.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)

    if platform.system() == "Linux":
        # Ensure the use of X11 instead of Wayland in Linux systems
        # This is needed because VTK is not compatible with Wayland
        os.environ["QT_QPA_PLATFORM"] = "xcb"

        # The native dialogs may not appear in some linux distributions
        Application.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, True)

    if platform.system() == "Windows":
        import ctypes

        # This forces the Vibra icon to appear in the taskbar
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(vibra.APP_ID)

    QLocale.setDefault(QLocale.c())

    app = Application(sys.argv)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
