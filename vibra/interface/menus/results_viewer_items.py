from PySide6.QtGui import QColor, QPen
from PySide6.QtCore import Qt

from vibra import app
from vibra.engine import AnalysisID
from vibra.interface.menus.common_menu_items import CommonMenuItems


class ResultsViewerItems(CommonMenuItems):
    """Menu Items

    This class is responsible for creating, configuring and building the items
    in the items menu, located on the left side of the interface.

    """
    def __init__(self):
        super().__init__()

        self.main_window = app().main_window
        self.project = app().project

        self.setObjectName("results_viewer_items")
        self._create_items()
        self._create_connections()

    def _create_items(self):

        ## Structural results items
        self.item_top_results_viewer_structural = self.add_top_item("Results Viewer - Structural")
        self.item_child_structural_mode_shapes = self.add_item("Plot Structural Mode Shapes")
        self.item_child_displacement_field = self.add_item("Plot Displacement Field")
        self.item_child_structural_frequency_response = self.add_item("Plot Structural Frequency Response")
        # self.item_child_reaction_frequency_response = self.add_item("Plot Reactions Frequency Response")
        # self.item_child_stress_field = self.add_item("Plot Stress Field")
        # self.item_child_stress_frequency_response = self.add_item("Plot Stress Frequency Response")

        ## Acoustic results items
        self.item_top_results_viewer_acoustic = self.add_top_item("Results Viewer - Acoustic")
        self.item_child_acoustic_mode_shapes = self.add_item("Acoustic Mode Shapes")
        self.item_child_acoustic_pressure_field = self.add_item("Acoustic Pressure Field")
        self.item_child_acoustic_pressure_frequency_response = self.add_item("Acoustic Pressure Frequency Response")
        self.item_child_acoustic_pressure_frequency_response_function = self.add_item("Acoustic Presssure Frequency Response Function")
        self.item_child_TL_NR = self.add_item("Transmission Loss or Attenuation")
        self.item_child_particle_velocity = self.add_item("Particle Velocity")
        self.item_child_acoustic_specific_impedance = self.add_item("Acoustic Specific Impedance")

        self.top_level_items = [
                                self.item_top_results_viewer_acoustic,
                                self.item_top_results_viewer_structural
                                ]

    def _create_connections(self):
        """
        This function iterates through all child items, connecting the items one by one
        into a function called child name + _callback, if the function exists
        """

        for top_level_items in self.top_level_items:
            for index in range(top_level_items.childCount()):
                item_child = top_level_items.child(index)
                item_child_name = self._find_qtree_widget_item_name(item_child)

                if item_child_name is None:
                    continue

                function_name = item_child_name + "_callback"
                function_exists = hasattr(self, function_name)
            
                if not function_exists:
                    continue

                function = getattr(self, function_name)
                if callable(function):
                    item_child.clicked.connect(function)

        app().main_window.theme_changed.connect(self.set_theme)

    def _find_qtree_widget_item_name(self, qtree_widet_item):
        for attr_name, attr_value in self.__dict__.items():
            if attr_value == qtree_widet_item:
                return attr_name

    def item_child_reaction_frequency_response_callback(self):
        return
        app().main_window.input_ui.plot_reaction_frequency_response()

    def item_child_stress_field_callback(self):
        return
        app().main_window.input_ui.plot_stress_field()

    def item_child_stress_frequency_response_callback(self):
        return
        app().main_window.input_ui.plot_stress_frequency_response()

    def modify_acoustic_results_viewer_items(self, key: bool):
        self.item_top_results_viewer_acoustic.setHidden(key)
        self.item_child_acoustic_mode_shapes.setDisabled(key)
        self.item_child_acoustic_pressure_frequency_response.setDisabled(key)
        self.item_child_acoustic_pressure_frequency_response_function.setDisabled(key)
        self.item_child_acoustic_pressure_field.setDisabled(key)
        self.item_child_TL_NR.setDisabled(key)
        self.item_child_particle_velocity.setDisabled(key)
        self.item_child_acoustic_specific_impedance.setDisabled(key)

    def modify_structural_results_viewer_items(self, key: bool):
        self.item_top_results_viewer_structural.setHidden(key)
        self.item_child_displacement_field.setDisabled(key)
        self.item_child_structural_frequency_response.setDisabled(key)
        # self.item_child_reaction_frequency_response.setDisabled(key)
        # self.item_child_stress_field.setDisabled(key)
        self.item_child_structural_mode_shapes.setDisabled(key)
    
    def update_structural_analysis_visibility_items(self):
        self.item_top_results_viewer_structural.setHidden(False)
        self.item_top_results_viewer_acoustic.setHidden(True)
        self.main_window.model_setup_widget.model_setup_items.hide_all_top_items()

    def update_acoustic_analysis_visibility_items(self):
        self.item_top_results_viewer_acoustic.setHidden(False)
        self.item_top_results_viewer_structural.setHidden(True)
        self.main_window.model_setup_widget.model_setup_items.hide_all_top_items()

    def update_coupled_analysis_visibility_items(self):
        self.item_top_results_viewer_structural.setHidden(False)
        self.item_top_results_viewer_acoustic.setHidden(False)
        self.main_window.model_setup_widget.model_setup_items.hide_all_top_items()

    def update_items(self):
        """Enables and disables the Child Items on the menu after the solution is done."""
        self.modify_acoustic_results_viewer_items(True)
        self.modify_structural_results_viewer_items(True)

        if len(app().project.analysis_data) == 0:
            return

        analysis_setup = app().file.read_analysis_setup_from_file()
        if analysis_setup is None:
            return

        analysis_id = analysis_setup.get("analysis_id", AnalysisID.NO_ANALYSIS)
        # analysis_id = app().project.analysis_data.get("analysis_id", AnalysisID.NO_ANALYSIS)

        if analysis_id in [
            AnalysisID.STRUCTURAL_HARMONIC_DIRECT_METHOD,
            AnalysisID.STRUCTURAL_HARMONIC_MODE_SUPERPOSITION,
            AnalysisID.STRUCTURAL_MODAL,
        ]:
            self.update_structural_analysis_visibility_items()
        
        elif analysis_id in [
            AnalysisID.ACOUSTIC_HARMONIC,
            AnalysisID.ACOUSTIC_MODAL,
        ]:
            self.update_acoustic_analysis_visibility_items()
        
        elif analysis_id in [
            AnalysisID.COUPLED_HARMONIC_DIRECT_METHOD,
            AnalysisID.COUPLED_HARMONIC_MODE_SUPERPOSITION,
        ]:    
            self.update_coupled_analysis_visibility_items()

        if analysis_id in [
            AnalysisID.STRUCTURAL_HARMONIC_DIRECT_METHOD,
            AnalysisID.STRUCTURAL_HARMONIC_MODE_SUPERPOSITION,
        ]:
            self.item_child_structural_frequency_response.setDisabled(False)
            self.item_child_displacement_field.setDisabled(False)
            # self.item_child_reaction_frequency_response.setDisabled(False)
            # self.item_child_stress_field.setDisabled(False)
            # self.item_child_stress_frequency_response.setDisabled(False)
        
        elif analysis_id == AnalysisID.STRUCTURAL_MODAL:
            self.item_child_structural_mode_shapes.setDisabled(False)
        
        elif analysis_id == AnalysisID.ACOUSTIC_MODAL:
            self.item_child_acoustic_mode_shapes.setDisabled(False)
        
        elif analysis_id in [
            AnalysisID.ACOUSTIC_HARMONIC,
            AnalysisID.COUPLED_HARMONIC_DIRECT_METHOD,
            AnalysisID.COUPLED_HARMONIC_MODE_SUPERPOSITION,
        ]:

            if analysis_id != AnalysisID.ACOUSTIC_HARMONIC:
                self.item_child_displacement_field.setDisabled(False)
                self.item_child_structural_frequency_response.setDisabled(False)
                # self.item_child_stress_field.setDisabled(False)
                # self.item_child_stress_frequency_response.setDisabled(False)
                # self.item_child_reaction_frequency_response.setDisabled(False)

            self.item_child_acoustic_pressure_frequency_response.setDisabled(False)
            self.item_child_acoustic_pressure_frequency_response_function.setDisabled(False)
            self.item_child_acoustic_pressure_field.setDisabled(False)
            self.item_child_TL_NR.setDisabled(False)
            self.item_child_particle_velocity.setDisabled(False)
            self.item_child_acoustic_specific_impedance.setDisabled(False)

        self.update_tree_visibility_after_solution()
    
    def update_tree_visibility_after_solution(self):
        """ Expands and collapses the Top Level Items on 
            the menu after the solution is done.
        """
        analysis_id = app().project.analysis_data.get("analysis_id", AnalysisID.NO_ANALYSIS)

        if analysis_id in [
            AnalysisID.STRUCTURAL_HARMONIC_DIRECT_METHOD,
            AnalysisID.STRUCTURAL_HARMONIC_MODE_SUPERPOSITION,
            AnalysisID.STRUCTURAL_MODAL,
        ]:
            self.expandItem(self.item_top_results_viewer_structural)

        elif analysis_id in [
            AnalysisID.ACOUSTIC_HARMONIC,
            AnalysisID.ACOUSTIC_MODAL,
        ]:
            self.expandItem(self.item_top_results_viewer_acoustic)

        elif analysis_id in [
            AnalysisID.COUPLED_HARMONIC_DIRECT_METHOD,
            AnalysisID.COUPLED_HARMONIC_MODE_SUPERPOSITION,
        ]:
            self.expandItem(self.item_top_results_viewer_structural)
            self.expandItem(self.item_top_results_viewer_acoustic)

    def set_theme(self, theme : str):

        if theme == "dark":
            self.line_color = QColor(26,115,232,150)
            self.background_color = QColor(60,60,70)
        else:
            self.line_color = QColor(26,115,232,150)
            self.background_color = QColor(225,230,230)
    
        border_role = Qt.UserRole + 1
        border_pen = QPen(self.line_color)
        border_pen.setWidth(1)
            
        for item in self.top_level_items:
            item.setBackground(0, self.background_color)
            item.setData(0, border_role, border_pen)
