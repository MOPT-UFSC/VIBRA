from PySide6.QtWidgets import QFrame, QWidget

from vibra import app
from vibra.interface.ui_generated.menu.left_menu_widget_ui import LeftMenuWidget_UI
from vibra.interface.menus.results_viewer_items import ResultsViewerItems
from vibra.interface.plots.acoustic.plot_acoustic_mode_shape import PlotAcousticModeShape
from vibra.interface.plots.acoustic.plot_acoustic_pressure_field import PlotAcousticPressureField
from vibra.interface.plots.structural.plot_displacement_field import PlotDisplacementField
from vibra.interface.plots.structural.plot_structural_mode_shape import PlotStructuralModeShape


class ResultsViewerWidget(LeftMenuWidget_UI):
    def __init__(self):
        super().__init__()

        self.plot_structural_modal = PlotStructuralModeShape()
        self.plot_structural_harmonic = PlotDisplacementField()
        self.plot_acoustic_modal = PlotAcousticModeShape()
        self.plot_acoustic_harmonic = PlotAcousticPressureField()

        self._reset()
        self._define_qt_variables()
        self._create_connections()

    def _reset(self):
        self.current_widget = None
    
    def hide_bottom_widget(self):
        self.bottom_widget.hide()

    def _define_qt_variables(self):
        self.main_frame = QFrame()
        self.results_viewer_items = ResultsViewerItems()
        
        self.layout().replaceWidget(self.top_widget, self.results_viewer_items)
        self.adjustSize()
    
    def _create_connections(self):
        # Structural
        self.results_viewer_items.item_child_plot_structural_mode_shapes.clicked.connect(self.add_structural_modal_widget)
        self.results_viewer_items.item_child_plot_structural_frequency_response.clicked.connect(self.add_structural_frequency_response_widget)
        self.results_viewer_items.item_child_plot_displacement_field.clicked.connect(self.add_structural_harmonic_widget)

        # Acoustic
        self.results_viewer_items.item_child_plot_acoustic_pressure_field.clicked.connect(self.add_acoustic_harmonic_widget)
        self.results_viewer_items.item_child_plot_acoustic_pressure_frequency_response.clicked.connect(self.add_acoustic_pressure_frequency_response_widget)
        self.results_viewer_items.item_child_plot_acoustic_pressure_frequency_response_function.clicked.connect(self.add_acoustic_pressure_frequency_response_function_widget)
        self.results_viewer_items.item_child_plot_TL_NR.clicked.connect(self.add_TL_NR_widget)
        self.results_viewer_items.item_child_plot_acoustic_mode_shapes.clicked.connect(self.add_acoustic_modal_widget)
    
    def get_item(self):
        return self.results_viewer_items

    def update_visibility_items(self):
        self.results_viewer_items._update_items()
        self.results_viewer_items.update_tree_visibility_after_solution()

    def add_structural_modal_widget(self):
        self.plot_structural_modal.load_natural_frequencies()
        self.plot_structural_modal.load_user_preference_colormap()
        self.plot_structural_modal.update_plot()
        self.add_widget(self.plot_structural_modal, animation_widget=True)

    def add_structural_harmonic_widget(self):
        self.plot_structural_harmonic.load_frequencies()
        self.plot_structural_harmonic.load_user_preference_colormap()
        self.plot_structural_harmonic.update_plot()
        self.add_widget(self.plot_structural_harmonic, animation_widget=True)

    def add_acoustic_modal_widget(self):
        self.plot_acoustic_modal.load_natural_frequencies()
        self.plot_acoustic_modal.load_user_preference_colormap()
        self.plot_acoustic_modal.update_plot()
        self.add_widget(self.plot_acoustic_modal, animation_widget=True)

    def add_acoustic_harmonic_widget(self):
        self.plot_acoustic_harmonic.load_frequencies()
        self.plot_acoustic_harmonic.load_user_preference_colormap()
        self.plot_acoustic_harmonic.update_plot()
        self.add_widget(self.plot_acoustic_harmonic, animation_widget=True)

    def add_structural_frequency_response_widget(self):
        self.current_widget = app().main_window.input_ui.plot_structural_frequency_response()

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()
        
        app().main_window.animation_toolbar.setDisabled(True)

        self.add_widget(self.current_widget)

    def add_acoustic_pressure_frequency_response_widget(self):
        self.current_widget = app().main_window.input_ui.plot_acoustic_pressure_frequency_response()

        # if app().main_window.acoustic_harmonic_analysis.playing_animation:
        #     app().main_window.acoustic_harmonic_analysis.stop_animation()
        
        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        app().main_window.animation_toolbar.setDisabled(True)

        self.add_widget(self.current_widget)
    
    def add_acoustic_pressure_frequency_response_function_widget(self):
        self.current_widget = app().main_window.input_ui.plot_acoustic_pressure_frequency_response_function()

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        # if app().main_window.acoustic_harmonic_analysis.playing_animation:
        #     app().main_window.acoustic_harmonic_analysis.stop_animation()
        #     app().main_window.animation_toolbar.setDisabled(True)

        self.add_widget(self.current_widget)
    
    def add_TL_NR_widget(self):
        self.current_widget = app().main_window.input_ui.plot_TL_NR()

        if app().main_window.results_widget.playing_animation:
            app().main_window.results_widget.stop_animation()

        # if app().main_window.acoustic_harmonic_analysis.playing_animation:
        #     app().main_window.acoustic_harmonic_analysis.stop_animation()
        
        app().main_window.animation_toolbar.setDisabled(True)

        self.add_widget(self.current_widget)


        # self.current_widget = app().main_window.input_ui.plot_acoustic_mode_shapes()
        # app().main_window.acoustic_modal_analysis.configure_menu_widget(self.current_widget)
        # self.add_widget(self.current_widget)

        # app().main_window.acoustic_modal_analysis.update_plot()

    def add_widget(self, widget: QWidget, animation_widget=False):

        # app().main_window.animation_toolbar.setEnabled(False)

        # TODO: please, remove the hide after all it shouldn't be needed
        if isinstance(self.bottom_widget, QWidget):
            self.bottom_widget.hide()

        self.layout().replaceWidget(self.bottom_widget, widget)
        self.bottom_widget = widget

        # app().main_window.animation_toolbar.setEnabled(animation_widget)
        self.adjustSize()
        widget.show()