from molde import Color
from PySide6.QtCore import Qt
from PySide6.QtGui import QPen

from vibra import app
from vibra.engine import AnalysisID
from vibra.interface.menus.common_menu_items import ChildTreeWidgetItem, CommonMenuItems


class ResultsViewerItems(CommonMenuItems):
    """Menu Items

    This class is responsible for creating, configuring and building the items
    in the items menu, located on the left side of the interface.

    """
    def __init__(self):
        super().__init__()

        self.project = app().project

        self.setObjectName("results_viewer_items")
        self._create_items()
        self._create_connections()

    def _create_items(self):

        ## Structural results items
        self.item_top_results_viewer_structural = self.add_top_item("Results Viewer - Structural")
        self.item_child_structural_mode_shapes = self.add_item("Plot Structural Mode Shapes")
        self.item_child_structural_results_fields = self.add_item("Structural Results Fields")
        self.item_child_structural_frequency_response = self.add_item("Plot Structural Frequency Response")
        # self.item_child_reaction_frequency_response = self.add_item("Plot Reactions Frequency Response")
        # self.item_child_stress_field = self.add_item("Plot Stress Field")
        # self.item_child_stress_frequency_response = self.add_item("Plot Stress Frequency Response")

        ## Acoustic results items
        self.item_top_results_viewer_acoustic = self.add_top_item("Results Viewer - Acoustic")
        self.item_child_acoustic_mode_shapes = self.add_item("Acoustic Mode Shapes")
        self.item_child_acoustic_pressure_field = self.add_item("Acoustic Pressure Field")
        self.item_child_acoustic_pressure_waveform_field = self.add_item("Acoustic Pressure Waveform Field")
        self.item_child_acoustic_pressure_waveform = self.add_item("Acoustic Pressure Waveform")
        self.item_child_acoustic_pressure_frequency_response = self.add_item("Acoustic Pressure Frequency Response")
        self.item_child_acoustic_pressure_frf = self.add_item("Acoustic Presssure FRF")
        self.item_child_allowable_pulsations_for_reciprocating_compressor = self.add_item("Allowable Pulsation (Reciprocating Compressor)")
        self.item_child_allowable_pulsations_for_screw_compressor = self.add_item("Allowable Pulsation (Screw Compressor)")
        self.item_child_TL_NR = self.add_item("Transmission Loss or Attenuation")
        self.item_child_particle_velocity = self.add_item("Particle Velocity")
        self.item_child_acoustic_impedance = self.add_item("Acoustic Impedance")
        self.item_child_absorption_coefficient = self.add_item("Absorption Coefficient")
        self.item_child_decompose_acoustic_waves = self.add_item("Decompose Acoustic Waves")

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
        self.item_child_acoustic_pressure_field.setDisabled(key)
        self.item_child_acoustic_pressure_frequency_response.setDisabled(key)
        self.item_child_acoustic_pressure_frf.setDisabled(key)
        self.item_child_decompose_acoustic_waves.setDisabled(key)
        self.item_child_allowable_pulsations_for_reciprocating_compressor.setDisabled(key)
        self.item_child_allowable_pulsations_for_screw_compressor.setDisabled(key)
        self.item_child_TL_NR.setDisabled(key)
        self.item_child_particle_velocity.setDisabled(key)
        self.item_child_acoustic_impedance.setDisabled(key)
        self.item_child_absorption_coefficient.setDisabled(key)

        if AnalysisID(app().project.model.analysis_id).is_modal():
            self.item_child_acoustic_pressure_waveform.setHidden(True)
            self.item_child_acoustic_pressure_waveform_field.setHidden(True)

        elif app().project.model.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            # only allow waveform plots for equally distributed solution steps 
            # with a compressor as the main excitation source
            cond_A = self.project.model.has_spectral_content_been_modified()
            cond_B = not self.project.model.is_there_a_compressor_excitation_in_model()
            self.item_child_acoustic_pressure_waveform.setHidden(cond_A or cond_B)
            self.item_child_acoustic_pressure_waveform_field.setHidden(cond_A or cond_B)

    def modify_structural_results_viewer_items(self, key: bool):
        self.item_top_results_viewer_structural.setHidden(key)
        self.item_child_structural_results_fields.setDisabled(key)
        self.item_child_structural_frequency_response.setDisabled(key)
        # self.item_child_reaction_frequency_response.setDisabled(key)
        # self.item_child_stress_field.setDisabled(key)
        self.item_child_structural_mode_shapes.setDisabled(key)
    
    def update_structural_analysis_visibility_items(self):
        self.item_top_results_viewer_structural.setHidden(False)
        self.item_top_results_viewer_acoustic.setHidden(True)

    def update_acoustic_analysis_visibility_items(self):
        self.item_top_results_viewer_acoustic.setHidden(False)
        self.item_top_results_viewer_structural.setHidden(True)

    def update_coupled_analysis_visibility_items(self):
        self.item_top_results_viewer_structural.setHidden(False)
        self.item_top_results_viewer_acoustic.setHidden(False)

    def update_items(self):
        """
        Enables and disables the Child Items on the menu after the solution is done.
        """
        self.modify_acoustic_results_viewer_items(True)
        self.modify_structural_results_viewer_items(True)

        analysis_id = app().project.model.analysis_id
        if analysis_id == AnalysisID.NO_ANALYSIS:
            return

        if analysis_id.is_structural():
            self.update_structural_analysis_visibility_items()

        elif analysis_id.is_acoustic():
            self.update_acoustic_analysis_visibility_items()

        elif analysis_id.is_coupled():    
            self.update_coupled_analysis_visibility_items()

        if analysis_id == AnalysisID.STRUCTURAL_HARMONIC:
            self.item_child_structural_frequency_response.setDisabled(False)
            self.item_child_structural_results_fields.setDisabled(False)
            # self.item_child_reaction_frequency_response.setDisabled(False)
            # self.item_child_stress_field.setDisabled(False)
            # self.item_child_stress_frequency_response.setDisabled(False)
        
        elif analysis_id == AnalysisID.STRUCTURAL_MODAL:
            self.item_child_structural_mode_shapes.setDisabled(False)
        
        elif analysis_id == AnalysisID.ACOUSTIC_MODAL:
            self.item_child_acoustic_mode_shapes.setDisabled(False)
        
        elif analysis_id in [AnalysisID.ACOUSTIC_HARMONIC, AnalysisID.COUPLED_HARMONIC]:
            if analysis_id == AnalysisID.COUPLED_HARMONIC:
                self.item_child_structural_results_fields.setDisabled(False)
                self.item_child_structural_frequency_response.setDisabled(False)
                # self.item_child_stress_field.setDisabled(False)
                # self.item_child_stress_frequency_response.setDisabled(False)
                # self.item_child_reaction_frequency_response.setDisabled(False)

            self.item_child_acoustic_pressure_field.setDisabled(False)
            self.item_child_acoustic_pressure_frequency_response.setDisabled(False)
            self.item_child_acoustic_pressure_frf.setDisabled(False)
            self.item_child_decompose_acoustic_waves.setDisabled(False)
            self.item_child_allowable_pulsations_for_reciprocating_compressor.setDisabled(False)
            self.item_child_allowable_pulsations_for_screw_compressor.setDisabled(False)
            self.item_child_acoustic_pressure_waveform.setDisabled(False)
            self.item_child_acoustic_pressure_waveform_field.setDisabled(False)
            self.item_child_TL_NR.setDisabled(False)
            self.item_child_particle_velocity.setDisabled(False)
            self.item_child_acoustic_impedance.setDisabled(False)
            self.item_child_absorption_coefficient.setDisabled(False)

        self.update_allowable_pulsation_criteria_visibility_for_reciprocating_compressor(analysis_id)
        self.update_allowable_pulsation_criteria_visibility_for_screw_compressor(analysis_id)
        self.update_tree_visibility_after_solution()
        self.update_results_items_warnings()

    def update_allowable_pulsation_criteria_visibility_for_reciprocating_compressor(self, analysis_id: int):
        compressor_exists = False
        if analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            compressor_exists = app().project.model.is_the_property_present_in_model("reciprocating_compressor_excitation", "surfaces")

        self.item_child_allowable_pulsations_for_reciprocating_compressor.setHidden(not compressor_exists)

    def update_allowable_pulsation_criteria_visibility_for_screw_compressor(self, analysis_id: int):
        compressor_exists = False
        if analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            for (prop_label, *args), prop_data in app().project.model.properties.surface_properties.items():
                if prop_label in ["compressor_excitation_spectrum", "compressor_excitation_waveform"]:
                    compressor_type = prop_data.get("compressor_type")
                    if compressor_type == "screw":
                        compressor_exists = True
                        break

        self.item_child_allowable_pulsations_for_screw_compressor.setHidden(not compressor_exists)

    def update_tree_visibility_after_solution(self):
        """ Expands and collapses the Top Level Items on 
            the menu after the solution is done.
        """
        analysis_id = app().project.model.analysis_id

        if analysis_id in [AnalysisID.STRUCTURAL_HARMONIC, AnalysisID.STRUCTURAL_MODAL]:
            self.expandItem(self.item_top_results_viewer_structural)

        elif analysis_id in [AnalysisID.ACOUSTIC_HARMONIC, AnalysisID.ACOUSTIC_MODAL]:
            self.expandItem(self.item_top_results_viewer_acoustic)

        elif analysis_id in [AnalysisID.COUPLED_HARMONIC]:
            self.expandItem(self.item_top_results_viewer_structural)
            self.expandItem(self.item_top_results_viewer_acoustic)

    def set_theme(self, theme : str):

        if theme == "dark":
            self.line_color = Color(26,115,232,150).to_qt()
            self.background_color = Color(60,60,70).to_qt()
        else:
            self.line_color = Color(26,115,232,150).to_qt()
            self.background_color = Color(225,230,230).to_qt()
    
        border_role = Qt.UserRole + 1
        border_pen = QPen(self.line_color)
        border_pen.setWidth(1)
            
        for item in self.top_level_items:
            item.setBackground(0, self.background_color)
            item.setData(0, border_role, border_pen)

    def update_results_items_warnings(self):

        # check if the current solution is outdated
        warning = app().project.model.outdated_solution

        for top_level_item in self.top_level_items:
            top_level_item.set_warning(warning)
            for index in range(top_level_item.childCount()):

                item_child: ChildTreeWidgetItem = top_level_item.child(index)
                if item_child.isDisabled():
                    item_child.setToolTip(0, "")
                    item_child.set_warning(False)
                    continue

                tool_tip = ""
                if warning:
                    tool_tip = "<b style='color:red'>The solution is outdated because the model configuration does not match that of the current solution.</b>"

                item_child.set_warning(warning, update_item_color=False)
                item_child.setToolTip(0, tool_tip)