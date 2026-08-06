import builtins
import os
import platform
import runpy
import signal
import sys
from pathlib import Path

from PySide6.QtCore import QThread, QTimer, Signal
from PySide6.QtWidgets import QApplication, QMainWindow

from vibra.engine.project import Project
from vibra.interface.viewer_3d.render_widgets.preview_render_widget import PreviewRenderWidget
from vibra.utils.preview_utils import SectionPlaneConfig


class ScriptRunner(QThread):
    finished_script = Signal(dict)

    def __init__(self, script_path: Path, script_cache: dict):
        super().__init__()
        self.script_path = script_path
        self.script_cache = script_cache

    def run(self):
        script_variables = {}
        try:
            script_variables = runpy.run_path(self.script_path)
        finally:
            self.finished_script.emit(script_variables)


class MainWindow(QMainWindow):
    def __init__(self, *, script_path):
        super().__init__()

        self.script_path = Path(script_path)
        self.script_cache = {}

        self.render_widget = PreviewRenderWidget()
        self.setCentralWidget(self.render_widget)
        self.setBaseSize(800, 450)

        self.last_modification_time = 0
        self.script_runner: ScriptRunner | None = None

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(500)

    def update(self):
        modification_time = self._modification_time(self.script_path)
        if modification_time <= self.last_modification_time:
            return

        if self.script_runner is not None and self.script_runner.isRunning():
            self.last_modification_time = modification_time
            return

        self.last_modification_time = modification_time

        # Hack to make @preview_cache decorator work
        if not hasattr(builtins, "__HOT_RELOAD_CACHE__"):
            builtins.__HOT_RELOAD_CACHE__ = self.script_cache

        print("\033[H\033[2J", end="")

        self.script_runner = ScriptRunner(self.script_path, self.script_cache)
        self.script_runner.finished_script.connect(self.on_script_finished)
        self.script_runner.start()

    def on_script_finished(self, script_variables: dict):
        self.render_widget.update_model(None)
        self.render_widget.update_section_plane(None)

        for var in script_variables.values():
            match var:
                case Project() as project:
                    self.render_widget.update_model(project.model)
                    self.setWindowTitle(project.model.name)

                case SectionPlaneConfig() as section_plane:
                    self.render_widget.update_section_plane(section_plane)

        self.render_widget.update_plot()

    def _modification_time(self, path: Path) -> float:
        return Path(path).stat().st_mtime


def main(script_path: str | Path):
    # Make the window scale evenly for every monitor
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

    if platform.system() == "Linux":
        os.environ["QT_QPA_PLATFORM"] = "xcb"

    app = QApplication(sys.argv)
    main_window = MainWindow(script_path=script_path)
    main_window.show()

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
