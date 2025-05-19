from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem
from PySide6.QtGui import QIcon, QFont, QPixmap, QColor, QLinearGradient, QBrush, QPen
from PySide6.QtCore import Qt, QSize, QRect
from pathlib import Path

from vibra import app
from vibra.interface.menus.common_menu_items import CommonMenuItems


class ModelSetupItems(CommonMenuItems):
    """Menu Items

    This class is responsible for creating, configuring and building the items
    in the items menu, located on the left side of the interface.

    """
    def __init__(self):
        super().__init__()

        self.project = app().project

        self._create_items()
        self._create_connections()
        self._initial_configuration()

    def _create_items(self):
        """Creates all TreeWidgetItems."""
        self.item_top_general_settings = self.add_top_item('General Settings')
        self.item_child_material = self.add_item("Material")
        self.item_child_fluid = self.add_item('Fluid')
        self.item_child_mesh_setup = self.add_item("Mesh Setup")
        self.item_child_degrees_of_freedom_decoupling = self.add_item("DOFs Decoupling")
        #
        material_tool_tip = "Attribute material to selected bodies. \ndefault material: steel (E = 210 GPa; poisson = 0.30; density = 7860 kg/m³)"
        fluid_tool_tip = "Attribute fluid to selected bodies. \ndefault fluid: air (speed of sound 343.2021 m/s; fluid density = 1.215 kg/m³)"
        self.item_child_material.setToolTip(0, material_tool_tip)
        self.item_child_fluid.setToolTip(0, fluid_tool_tip)
        #
        self.item_top_structural_model_setup = self.add_top_item('Structural Model Setup')
        self.item_child_surface_thickness = self.add_item("Surface Thickness")
        self.item_child_prescribed_dofs = self.add_item("Prescribed DOFs")
        self.item_child_nodal_loads = self.add_item("Nodal Loads")
        self.item_child_distributed_loads = self.add_item("Distributed Loads")
        self.item_child_normal_pressure_load = self.add_item("Normal Pressure Load")
        #
        self.item_top_acoustic_model_setup = self.add_top_item('Acoustic Model Setup')
        self.item_child_acoustic_pressure = self.add_item('Acoustic Pressure')
        self.item_child_mass_flow_rate = self.add_item("Mass Flow Rate")
        self.item_child_surface_velocity = self.add_item("Surface Velocity")
        self.item_child_anechoic_termination = self.add_item("Anechoic Termination")
        self.item_child_specific_impedance = self.add_item("Specific Impedance")
        self.item_child_transfer_impedance = self.add_item("Transfer Impedance")
        self.item_child_absorption_surface = self.add_item("Absorption Surface")
        self.item_child_dissipation_model = self.add_item("Dissipation Model")
        self.item_child_porous_material_model = self.add_item("Porous Material Model")
        self.item_child_viscous_thermal_model = self.add_item("Viscous-thermal Loss Model")
        self.item_child_perforated_plate_model = self.add_item("Perforated Plate Model")
        self.item_child_acoustic_properties_gradient = self.add_item("Acoustic Properties Gradient")
        self.item_child_reciprocating_compressor_excitation = self.add_item("Reciprocating Compressor Excitation")
        self.item_child_acoustic_transfer_element_setup = self.add_item("Acoustic Transfer Element Data")
        #
        self.item_child_anechoic_termination.setToolTip(0, "equivalent to the long pipe boundary condition")
        self.item_child_acoustic_properties_gradient.setHidden(True)
        #
        self.top_level_items = [
                                self.item_top_general_settings,
                                self.item_top_structural_model_setup,
                                self.item_top_acoustic_model_setup
                                ]

    def _create_connections(self):
        """
        This function iterates through all child items, connecting the items one by one
        into a function called child name + _callback, if the function exists.

        Example: If the name of the child item is item_child_material, it will be connected
        with a function called item_child_material_callback, it this function exists.
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

    def _initial_configuration(self):
        self.item_top_structural_model_setup.setHidden(True)
        self.item_top_acoustic_model_setup.setHidden(True)

        self.item_child_mesh_setup.setDisabled(True)
        self.item_child_material.setDisabled(True)
        self.item_child_fluid.setDisabled(True)

    def _find_qtree_widget_item_name(self, qtree_widet_item):
        for attr_name, attr_value in self.__dict__.items():
            if attr_value == qtree_widet_item:
                return attr_name

    # Callbacks
    def item_child_material_callback(self):
        app().main_window.input_ui.set_material()

    def item_child_fluid_callback(self):
        app().main_window.input_ui.set_fluid()

    def item_child_mesh_setup_callback(self):
        app().main_window.input_ui.mesh_setup()

    def item_child_surface_thickness_callback(self):
        app().main_window.input_ui.set_surface_thickness()

    def item_child_prescribed_dofs_callback(self):
        app().main_window.input_ui.prescribe_structural_dofs()

    def item_child_nodal_loads_callback(self):
       app().main_window.input_ui.set_nodal_loads()
    
    def item_child_distributed_loads_callback(self):
        app().main_window.input_ui.set_distributed_loads()
    
    def item_child_normal_pressure_load_callback(self):
        app().main_window.input_ui.set_normal_pressure_load()
    
    def item_child_acoustic_pressure_callback(self):
        app().main_window.input_ui.set_acoustic_pressure()
    
    def item_child_mass_flow_rate_callback(self):
        app().main_window.input_ui.set_mass_flow_rate()
    
    def item_child_surface_velocity_callback(self):
        app().main_window.input_ui.set_surface_velocity()
    
    def item_child_anechoic_termination_callback(self):
        app().main_window.input_ui.set_anechoic_termination()
    
    def item_child_specific_impedance_callback(self):
        app().main_window.input_ui.set_specific_impedance()

    def item_child_transfer_impedance_callback(self):
        app().main_window.input_ui.set_transfer_impedance()

    def item_child_absorption_surface_callback(self):
        app().main_window.input_ui.set_absorption_surface()

    def item_child_dissipation_model_callback(self):
        app().main_window.input_ui.set_dissipation_model()
    
    def item_child_porous_material_model_callback(self):
        app().main_window.input_ui.set_porous_material_model()

    def item_child_degrees_of_freedom_decoupling_callback(self):
        app().main_window.input_ui.set_degrees_of_freedom_decoupling()
    
    def item_child_viscous_thermal_model_callback(self):
        app().main_window.input_ui.set_viscous_thermal_model()

    def item_child_perforated_plate_model_callback(self):
        app().main_window.input_ui.set_perforated_plate_model()

    def item_child_reciprocating_compressor_excitation_callback(self):
        app().main_window.input_ui.add_reciprocating_compressor_excitation()
    
    def item_child_acoustic_properties_gradient_callback(self):
        app().main_window.input_ui.set_acoustic_properties_grandient()
    
    def item_child_acoustic_transfer_element_setup_callback(self):
        app().main_window.input_ui.set_acoustic_transfer_element_setup()
    
    def modify_general_settings_items_access(self, key: bool):
        imported_geometry = app().project.model.mesh.geometry_imported
        self.item_child_mesh_setup.setDisabled(not imported_geometry)
        self.item_child_material.setDisabled(key)
        self.item_child_fluid.setDisabled(key)

    def modify_structural_model_setup_items_acces(self, key: bool):
        self.item_child_surface_thickness.setDisabled(key)
        self.item_child_prescribed_dofs.setDisabled(key)
        self.item_child_nodal_loads.setDisabled(key)
        self.item_child_normal_pressure_load.setDisabled(key)
        self.item_child_distributed_loads.setDisabled(key)

    def modify_acoustic_model_setup_items_acces(self, key: bool):
        self.item_child_acoustic_pressure.setDisabled(key)
        self.item_child_mass_flow_rate.setDisabled(key)
        self.item_child_surface_velocity.setDisabled(key)
        self.item_child_specific_impedance.setDisabled(key)
        self.item_child_transfer_impedance.setDisabled(key)
        self.item_child_anechoic_termination.setDisabled(key)
        self.item_child_absorption_surface.setDisabled(key)
        self.item_child_dissipation_model.setDisabled(key)
        self.item_child_porous_material_model.setDisabled(key)
        self.item_child_viscous_thermal_model.setDisabled(key)
        self.item_child_perforated_plate_model.setDisabled(key)
        self.item_child_degrees_of_freedom_decoupling.setDisabled(key)
        self.item_child_acoustic_properties_gradient.setDisabled(key)
        self.item_child_reciprocating_compressor_excitation.setDisabled(key)
        self.item_child_acoustic_transfer_element_setup.setDisabled(key)
    
    def modify_items_access_after_geometry_importing(self):

        self.modify_general_settings_items_access(False)
        self.modify_acoustic_model_setup_items_acces(False)
        self.modify_structural_model_setup_items_acces(False)

        self.item_top_general_settings.setHidden(False)
        self.item_top_structural_model_setup.setHidden(False)
        self.item_top_acoustic_model_setup.setHidden(False)

        self.expandItem(self.item_top_general_settings)
        self.expandItem(self.item_top_structural_model_setup)
        self.expandItem(self.item_top_acoustic_model_setup)
    
    def hide_all_top_items(self):
        self.item_top_general_settings.setHidden(True)
        self.item_top_structural_model_setup.setHidden(True)
        self.item_top_acoustic_model_setup.setHidden(True)
    
    def set_theme(self, theme : str):

        if theme == "dark":
            self.line_color = QColor(107,137,185)
            self.background_color = QColor(60,60,70)

        else:
            self.line_color = QColor(107,137,185)
            self.background_color = QColor(230,230,230)

        border_role = Qt.UserRole + 1
        border_pen = QPen(self.line_color)
        border_pen.setWidth(1)
            
        for item in self.top_level_items:
            item.setBackground(0, self.background_color)
            item.setData(0, border_role, border_pen)