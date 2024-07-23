from PyQt5.QtWidgets import QAction, QMenu
from PyQt5.QtGui import QColor

from vibra.interface.plots.acoustic.plot_particle_velocity_frequency_response_input import PlotParticleVelocityFrequencyResponseInput
from vibra.interface.plots.acoustic.plot_specific_acoustic_impedance_input import PlotSpecificAcousticImpedanceInput

from vibra.interface.viewer_3d.render_widgets.common_render_widget import CommonRenderWidget

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
        self.plot_particle_velocity_action = QAction(self.plot_icon, "Plot particle velocity", self)
        self.plot_specific_acoustic_impedance_action = QAction(self.plot_icon, "Plot specific acoustic impedance", self)
        self.plot_particle_velocity_action.triggered.connect(self.plot_particle_velocity)
        self.plot_specific_acoustic_impedance_action.triggered.connect(self.plot_specific_acoustic_impedance)

    def create_layout(self):
        self.addAction(self.plot_particle_velocity_action)
        self.addAction(self.plot_specific_acoustic_impedance_action)

    def plot_specific_acoustic_impedance(self):
        if app().main_window.project.acoustic_harmonic_solver.solution is None:
            return
        PlotSpecificAcousticImpedanceInput()

    def plot_particle_velocity(self):
        if app().main_window.project.acoustic_harmonic_solver.solution is None:
            return
        PlotParticleVelocityFrequencyResponseInput()

    def disable_advanced_acoustic_plots_buttons(self, _bool : bool):
        self.plot_specific_acoustic_impedance_action.setDisabled(_bool)
        self.plot_particle_velocity_action.setDisabled(_bool)