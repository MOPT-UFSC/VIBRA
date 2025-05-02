import re
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QTextEdit
from PySide6.QtGui import QIcon, QFont, QPixmap, QColor, QLinearGradient, QBrush, QPen
from PySide6.QtCore import Qt, QSize, QRect
from pathlib import Path

from vibra.interface.menus.tool_tips_model_setup_items import (
    material_tool_tip, fluid_tool_tip, mesh_tool_tip, surface_thickness_tool_tip,
    prescribed_dofs_tool_tip, nodal_loads_tool_tip, distributed_loads_tool_tip,
    normal_pressure_load_tool_tip, acoustic_pressure_tool_tip, surface_velocity_tool_tip,
    anechoic_termination_tool_tip, specific_impedance_tool_tip, dissipation_model_tool_tip,
    porous_material_model_tool_tip, viscous_thermal_model_tool_tip, perforated_plate_model_tool_tip,
    acoustic_properties_gradient_tool_tip, reciprocating_compressor_excitation_tool_tip,
    process_acoustic_transfer_element_data_tool_tip
)


from vibra import app, ICON_DIR

from vibra.interface.menus.common_menu_items import ChildTreeWidgetItem, CommonMenuItems
from vibra.interface.menus.border_item_delegate import BorderItemDelegate
from vibra.interface.general.print_message_input import PrintMessageInput


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
        self.update_items_icons()

    def _create_items(self):
        """Creates all TreeWidgetItems."""
        self.item_top_general_settings = self.add_top_item("General Settings")
        self.item_child_set_material = self.add_item("Set Material")
        self.item_child_set_fluid = self.add_item("Set Fluid")
        self.item_child_mesh_setup = self.add_item("Mesh Setup")
        # tool tips
        self.item_child_set_material.setToolTip(0, QTextEdit(markdown=material_tool_tip).toHtml())
        self.item_child_set_fluid.setToolTip(0, QTextEdit(markdown=fluid_tool_tip).toHtml())
        self.item_child_mesh_setup.setToolTip(0, QTextEdit(markdown=mesh_tool_tip).toHtml())

        #
        self.item_top_structural_model_setup = self.add_top_item("Structural Model Setup")
        self.item_child_set_surface_thickness = self.add_item("Set Surface Thickness")
        self.item_child_set_prescribed_dofs = self.add_item("Set Prescribed DOFs")
        self.item_child_set_nodal_loads = self.add_item("Set Nodal Loads")
        self.item_child_set_distributed_loads = self.add_item("Set Distributed Loads")
        self.item_child_set_normal_pressure_load = self.add_item("Set Normal Pressure Load")
        # tool tips
        self.item_child_set_surface_thickness.setToolTip(0, QTextEdit(markdown=surface_thickness_tool_tip).toHtml())
        self.item_child_set_prescribed_dofs.setToolTip(0, QTextEdit(markdown=prescribed_dofs_tool_tip).toHtml())
        self.item_child_set_nodal_loads.setToolTip(0, QTextEdit(markdown=nodal_loads_tool_tip).toHtml())
        self.item_child_set_distributed_loads.setToolTip(0, QTextEdit(markdown=distributed_loads_tool_tip).toHtml())
        self.item_child_set_normal_pressure_load.setToolTip(0, QTextEdit(markdown=normal_pressure_load_tool_tip).toHtml())

        self.item_top_acoustic_model_setup = self.add_top_item("Acoustic Model Setup")
        self.item_child_set_acoustic_pressure = self.add_item("Set Acoustic Pressure")
        # self.item_child_set_mass_flow_rate = self.add_item("Set Mass Flow Rate")
        self.item_child_set_surface_velocity = self.add_item("Set Surface Velocity")
        self.item_child_set_anechoic_termination = self.add_item("Set Anechoic Termination")
        self.item_child_set_specific_impedance = self.add_item("Set Specific Impedance")
        self.item_child_set_dissipation_model = self.add_item("Set Dissipation Model")
        self.item_child_set_porous_material_model = self.add_item("Set Porous Material Model")
        self.item_child_set_viscous_thermal_model = self.add_item("Set Viscous-thermal Loss Model")
        self.item_child_set_perforated_plate_model = self.add_item("Set Perforated Plate Model")
        self.item_child_set_acoustic_properties_gradient = self.add_item("Set Acoustic Properties Gradient")
        self.item_child_add_reciprocating_compressor_excitation = self.add_item("Add Reciprocating Compressor Excitation")
        self.item_child_set_acoustic_transfer_element_setup = self.add_item("Process Acoustic Transfer Element Data")
        # tool tips
        self.item_child_set_acoustic_pressure.setToolTip(0, QTextEdit(markdown=acoustic_pressure_tool_tip).toHtml())
        self.item_child_set_surface_velocity.setToolTip(0, QTextEdit(markdown=surface_velocity_tool_tip).toHtml())
        self.item_child_set_anechoic_termination.setToolTip(0, QTextEdit(markdown=anechoic_termination_tool_tip).toHtml())
        self.item_child_set_specific_impedance.setToolTip(0, QTextEdit(markdown=specific_impedance_tool_tip).toHtml())
        self.item_child_set_dissipation_model.setToolTip(0, QTextEdit(markdown=dissipation_model_tool_tip).toHtml())
        self.item_child_set_porous_material_model.setToolTip(0, QTextEdit(markdown=porous_material_model_tool_tip).toHtml())    
        self.item_child_set_viscous_thermal_model.setToolTip(0, QTextEdit(markdown=viscous_thermal_model_tool_tip).toHtml())
        self.item_child_set_perforated_plate_model.setToolTip(0, QTextEdit(markdown=perforated_plate_model_tool_tip).toHtml())
        self.item_child_set_acoustic_properties_gradient.setToolTip(0, QTextEdit(markdown=acoustic_properties_gradient_tool_tip).toHtml())
        self.item_child_add_reciprocating_compressor_excitation.setToolTip(0, QTextEdit(markdown=reciprocating_compressor_excitation_tool_tip).toHtml())
        self.item_child_set_acoustic_transfer_element_setup.setToolTip(0, QTextEdit(markdown=process_acoustic_transfer_element_data_tool_tip).toHtml())
        #
        self.item_child_set_anechoic_termination.setToolTip(0, "equivalent to the long pipe boundary condition")
        #
        self.top_level_items = [
            self.item_top_general_settings,
            self.item_top_structural_model_setup,
            self.item_top_acoustic_model_setup,
        ]

    def _create_connections(self):
        """
        This function iterates through all child items, connecting the items one by one
        into a function called child name + _callback, if the function exists.

        Example: If the name of the child item is item_child_set_material, it will be connected
        with a function called item_child_set_material_callback, it this function exists.
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
        self.item_child_set_material.setDisabled(True)
        self.item_child_set_fluid.setDisabled(True)

    def _find_qtree_widget_item_name(self, qtree_widet_item):
        for attr_name, attr_value in self.__dict__.items():
            if attr_value == qtree_widet_item:
                return attr_name
    
    def _contains_property(self, property_name):
        property = app().project.model.properties
        property_dicts = [
            property.acoustic_imported_tables,
            property.structural_imported_tables,
            property.global_properties,
            property.group_properties,
            property.volume_properties,
            property.surface_properties,
            property.line_properties,
            property.point_properties,
            property.element_properties,
            property.nodal_properties
            ]
           
        # test for mesh. Not ideal, but it works. Since the mesh config is not part of the properties, the necessary check is performed here
        if property_name == "mesh_setup":
            return app().project.model.mesh_setup is not None

        # As anechoic_termination is a subproperty of specific_impedance, 
        # we need to garantee there is a specific_impedance that is not anechoic_termination
        if property_name == "specific_impedance":
            for key, data in property.surface_properties.items():
                if key[0] == "specific_impedance":
                    if "anechoic_termination" not in data.keys():
                        return True
            return False
        
        # search for anechoic_termination in specific_impedance
        if property_name == "anechoic_termination":
            for key, data in property.surface_properties.items():
                if key[0] == "specific_impedance":
                    if "anechoic_termination" in data.keys():
                        return True
        
        # test other properties
        for dic in property_dicts:
            for key in dic.keys():
                if key[0] == property_name:
                    return True
        
        return False
    
    def update_items_icons(self):
        try:
            analysis_type = app().main_window.analysis_toolbar.combo_box_analysis_type.currentText()
            physical_domain = app().main_window.analysis_toolbar.combo_box_physical_domain.currentText()
        except Exception:
            analysis_type, physical_domain = app().project.get_analysis_type_and_physical_domain()
        
        # print(app().project.model.mesh_setup)
        
        for attr, value in self.__dict__.items():
            if isinstance(value, ChildTreeWidgetItem):
                property_name = re.match(r"item_child_(?:set_)?(.+)", attr).group(1)
                
                if property_name is None:
                    continue
                
                if self._contains_property(property_name):
                    self.set_item_icon(value, property_name)
                else:
                    if property_name == "material":
                        self.set_item_icon(value, "warning_yellow")
                        # value.setToolTip(0, QTextEdit(markdown=("**No material selected**.\n\n" + material_tool_tip)).toHtml())
                    elif property_name == "fluid":
                        self.set_item_icon(value, "warning_yellow")
                        # value.setToolTip(0, QTextEdit(markdown=("**No fluid selected**.\n\n" + fluid_tool_tip)).toHtml())
                    elif property_name == "mesh_setup":
                        self.set_item_icon(value, "warning_yellow")
                        # value.setToolTip(0, QTextEdit(markdown=("**No mesh seted**.\n\n" + mesh_tool_tip)).toHtml())
                    else:
                        value.setIcon(0, QIcon())

    def set_item_icon(self, item, image_name):
        path_image = str(Path(ICON_DIR / "model_setup_items" / str(image_name + ".png")))
        item.setIcon(0, QIcon(path_image))
        item.should_paint = False
    
    # Callbacks
    def item_child_set_material_callback(self):
        app().main_window.input_ui.set_material()

    def item_child_set_fluid_callback(self):
        app().main_window.input_ui.set_fluid()

    def item_child_mesh_setup_callback(self):
        app().main_window.input_ui.mesh_setup()

    def item_child_set_surface_thickness_callback(self):
        app().main_window.input_ui.set_surface_thickness()

    def item_child_set_prescribed_dofs_callback(self):
        app().main_window.input_ui.set_prescribed_dofs()

    def item_child_set_nodal_loads_callback(self):
        app().main_window.input_ui.set_nodal_loads()

    def item_child_set_distributed_loads_callback(self):
        app().main_window.input_ui.set_distributed_loads()

    def item_child_set_normal_pressure_load_callback(self):
        app().main_window.input_ui.set_normal_pressure_load()

    def item_child_set_acoustic_pressure_callback(self):
        app().main_window.input_ui.set_acoustic_pressure()

    def item_child_set_mass_flow_rate_callback(self):
        return
        app().main_window.input_ui.set_mass_flow_rate()

    def item_child_set_surface_velocity_callback(self):
        app().main_window.input_ui.set_surface_velocity()

    def item_child_set_anechoic_termination_callback(self):
        app().main_window.input_ui.set_anechoic_termination()

    def item_child_set_specific_impedance_callback(self):
        app().main_window.input_ui.set_specific_impedance()

    def item_child_set_dissipation_model_callback(self):
        app().main_window.input_ui.set_dissipation_model()

    def item_child_set_porous_material_model_callback(self):
        app().main_window.input_ui.set_porous_material_model()

    def item_child_set_viscous_thermal_model_callback(self):
        app().main_window.input_ui.set_viscous_thermal_model()

    def item_child_set_perforated_plate_model_callback(self):
        app().main_window.input_ui.set_perforated_plate_model()

    def item_child_add_reciprocating_compressor_excitation_callback(self):
        app().main_window.input_ui.add_reciprocating_compressor_excitation()

    def item_child_set_acoustic_properties_gradient_callback(self):
        app().main_window.input_ui.set_acoustic_properties_grandient()

    def item_child_set_acoustic_transfer_element_setup_callback(self):
        app().main_window.input_ui.set_acoustic_transfer_element_setup()

    def modify_general_settings_items_access(self, key: bool):
        self.item_child_mesh_setup.setDisabled(key)
        self.item_child_set_material.setDisabled(key)
        self.item_child_set_fluid.setDisabled(key)

    def modify_structural_model_setup_items_acces(self, key: bool):
        self.item_child_set_surface_thickness.setDisabled(key)
        self.item_child_set_prescribed_dofs.setDisabled(key)
        self.item_child_set_nodal_loads.setDisabled(key)
        self.item_child_set_normal_pressure_load.setDisabled(key)
        self.item_child_set_distributed_loads.setDisabled(key)

    def modify_acoustic_model_setup_items_acces(self, key: bool):
        self.item_child_set_acoustic_pressure.setDisabled(key)
        # self.item_child_set_mass_flow_rate.setDisabled(key)
        self.item_child_set_surface_velocity.setDisabled(key)
        self.item_child_set_specific_impedance.setDisabled(key)
        self.item_child_set_anechoic_termination.setDisabled(key)
        self.item_child_set_dissipation_model.setDisabled(key)
        self.item_child_set_porous_material_model.setDisabled(key)
        self.item_child_set_viscous_thermal_model.setDisabled(key)
        self.item_child_set_perforated_plate_model.setDisabled(key)
        self.item_child_set_acoustic_properties_gradient.setDisabled(key)
        self.item_child_add_reciprocating_compressor_excitation.setDisabled(key)
        self.item_child_set_acoustic_transfer_element_setup.setDisabled(key)

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

    def set_theme(self, theme: str):
        if theme == "dark":
            self.line_color = QColor(107, 137, 185)
            self.background_color = QColor(60, 60, 70)

        else:
            self.line_color = QColor(107, 137, 185)
            self.background_color = QColor(230, 230, 230)

        border_role = Qt.UserRole + 1
        border_pen = QPen(self.line_color)
        border_pen.setWidth(1)

        for item in self.top_level_items:
            item.setBackground(0, self.background_color)
            item.setData(0, border_role, border_pen)
