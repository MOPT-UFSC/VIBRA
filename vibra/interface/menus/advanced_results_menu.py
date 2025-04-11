from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QColor, QAction

from vibra.interface.plots.acoustic.export_element_transfer_data_input import ExportElementTransferDataInput

from molde.render_widgets import CommonRenderWidget


from vibra import app, ICON_DIR
from vibra.utils.icons import load_icon


class AdvancedResultsMenu(QMenu):
    def __init__(self, parent):
        super().__init__(parent)
        self.setTitle("Advanced results")

        self.create_actions()
        self.create_layout()
        self.disable_advanced_acoustic_plots_buttons(True)

    def create_actions(self):

        color = QColor("#448cff")
        self.plot_icon = load_icon(ICON_DIR / "image-plus.png", color)
        self.export_icon = load_icon(ICON_DIR / "exit.png", color)

        self.plot_particle_velocity_action = QAction(self.plot_icon, "Plot particle velocity", self)
        self.plot_particle_velocity_action.triggered.connect(self.plot_particle_velocity)

        self.plot_specific_acoustic_impedance_action = QAction(self.plot_icon, "Plot specific acoustic impedance", self)
        self.plot_specific_acoustic_impedance_action.triggered.connect(self.plot_specific_acoustic_impedance)

        self.export_element_transfer_data_action = QAction(self.export_icon, "Export element transfer data", self)
        self.export_element_transfer_data_action.triggered.connect(self.export_element_transfer_data_callback)

    def create_layout(self):
        self.addAction(self.plot_particle_velocity_action)
        self.addAction(self.plot_specific_acoustic_impedance_action)
        self.addAction(self.export_element_transfer_data_action)

    def export_element_transfer_data_callback(self):
        if app().project.acoustic_harmonic_solver.solution is None:
            return
        ExportElementTransferDataInput()

    def disable_advanced_acoustic_plots_buttons(self, disabled : bool):
        self.plot_specific_acoustic_impedance_action.setDisabled(disabled)
        self.plot_particle_velocity_action.setDisabled(disabled)
        self.export_element_transfer_data_action.setDisabled(disabled)