from PySide6.QtWidgets import QGridLayout
from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import Qt

from vibra import app
from vibra.interface.ui_generated.model.fluid.simplified_fluid_inputs_ui import SimplifiedFluidInputs_UI
from vibra.interface.model_inputs.fluid.fluid_widget import FluidWidget


class SetFluidInputsSimplified(SimplifiedFluidInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.update_workspace = kwargs.get("update_workspace", True)

        app().main_window.set_input_widget(self)

        if self.update_workspace:
            app().main_window.workspace_updating_for_model_setup()

        self._initialize()
        self._config_window()
        self._add_fluid_widget()
        self._create_connections()

    def _initialize(self):
        self.fluid = None
        self.complete = False
        self.keep_window_open = True

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.vibra_icon)
        self.setWindowTitle("Vibra")

    def _create_connections(self):
        self.fluid_widget.pushButton_cancel.clicked.connect(self.close)
        self.fluid_widget.tableWidget_fluid_data.currentCellChanged.connect(self.current_cell_changed)

    def _add_fluid_widget(self):
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0,0,0,0)
        self.scrollArea_table_of_fluids.setLayout(self.grid_layout)

        self.fluid_widget = FluidWidget()
        self.grid_layout.addWidget(self.fluid_widget)
        self.fluid_widget.pushButton_remove_column.clicked.connect(self.reset_selected_fluid_lineEdit)

    def reset_fluid_library_callback(self):
        self.hide()
        self.fluid_widget.reset_library_callback()

    def reset_selected_fluid_lineEdit(self):
        self.lineEdit_selected_fluid_name.setText("")

    def current_cell_changed(self, current_row, current_col, previous_row, previous_col):
        self.update_fluid_selection(current_col)

    def update_fluid_selection(self, selected_column: int):

        if not isinstance(selected_column, int):
            return

        item_0 = self.fluid_widget.tableWidget_fluid_data.item(0, selected_column)
        if item_0 is None:
            return
        
        item_1 = self.fluid_widget.tableWidget_fluid_data.item(1, selected_column)
        if item_1 is None:
            return

        fluid_name = item_0.text()
        fluid_identifier = item_1.text()

        self.lineEdit_fluid_identifier.clear()
        self.lineEdit_selected_fluid_name.clear()

        if fluid_name != "":
            self.lineEdit_selected_fluid_name.setText(fluid_name)

        if fluid_identifier != "":
            self.lineEdit_fluid_identifier.setText(fluid_identifier)

    def get_selected_fluid(self):
        return self.fluid_widget.get_selected_fluid()

    def load_model_info(self):
        pass

    def exec_and_keep_window_open(self):
        self.keep_window_open = True
        while self.keep_window_open:
            self.exec()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)