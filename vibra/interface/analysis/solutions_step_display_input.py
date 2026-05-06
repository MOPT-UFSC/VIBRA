import numpy as np
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QAbstractItemView, QHeaderView, QTableWidgetItem

from vibra import app
from vibra.engine.analysis_info import HarmonicAnalysisSetup
from vibra.interface.ui_generated.analysis.solution_steps_display_input_ui import SolutionStepsDisplayInput_UI


class SolutionStepsDisplayInput(SolutionStepsDisplayInput_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)

        self._initialize()
        self._config_window()
        self._create_connections()

        self.load_solution_steps()

        while self.keep_window_open:
            self.exec()

    @property
    def model(self):
        return app().project.model
    
    @property
    def analysis_setup(self):
        return app().project.model.analysis_setup

    def _initialize(self):
        self.setup_defined = False
        self.solve_analysis = False
        self.keep_window_open = True
        self.user_defined_solution_steps = list()
        self.table_exists = self.model.properties.check_if_there_are_tables_at_the_model()
        self.tabular_frequency_setup = self.model.get_tabular_frequency_setup()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Analysis setup")

    def _create_connections(self):
        self.pushButton_exit.clicked.connect(self.close)

    def load_solution_steps(self):
        self.tableWidget_solution_steps.clearContents()
        self.tableWidget_solution_steps.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableWidget_solution_steps.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_solution_steps.setSelectionMode(QAbstractItemView.NoSelection)

        frequencies = self.model.frequencies
        if frequencies is None:
            return
                
        if isinstance(frequencies, np.ndarray | list):
            self.tableWidget_solution_steps.setRowCount(len(frequencies))
            if not isinstance(self.analysis_setup, HarmonicAnalysisSetup):
                return

            frequency_spacing = self.analysis_setup.frequency_spacing

            for index, freq in enumerate(frequencies):
                self.tableWidget_solution_steps.setItem(index, 0, QTableWidgetItem(str(index+1)))
                self.tableWidget_solution_steps.setItem(index, 1, QTableWidgetItem(str(freq)))
                self.tableWidget_solution_steps.setItem(index, 2, QTableWidgetItem(frequency_spacing))

                for j in range(3):
                    self.tableWidget_solution_steps.item(index, j).setTextAlignment(Qt.AlignCenter)

    def closeEvent(self, a0):
        self.keep_window_open = False
        return super().closeEvent(a0)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return or event.key() == Qt.Key_Escape:
            self.close()