import logging
import os
import sys
from traceback import format_tb
import platform

from vtkmodules.vtkCommonCore import vtkLogger, vtkObject

from vibra import USER_PATH
from vibra.errors import VibraException
from vibra.interface.application import Application

error_message = None


def custom_exception_hooks(exc_type, exc_value, exc_traceback):
    global error_message

    if issubclass(exc_type, KeyboardInterrupt):
        sys.exit()

    # Logs unhandled errors for future checks
    if not isinstance(exc_value, VibraException):
        logging.error("Unhandled error", exc_info=(exc_type, exc_value, exc_traceback))

    try:
        from vibra.interface.message.exception_message import ExceptionMessage

        if isinstance(error_message, ExceptionMessage):
            error_message.close()

        if isinstance(exc_value, VibraException):
            exc_traceback = None

        error_message = ExceptionMessage(exc_value, stack_trace=exc_traceback)
        error_message.show()

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
    file_formatter = logging.Formatter("%(asctime)s \t | %(levelname)s \t | %(message)s")
    file_handler = logging.FileHandler(USER_PATH / ".vibra.log", "w+")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(file_formatter)

    stream_formatter = logging.Formatter(logging.BASIC_FORMAT)
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
    # Import enabling compiled qt resources to be found from path `:/icons/{filepath_relative_to_qrc}`
    import vibra.interface.data.icons.resources_rc  # noqa: F401

    configure_logs()

    # disables the terrible vtk error handler and its logs
    # you may want to enable them while debugging something
    vtkObject.GlobalWarningDisplayOff()
    vtkLogger.SetStderrVerbosity(vtkLogger.VERBOSITY_OFF)

    # Make the window scale evenly for every monitor
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

    # Ensure the use of X11 instead of Wayland in Linux systems
    # This is needed because VTK is not compatible with Wayland
    if platform.system() == "Linux":
        os.environ["QT_QPA_PLATFORM"] = "xcb"

    app = Application(sys.argv)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
