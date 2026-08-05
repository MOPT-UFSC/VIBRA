import builtins
import os
import platform
import runpy
import sys
from pathlib import Path

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QMainWindow

from vibra.engine.project import Project
from vibra.interface.viewer_3d.render_widgets.preview_render_widget import PreviewRenderWidget


class MainWindow(QMainWindow):
    def __init__(self, *, script_path):
        super().__init__()

        self.script_path = Path(script_path)
        self.script_cache = {}

        self.render_widget = PreviewRenderWidget()
        self.setCentralWidget(self.render_widget)
        self.setBaseSize(800, 450)

        self.last_modification_time = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(500)

    def update(self):
        modification_time = self._modification_time(self.script_path)
        if modification_time <= self.last_modification_time:
            return
        self.last_modification_time = modification_time

        # Hack to make @preview_cache decorator work
        if not hasattr(builtins, "__HOT_RELOAD_CACHE__"):
            builtins.__HOT_RELOAD_CACHE__ = self.script_cache

        print("\033[H\033[2J", end="")
        script_variables = runpy.run_path(self.script_path)

        for var in script_variables.values():
            if isinstance(var, Project):
                self.render_widget.model = var.model
                self.setWindowTitle(var.model.name)
                break
        else:
            return

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

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
