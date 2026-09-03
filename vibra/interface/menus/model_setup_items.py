
from molde import Color
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPen

from vibra import DEVELOPER_MODE, ICON_DIR, app
from vibra.interface.menus.common_menu_items import ChildTreeWidgetItem, CommonMenuItems


class ModelSetupItems(CommonMenuItems):
    """Menu Items

    This class is responsible for creating, configuring and building the items
    in the items menu, located on the left side of the interface.

    """

    def __init__(self):
        super().__init__()

        self._create_items()
        self._create_connections()
        self._initial_configuration()
        self._filter_visible_items_based_on_current_mode()
        self.update_items_appearance()
    
    def _create_items(self):
        """Creates all TreeWidgetItems."""
        self.item_top_general_settings = self.add_top_item('General Settings')
        self.item_child_material = self.add_item("Material")
        self.item_child_fluid = self.add_item('Fluid')
        self.item_child_mesh_setup = self.add_item("Mesh Setup")
        self.item_child_element_options = self.add_item("Element Options")
        self.item_child_degrees_of_freedom_decoupling = self.add_item("DOF Decoupling")

        self.item_top_structural_model_setup = self.add_top_item('Structural Model Setup (Beta)')

        tooltip_html = '''
                        <p><b>Structural Properties</b></p>
                        <p><span style="color:red;">
                        <b>Note:</b> The calculations for these structural properties are currently undergoing refinement.</span> 
                        While we are actively working to ensure complete accuracy, please be aware that simulation results may 
                        exhibit minor variations. We appreciate your understanding as we continue to improve the precision of our models.</p>
                        '''
        self.item_top_structural_model_setup.setToolTip(0, tooltip_html)
        path_image = str(ICON_DIR / "model_setup_items/structural_help.png")
        self.item_top_structural_model_setup.setIcon(0, QIcon(path_image))

        self.item_child_surface_thickness = self.add_item("Surface Thickness")
        self.item_child_prescribed_dof = self.add_item("Prescribed DOF")
        self.item_child_nodal_loads = self.add_item("Nodal Loads")
        self.item_child_distributed_loads = self.add_item("Distributed Loads")
        self.item_child_normal_pressure_load = self.add_item("Normal Pressure Load")
        self.item_child_distributed_mass = self.add_item("Distributed Mass")
    
        self.item_top_acoustic_model_setup = self.add_top_item('Acoustic Model Setup')

        # acoustic model excitations
        self.item_child_acoustic_pressure = self.add_item('Acoustic Pressure')
        self.item_child_mass_source = self.add_item("Mass Source")
        self.item_child_surface_velocity = self.add_item("Surface Velocity")
        self.item_child_incident_plane_wave = self.add_item("Incident Plane Wave")
        self.item_child_compressor_excitation_spectrum = self.add_item("Compressor Excitation (spectrum)")
        self.item_child_compressor_excitation_waveform = self.add_item("Compressor Excitation (waveform)")
        self.item_child_reciprocating_compressor_excitation = self.add_item("Reciprocating Compressor Excitation")

        # external impedances
        self.item_child_anechoic_termination = self.add_item("Anechoic Termination")
        self.item_child_specific_impedance = self.add_item("Specific Impedance")
        self.item_child_absorption_surface = self.add_item("Absorption Surface")
        self.item_child_anechoic_termination.setToolTip(0, "equivalent to the long pipe boundary condition")

        # internal impedances
        self.item_child_transfer_impedance = self.add_item("Transfer Impedance")
        self.item_child_perforated_plate_model = self.add_item("Perforated Plate Model")

        # dissipation models
        self.item_child_proportional_damping = self.add_item("Proportional Damping")
        self.item_child_porous_material_model = self.add_item("Porous Material Model")
        self.item_child_viscous_thermal_model = self.add_item("Viscous-thermal Loss Model")

        # other features
        self.item_child_acoustic_properties_gradient = self.add_item("Acoustic Properties Gradient")
        self.item_child_acoustic_transfer_element_setup = self.add_item("Acoustic Transfer Element Data")

        # self.item_child_acoustic_properties_gradient.setHidden(True)
        # self.item_child_compressor_excitation_spectrum.setHidden(True)

        self.top_level_items = [
            self.item_top_general_settings,
            self.item_top_structural_model_setup,
            self.item_top_acoustic_model_setup,
        ]
        
        # correlate each menu item with the name of the related property.
        self.property_names = {
            "item_child_material": "material",
            "item_child_fluid": "fluid",
            "item_child_mesh_setup": "mesh_setup",
            "item_child_element_options": "element_options",
            "item_child_degrees_of_freedom_decoupling": "degrees_of_freedom_decoupling",
            "item_child_surface_thickness": "surface_thickness",
            "item_child_prescribed_dof": "prescribed_dof",
            "item_child_nodal_loads": "nodal_loads",
            "item_child_distributed_loads": "distributed_loads",
            "item_child_normal_pressure_load": "normal_pressure_load",
            "item_child_distributed_mass": "distributed_mass",
            "item_child_acoustic_pressure": "acoustic_pressure",
            "item_child_mass_source": "mass_source",
            "item_child_surface_velocity": "surface_velocity",
            "item_child_incident_plane_wave": "incident_plane_wave",
            "item_child_anechoic_termination": "anechoic_termination",
            "item_child_absorption_surface": "absorption_surface",
            "item_child_specific_impedance": "specific_impedance",
            "item_child_transfer_impedance": "transfer_impedance",
            "item_child_perforated_plate_model": "perforated_plate_model",
            "item_child_proportional_damping": "proportional_damping",
            "item_child_porous_material_model": "porous_material_model",
            "item_child_viscous_thermal_model": "viscous_thermal_model",
            "item_child_acoustic_properties_gradient": "acoustic_properties_gradient",
            "item_child_reciprocating_compressor_excitation": "reciprocating_compressor_excitation",
            "item_child_compressor_excitation_waveform": "compressor_excitation_waveform",
            "item_child_compressor_excitation_spectrum": "compressor_excitation_spectrum",
            "item_child_acoustic_transfer_element_setup": "acoustic_transfer_element_setup",
        }

    def _create_connections(self):
        """
        This function iterates through all child items, connecting the items one by one
        into a function called child name + _callback, if the function exists.

        Example: If the name of the child item is item_child_material, it will be connected
        with a function called item_child_material_callback, it this function exists.
        """

        for top_level_items in self.top_level_items:
            for index in range(top_level_items.childCount()):
                item_child: ChildTreeWidgetItem = top_level_items.child(index)
                item_child_name = self._find_qtree_widget_item_name(item_child)

                if item_child_name is None:
                    continue

                property_name = self.property_names.get(item_child_name)
                if property_name is None:
                    continue

                item_child.set_property_name(property_name)

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

    def _filter_visible_items_based_on_current_mode(self):
        # self.item_child_incident_plane_wave.setHidden(not DEVELOPER_MODE)
        self.item_child_acoustic_properties_gradient.setHidden(not DEVELOPER_MODE)
        self.item_child_acoustic_transfer_element_setup.setHidden(not DEVELOPER_MODE)

        # TODO: remove when possible
        # self.item_child_incident_plane_wave.setHidden(True)
        self.item_child_acoustic_properties_gradient.setHidden(True)

    def _find_qtree_widget_item_name(self, qtree_widet_item) -> str | None:
        for attr_name, attr_value in self.__dict__.items():
            if attr_value == qtree_widet_item:
                return attr_name
    
    def _contains_property(self, property_name: str) -> bool:

        model = app().project.model
        mesh = app().project.model.mesh
        properties = app().project.model.properties

        property_dicts = [
            properties.acoustic_imported_tables,
            properties.structural_imported_tables,
            properties.global_properties,
            properties.group_properties,
            properties.volume_properties,
            properties.surface_properties,
            properties.line_properties,
            properties.point_properties,
            properties.element_properties,
            properties.nodal_properties,
        ]

        if property_name == "material":
            if mesh.are_there_volumes_in_geometry():
                volume_ids = mesh.geometry_information.get("volumes")
                volume_ids.sort()
                volumes_without_material = properties.get_entities_without_property("material", volumes=volume_ids)
                if volumes_without_material:
                    acoustic_volumes = model.model_domains.get("acoustic", [])
                    if volumes_without_material == volume_ids:
                        return False

                    for vol_id in volumes_without_material:
                        if vol_id not in acoustic_volumes:
                            return False

                return True

            else:
                surface_ids = mesh.geometry_information.get("surfaces")
                surfaces_without_material = properties.get_entities_without_property("material", surfaces=surface_ids)
                return not bool(len(surfaces_without_material))

        if property_name == "fluid":
            if mesh.are_there_volumes_in_geometry():
                volume_ids = mesh.geometry_information.get("volumes")
                volume_ids.sort()
                volumes_without_fluid = properties.get_entities_without_property("fluid", volumes=volume_ids)
                if volumes_without_fluid:
                    structural_volumes = model.model_domains.get("structural", [])
                    if volumes_without_fluid == volume_ids:
                        return False

                    for vol_id in volumes_without_fluid:
                        if vol_id not in structural_volumes:
                            return False

                return True
            # else:
            #     surface_ids = mesh.geometry_information.get("surfaces")
            #     surfaces_without_fluid = properties.get_entities_without_property("fluid", surfaces=surface_ids)
            #     return not bool(len(surfaces_without_fluid))

        # test for mesh. Not ideal, but it works. Since the mesh config is not part of the properties, the necessary check is performed here
        if property_name == "mesh_setup":
            disconnected_nodes = bool(mesh.disconnected_nodes_data)
            collapsed_elements = bool(mesh.collapsed_elements_data)
            if collapsed_elements or disconnected_nodes:
                return False

            return model.mesh_setup is not None

        # verify if there are surface thickness in all surfaces before changing the icon
        if property_name == "surface_thickness":
            if mesh is not None:
                st_check = model.is_surface_thickness_properly_applied_in_model()
                if isinstance(st_check, list) and st_check:
                    return not st_check

        # As anechoic_termination is a subproperty of specific_impedance, 
        # we need to garantee there is a specific_impedance that is not anechoic_termination
        if property_name == "specific_impedance":
            for key, data in properties.surface_properties.items():
                if key[0] == "specific_impedance":
                    if "anechoic_termination" not in data.keys():
                        return True
            return False
        
        # search for anechoic_termination in specific_impedance
        if property_name == "anechoic_termination":
            for key, data in properties.surface_properties.items():
                if key[0] == "specific_impedance":
                    if "anechoic_termination" in data.keys():
                        return True

        # test other properties
        for property_dict in property_dicts:
            for key in property_dict.keys():
                if key[0] == property_name:
                    if property_name == "degrees_of_freedom_decoupling":
                        pp_data = properties._get_property("perforated_plate_model", surface=key[1])
                        if isinstance(pp_data, dict):
                            continue

                        ti_data = properties._get_property("transfer_impedance", surface=key[1])
                        if isinstance(ti_data, dict):
                            continue

                    return True

        return False

    def _needs_property(self, property_name: str, analysis_type: str | None = None, physical_domain: str | None = None) -> bool:
        if property_name == "mesh_setup":
            return True

        if property_name == "material":
            return physical_domain == "structural"

        if property_name == "fluid":
            return physical_domain == "acoustic"

        if property_name == "surface_thickness":
            if physical_domain == "structural":
                if app().project.model.mesh is not None:
                    volume_exists = app().project.model.mesh.are_there_volumes_in_geometry()
                    if not volume_exists:
                        return True

                    st_check = app().project.model.is_surface_thickness_properly_applied_in_model()
                    if isinstance(st_check, list) and st_check:
                        return True

        return False
    
    def filter_available_items_and_analyzes_according_to_geometry_information(self):
        """
        This method filters the available analyzes and items according to the geometry information.
        If there are no volumes in geometry, the physical domain comboBox will be switched and disabled 
        in structural type because there is no implementation for 2D acoustic models.
        """

        volume_exists = None
        mesh = app().project.model.mesh
        toolbar = app().main_window.analysis_toolbar

        if mesh is not None:
            volume_exists = mesh.are_there_volumes_in_geometry()
            self.item_child_surface_thickness.setHidden(volume_exists)
            # self.item_child_distributed_loads.setHidden(volume_exists)
            # self.item_child_normal_pressure_load.setHidden(volume_exists)

        if isinstance(volume_exists, bool):
            toolbar.combo_box_physical_domain.setEnabled(volume_exists)
            if not volume_exists:
                toolbar.combo_box_physical_domain.setCurrentIndex(0)
                return

        if app().project.get_physical_domain() == "":
            toolbar.combo_box_physical_domain.setCurrentIndex(1)
            toolbar.check_analysis_setup_callback()
        else:
            toolbar.update_analysis_combo_boxes(block_signals=True)

    def filter_items_according_to_analysis(self, analysis_type: str, physical_domain: str):
        """
        This method filters the available items according to the analysis type and physical domain.

        Parameters:
        -----------
        analysis_type: str
        It represents the analysis type (harmonic or modal).  

        physical_domain: str
        It represents the physical domain (structural or acoustic).
        """

        self.item_top_general_settings.setHidden(False)

        if physical_domain == "acoustic":
            self.item_child_fluid.setHidden(False)
            self.item_child_material.setHidden(True)
            self.item_top_acoustic_model_setup.setHidden(False)
            self.item_top_structural_model_setup.setHidden(True)

        elif physical_domain == "structural":
            self.item_child_fluid.setHidden(True)
            self.item_child_material.setHidden(False)
            self.item_top_acoustic_model_setup.setHidden(True)
            self.item_top_structural_model_setup.setHidden(False)

        elif physical_domain == "coupled":
            self.item_child_fluid.setHidden(False)
            self.item_child_material.setHidden(False)
            self.item_top_acoustic_model_setup.setHidden(False)
            self.item_top_structural_model_setup.setHidden(False)

    def _are_there_collapsed_elements(self, item_child) -> bool:
        if item_child.property_name == "mesh_setup":
            mesh = app().project.model.mesh
            if mesh is not None:
                collapsed_elements = bool(mesh.collapsed_elements_data)
                item_child.set_error(collapsed_elements)
                if collapsed_elements:
                    return True
        return False

    def _are_there_disconnected_nodes(self, item_child):
        if item_child.property_name == "mesh_setup":
            mesh = app().project.model.mesh
            if mesh is not None:
                disconnected_nodes = bool(mesh.disconnected_nodes_data)
                item_child.set_error(disconnected_nodes)
                if disconnected_nodes:
                    return True
        return False

    def update_items_appearance(self):

        # It may happen that the analysis toolbar has not been created yet. If so, 
        # retrieve the analysis type and physical domain from the project
        try:
            analysis_type = app().main_window.analysis_toolbar.combo_box_analysis_type.currentText()
            physical_domain = app().main_window.analysis_toolbar.combo_box_physical_domain.currentText()
        except Exception:
            analysis_type = app().project.get_analysis_type()
            physical_domain = app().project.get_physical_domain()

        analysis_type = analysis_type.lower()
        physical_domain = physical_domain.lower()
        self.filter_items_according_to_analysis(analysis_type, physical_domain)

        if app().project.model.mesh is None:
            return

        for top_level_items in self.top_level_items:

            for index in range(top_level_items.childCount()):
                item_child: ChildTreeWidgetItem = top_level_items.child(index)
                item_child_name = self._find_qtree_widget_item_name(item_child)

                if item_child_name is None:
                    continue

                item_child.set_warning(False)
                item_child.set_tool_tip(item_child.property_name)
                
                if item_child.isDisabled():
                    continue

                if self._are_there_collapsed_elements(item_child):
                    continue
                    
                if self._are_there_disconnected_nodes(item_child):
                    continue

                if self._contains_property(item_child.property_name):
                    item_child.set_icon()

                    # special treatment for compressors
                    if item_child.property_name == "compressor_excitation_waveform":
                        surface_properties = app().project.model.properties.surface_properties
                        for key in surface_properties.items():
                            if key[0][0] == "compressor_excitation_waveform":
                                # compressor_type = property_data.get("compressor_type", "reciprocating")
                                compressor_type = key[1].get("compressor_type")
                                if compressor_type == "screw":
                                    item_child.set_icon("screw_compressor")
                                elif compressor_type == "reciprocating":
                                    item_child.set_icon("reciprocating_compressor_excitation")
                                else:
                                    item_child.set_icon("other_compressor")
                    
                    if item_child.property_name == "compressor_excitation_spectrum":
                        surface_properties = app().project.model.properties.surface_properties
                        for key in surface_properties.items():
                            if key[0][0] == "compressor_excitation_spectrum":
                                # compressor_type = property_data.get("compressor_type", "reciprocating")
                                compressor_type = key[1].get("compressor_type")
                                if compressor_type == "screw":
                                    item_child.set_icon("screw_compressor")
                                elif compressor_type == "reciprocating":
                                    item_child.set_icon("reciprocating_compressor_excitation")
                                else:
                                    item_child.set_icon("other_compressor")

                elif self._needs_property(item_child.property_name, analysis_type, physical_domain):
                    item_child.set_warning(True)
                    item_child.set_tool_tip(item_child.property_name, requirement=True)

                else:
                    item_child.set_icon(visible=False)

    def reset_items_appearance(self):
        for top_level_items in self.top_level_items:
            for index in range(top_level_items.childCount()):
                item_child: ChildTreeWidgetItem = top_level_items.child(index)
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

    def item_child_element_options_callback(self):
        app().main_window.input_ui.advanced_element_options()

    def item_child_surface_thickness_callback(self):
        app().main_window.input_ui.set_surface_thickness()

    def item_child_prescribed_dof_callback(self):
        app().main_window.input_ui.prescribe_structural_dof()

    def item_child_nodal_loads_callback(self):
       app().main_window.input_ui.set_nodal_loads()
    
    def item_child_distributed_loads_callback(self):
        app().main_window.input_ui.set_distributed_loads()

    def item_child_distributed_mass_callback(self):
        app().main_window.input_ui.set_distributed_mass()
    
    def item_child_normal_pressure_load_callback(self):
        app().main_window.input_ui.set_normal_pressure_load()
    
    def item_child_acoustic_pressure_callback(self):
        app().main_window.input_ui.set_acoustic_pressure()
    
    def item_child_compressor_excitation_waveform_callback(self):
        app().main_window.input_ui.compressor_excitation_waveform()

    def item_child_compressor_excitation_spectrum_callback(self):
        app().main_window.input_ui.compressor_excitation_spectrum()

    def item_child_reciprocating_compressor_excitation_callback(self):
        app().main_window.input_ui.add_reciprocating_compressor_excitation()

    def item_child_mass_source_callback(self):
        app().main_window.input_ui.set_mass_source()
    
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

    def item_child_acoustic_properties_gradient_callback(self):
        app().main_window.input_ui.set_acoustic_properties_grandient()
    
    def item_child_acoustic_transfer_element_setup_callback(self):
        app().main_window.input_ui.set_acoustic_transfer_element_setup()

    def modify_general_settings_items_access(self):
        imported_geometry = app().project.model.is_there_a_geometry_imported()
        self.item_child_mesh_setup.setDisabled(not imported_geometry)
        self.item_child_element_options.setDisabled(not imported_geometry)

    def hide_all_top_items(self):
        self.item_top_general_settings.setHidden(True)
        self.hide_model_setup_top_items()

    def hide_model_setup_top_items(self):
        self.item_top_structural_model_setup.setHidden(True)
        self.item_top_acoustic_model_setup.setHidden(True)

    def expand_menu_items(self):
        self.expandItem(self.item_top_general_settings)
        self.expandItem(self.item_top_structural_model_setup)
        self.expandItem(self.item_top_acoustic_model_setup)

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
