from PySide6.QtGui import QPen, QColor
from PySide6.QtCore import Qt

from vibra import app
from vibra.interface.menus.common_menu_items import CommonMenuItems

from molde import Color

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
        self.update_items_appearance()

    def _create_items(self):
        """Creates all TreeWidgetItems."""
        self.item_top_general_settings = self.add_top_item('General Settings')
        self.item_child_material = self.add_item("Material")
        self.item_child_fluid = self.add_item('Fluid')
        self.item_child_mesh_setup = self.add_item("Mesh Setup")
        self.item_child_degrees_of_freedom_decoupling = self.add_item("DOFs Decoupling")

        self.item_top_structural_model_setup = self.add_top_item('Structural Model Setup')
        self.item_child_surface_thickness = self.add_item("Surface Thickness")
        self.item_child_prescribed_dofs = self.add_item("Prescribed DOFs")
        self.item_child_nodal_loads = self.add_item("Nodal Loads")
        self.item_child_distributed_loads = self.add_item("Distributed Loads")
        self.item_child_normal_pressure_load = self.add_item("Normal Pressure Load")
    
        self.item_top_acoustic_model_setup = self.add_top_item('Acoustic Model Setup')
        self.item_child_acoustic_pressure = self.add_item('Acoustic Pressure')
        self.item_child_mass_flow_rate = self.add_item("Mass Flow Rate")
        self.item_child_surface_velocity = self.add_item("Surface Velocity")
        self.item_child_incident_plane_wave = self.add_item("Incident Plane Wave")
        self.item_child_anechoic_termination = self.add_item("Anechoic Termination")
        self.item_child_absorption_surface = self.add_item("Absorption Surface")
        self.item_child_specific_impedance = self.add_item("Specific Impedance")
        self.item_child_transfer_impedance = self.add_item("Transfer Impedance")
        self.item_child_perforated_plate_model = self.add_item("Perforated Plate Model")
        self.item_child_proportional_damping = self.add_item("Proportional Damping")
        self.item_child_porous_material_model = self.add_item("Porous Material Model")
        self.item_child_viscous_thermal_model = self.add_item("Viscous-thermal Loss Model")
        self.item_child_acoustic_properties_gradient = self.add_item("Acoustic Properties Gradient")
        self.item_child_reciprocating_compressor_excitation = self.add_item("Reciprocating Compressor Excitation")
        self.item_child_acoustic_transfer_element_setup = self.add_item("Acoustic Transfer Element Data")
        
        self.item_child_anechoic_termination.setToolTip(0, "equivalent to the long pipe boundary condition")
        self.item_child_acoustic_properties_gradient.setHidden(True)
        
        self.top_level_items = [
            self.item_top_general_settings,
            self.item_top_structural_model_setup,
            self.item_top_acoustic_model_setup,
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
            property.nodal_properties,
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
        for property_dict in property_dicts:
            for key in property_dict.keys():
                if key[0] == property_name:
                    if property_name == "degrees_of_freedom_decoupling":
                        pp_data = app().project.model.properties._get_property("perforated_plate_model", surface=key[1])
                        if isinstance(pp_data, dict):
                            continue

                    return True
        
        return False

    def _needs_property(self, property_name, analysis_type=None, physical_domain=None):
        if property_name == "mesh_setup":
            return True
        
        if property_name == "material":
            return physical_domain == "structural"
        
        if property_name == "fluid":
            return physical_domain == "acoustic"
        
        # if property_name == "nodal_loads":
        #     return analysis_type == "harmonic" and physical_domain == "structural"
        
        # if property_name == "surface_velocity":
        #     return analysis_type == "harmonic" and physical_domain == "acoustic"
        
        return False
    
    def update_items_appearance(self):
        # It may happen that the analysis toolbar has not been created yet. If so, retrieve the analysis type and physical domain from the project
        try:
            analysis_type = app().main_window.analysis_toolbar.combo_box_analysis_type.currentText()
            physical_domain = app().main_window.analysis_toolbar.combo_box_physical_domain.currentText()
        except Exception:
            analysis_type, physical_domain = app().project.get_analysis_type_and_physical_domain()
        
        analysis_type = analysis_type.lower()
        physical_domain = physical_domain.lower()
        
        for top_level_items in self.top_level_items:
            for index in range(top_level_items.childCount()):
                item_child = top_level_items.child(index)
                item_child_name = self._find_qtree_widget_item_name(item_child)

                if item_child_name is None:
                    continue

                # just to make sure the name is correct (there was a bug in the previous versions)
                item_child.set_property_name(item_child_name)

                item_child.set_warning(False)
                item_child.set_tool_tip()
                
                if item_child.isDisabled():
                    continue
                
                if self._contains_property(item_child.property_name):
                    item_child.set_icon()
                    
                elif self._needs_property(item_child.property_name, analysis_type, physical_domain):
                    item_child.set_warning(True)
                    item_child.set_tool_tip(requirement=True)

                else:
                    item_child.set_icon(visible=False)

    def reset_items_appearance(self):
        for top_level_items in self.top_level_items:
            for index in range(top_level_items.childCount()):
                item_child = top_level_items.child(index)
                item_child.set_icon(visible=False)
                item_child.set_warning(False)
                item_child.set_tool_tip()
    
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

    def item_child_incident_plane_wave_callback(self):
        app().main_window.input_ui.set_incident_plane_wave()
    
    def item_child_anechoic_termination_callback(self):
        app().main_window.input_ui.set_anechoic_termination()
    
    def item_child_specific_impedance_callback(self):
        app().main_window.input_ui.set_specific_impedance()

    def item_child_transfer_impedance_callback(self):
        app().main_window.input_ui.set_transfer_impedance()

    def item_child_absorption_surface_callback(self):
        app().main_window.input_ui.set_absorption_surface()

    def item_child_proportional_damping_callback(self):
        app().main_window.input_ui.set_proportional_damping_for_acoustic_model()
    
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
        self.item_child_incident_plane_wave.setDisabled(key)
        self.item_child_specific_impedance.setDisabled(key)
        self.item_child_anechoic_termination.setDisabled(key)
        self.item_child_absorption_surface.setDisabled(key)
        self.item_child_transfer_impedance.setDisabled(key)
        self.item_child_proportional_damping.setDisabled(key)
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

    def set_theme(self, theme: str):
        if theme == "dark":
            self.line_color = Color(107, 137, 185).to_qt()
            self.background_color = Color(60, 60, 70).to_qt()

        else:
            self.line_color = Color(107, 137, 185).to_qt()
            self.background_color = Color(230, 230, 230).to_qt()

        border_role = Qt.UserRole + 1
        border_pen = QPen(self.line_color)
        border_pen.setWidth(1)

        for item in self.top_level_items:
            item.setBackground(0, self.background_color)
            item.setData(0, border_role, border_pen)
