from enum import Enum
import numpy as np
from molde.colors import color_names, Color
from molde.actors import CommonSymbolsActorVariableSize


from vibra import app
from vibra.interface.viewer_3d.sources import (
    create_arrow_source,
    create_cone_source,
    create_cube_source,
    create_damper_source,
    create_double_arrow_source,
    create_long_arrow_source,
    create_mass_source,
    create_outwards_arrow_source,
    create_spring_source,
    create_perforated_plate_source,
    create_impedance_source,
    create_anechoic_termination_source,
    create_transfer_impedance_source,
    create_mass_flow_rate_source,
    create_triple_arrow_source,
    create_outwards_triple_arrow_source,
    create_normal_pressure_load,
    create_outwards_normal_pressure_load,
    create_degrees_of_freedom_decoupling_source,
    create_absorption_surface_source,
    create_acoustic_pressure_source,
    create_compressor_discharge_source,
    create_compressor_suction_source,
    create_dissipation_model_source,
    create_acoustic_transfer_element_data_source,
    create_incident_plane_wave_source,
    create_outwards_incident_plane_wave_source,
    create_surface_velocity_source,
    create_mass_load_first_layer_source,
    create_mass_load_second_layer_source,
    create_mass_load_third_layer_source,
    create_mass_load_fourth_layer_source,
)

Triple = tuple[float, float, float]

class SymbolsActor(CommonSymbolsActorVariableSize):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure_appearance()
        self._register_shapes()
        self.build()

    def configure_appearance(self):
        self.GetProperty().SetAmbient(0.5)
        self.PickableOff()

    def build(self):
        self.clear_symbols()
        self._build_nodal_normals()
        
        # line_properties = app().project.model.properties.line_properties
        # for (property_name, line_id) in line_properties.keys():
        #     if property_name == "nodal_loads":
        #         property = line_properties[property_name, line_id]
        #         print(property)
        #         print('=====================================')
        #         coord = self._get_center_coords_and_normals_line(line_id)
        #         print()
        #         self.add_symbol_render("arrow", coord, (0, 0, 0), color=color_names.RED_2)
        #         # coords, normal = self._get_center_coords_and_normals(surface_id)
                
        #         # x, y, z, *_ = [(i if i is not None else 0) for i in property["values"]]
        #         # orientation = np.real((x, y, z))
        #         # is_pointing = np.dot(normal, orientation) < 0
        #         # shape = "arrow" if is_pointing else "outwards_arrow"
        #         # self.add_symbol_render(shape, coords, orientation, color=color_names.RED_2)
        
        surface_properties = app().project.model.properties.surface_properties
        for (property_name, surface_id) in surface_properties.keys():
            if property_name == "surface_velocity":
                self._build_surface_velocity(surface_id)
            
            elif property_name == "prescribed_dofs":
                self._build_prescribed_dofs(property_name, surface_id)
            
            elif property_name == "nodal_loads":
                self._build_nodal_loads(property_name, surface_id)
            
            elif property_name == "distributed_loads":
                self._build_distributed_loads(property_name, surface_id)
            
            elif property_name == "normal_pressure_load":
                self._build_normal_pressure_load(property_name, surface_id)
            
            elif property_name == "specific_impedance":
                self._build_specific_impedance(property_name, surface_id)
                
            elif property_name == "transfer_impedance":
                self._build_transfer_impedance(surface_id)
            
            elif property_name == "mass_flow_rate":
                self._build_mass_flow_rate(surface_id)
            
            elif property_name == "degrees_of_freedom_decoupling":
                self._build_dofs_decoupling(surface_id)
            
            elif property_name == "absorption_surface":    
                self._build_absorption_surface(surface_id)
            
            elif property_name == "acoustic_pressure":
                self._build_acoustic_pressure(surface_id)
            
            elif property_name == "reciprocating_compressor_excitation":
                self._build_reciprocating_compressor(property_name, surface_id)
            
            elif property_name == "dissipation_model":
                self._build_dissipation_model(surface_id)
            
            elif property_name == "acoustic_transfer_element_data":
                self._build_acoustic_transfer_element_data(surface_id)
            
            elif property_name == "incident_plane_wave":
                self._build_incident_plane_wave(property_name, surface_id)
            
            elif property_name == "mass_source":
                self._build_mass_source(property_name, surface_id)

        super().build()

    def _get_center_coords_and_normals(self, surface_id: int) -> tuple[np.ndarray, np.ndarray]:
        mesh = app().project.model.mesh
        surface_nodes = mesh.nodes_from_surfaces.get(surface_id)
        surface_coordinates = mesh.nodal_coordinates[surface_nodes, 1:]

        surface_normals = mesh.normals_surface.get(surface_id)
        if surface_normals is None:
            eface_normals = mesh.get_stacked_normals_for_surface_elements(surface_id)
            avg_normal = np.average(eface_normals, axis=0).flatten()

        else:
            avg_normal = np.average(surface_normals, axis=0).round(6)

        curvatures_surface = mesh.curvatures_surface.get(surface_id)
        contains_curvature = (curvatures_surface is not None) and np.any(curvatures_surface)
        center_coords = np.average(surface_coordinates, axis=0)

        if contains_curvature:
            # Finds the node that is closest to the center coords
            dist = np.linalg.norm(surface_coordinates - center_coords, axis=1)
            index = np.argmin(dist)
            return surface_coordinates[index, :], surface_normals[index, :]

        return center_coords, avg_normal

    # def _get_center_coords_and_normals_line(self, line_id: int) -> tuple[np.ndarray, np.ndarray]:
    #     mesh = app().project.model.mesh
    #     line_nodes = mesh.nodes_from_lines.get(line_id)
    #     print(line_nodes)
    #     line_coordinates = mesh.nodal_coordinates[line_nodes, 1:]
    #     print('===================================')
    #     print(line_coordinates)

    #     # surface_normals = mesh.normals_surface.get(surface_id)
    #     # if surface_normals is None:
    #     #     eface_normals = mesh.get_stacked_normals_for_surface_elements(surface_id)
    #     #     avg_normal = np.average(eface_normals, axis=0).flatten()

    #     # else:
    #     #     avg_normal = np.average(surface_normals, axis=0).round(6)

    #     # curvatures_surface = mesh.curvatures_surface.get(surface_id)
    #     # contains_curvature = (curvatures_surface is not None) and np.any(curvatures_surface)
    #     center_coords = np.average(line_coordinates, axis=0)
    #     return center_coords

    #     # if contains_curvature:
    #     #     # Finds the node that is closest to the center coords
    #     #     dist = np.linalg.norm(surface_coordinates - center_coords, axis=1)
    #     #     index = np.argmin(dist)
    #     #     return surface_coordinates[index, :], surface_normals[index, :]

    #     # return center_coords, avg_normal

    def _build_surface_velocity(self, surface_id: int):
        if surface_id is None:
            return
        
        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol_render("surface_velocity", coords, normal, color=color_names.RED_6)

    def _build_nodal_normals(self):
        mesh = app().project.model.mesh
        for node_id, normal_vector in mesh.nodal_normals_data.items():
            coords = mesh.nodal_coordinates[node_id, 1:]
            self.add_symbol_render("outwards_arrow", coords, normal_vector, color=color_names.GRAY)

    def _build_prescribed_dofs(self, property_name, surface_id):
        coords, _ = self._get_center_coords_and_normals(surface_id)
            
        surface_properties = app().project.model.properties.surface_properties
        property = surface_properties[property_name, surface_id]
        x, y, z, *_ = property["values"]

        # alternate add_symbol function to a generic one
        if x is not None:
            self.add_symbol_render("cone", coords, (1, 0, 0), color=color_names.GREEN)

        if y is not None:
            self.add_symbol_render("cone", coords, (0, 1, 0), color=color_names.GREEN)

        if z is not None:
            self.add_symbol_render("cone", coords, (0, 0, 1), color=color_names.GREEN)

    def _build_nodal_loads(self, property_name: str, surface_id):
        surface_properties = app().project.model.properties.surface_properties
        property = surface_properties[property_name, surface_id]
        coords, normal = self._get_center_coords_and_normals(surface_id)
        
        x, y, z, *_ = [(i if i is not None else 0) for i in property["values"]]
        orientation = np.real((x, y, z))
        is_pointing = np.dot(normal, orientation) < 0
        shape = "arrow" if is_pointing else "outwards_arrow"
        self.add_symbol_render(shape, coords, orientation, color=color_names.RED_2)
            
    def _build_distributed_loads(self, property_name: str, surface_id: int):
        surface_properties = app().project.model.properties.surface_properties
        property = surface_properties[property_name, surface_id]
        
        coords, normal = self._get_center_coords_and_normals(surface_id)
        x, y, z, *_ = [(i if i is not None else 0) for i in property["values"]]
        orientation = np.real((x, y, z))
        is_pointing = np.dot(normal, orientation) < 0
        shape = "distributed_loads" if is_pointing else "distributed_loads_outwards"
        self.add_symbol_render(shape, coords, orientation, color=color_names.RED_2)
    
    def _build_normal_pressure_load(self, property_name: str, surface_id: int):
        surface_properties = app().project.model.properties.surface_properties
        property = surface_properties[property_name, surface_id]
        
        coords, normal = self._get_center_coords_and_normals(surface_id)
        x = property["values"]
        shape = "outwards_normal_pressure_load" if x[0].real > 0 else "normal_pressure_load"
        
        self.add_symbol_render(shape, coords, normal, color=color_names.RED_2)
    
    def _build_specific_impedance(self, property_name: str, surface_id: int):
        surface_properties = app().project.model.properties.surface_properties
        property = surface_properties[property_name, surface_id]
        
        coords, normal = self._get_center_coords_and_normals(surface_id)
        shape = "anechoic_termination" if "anechoic_termination" in property.keys() else "impedance"
        self.add_symbol_render(shape, coords, normal, color=color_names.PURPLE_2)
   
    def _build_transfer_impedance(self, surface_id: int):
        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol_render("transfer_impedance", coords, normal, color=color_names.PURPLE_2)
    
    def _build_perforated_plate_model(self, surface_id: int):
        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol_render("perforated_plate_model", coords, normal, color=color_names.RED)

    def _build_mass_flow_rate(self, surface_id: int):
        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol_render("mass_flow_rate", coords, normal, color=color_names.PINK)
    
    def _build_dofs_decoupling(self, surface_id: int):
        surface_properties = app().project.model.properties.surface_properties
        if ("perforated_plate_model", surface_id) in surface_properties.keys():
            return
        if ("transfer_impedance", surface_id) in surface_properties.keys():
            return 

        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol_render("degrees_of_freedom_decoupling", coords, normal, color=color_names.GREEN)
    
    def _build_absorption_surface(self, surface_id: int):
        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol_render("absorption_surface", coords, normal, color=color_names.GREEN)
    
    def _build_acoustic_pressure(self, surface_id: int):
        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol_render("acoustic_pressure", coords, normal, color=color_names.RED_2)
    
    def _build_reciprocating_compressor(self, property_name: str, surface_id: int):
        surface_properties = app().project.model.properties.surface_properties
        property = surface_properties[property_name, surface_id]
        
        if property["connection_type"] == "discharge":
            shape = "compressor_discharge"
        elif property["connection_type"] == "suction":
            shape = "compressor_suction"
        
        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol_render(shape, coords, normal, color=color_names.RED_2)
    
    def _build_dissipation_model(self, surface_id: int):
        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol_render("dissipation_model", coords, normal, color=color_names.BLUE)
    
    def _build_viscous_thermal_loss_model(self, surface_id: int):
        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol_render("dissipation_model", coords, normal, color=color_names.ORANGE)
    
    def _build_acoustic_transfer_element_data(self, surface_id: int):
        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol_render("acoustic_transfer_element_data", coords, normal, color=color_names.TURQUOISE)
    
    def _build_incident_plane_wave(self, property_name: str, surface_id: int):
        surface_properties = app().project.model.properties.surface_properties
        property = surface_properties[property_name, surface_id]
        
        wave_vector = property.get("wave_vector")
        coords, _ = self._get_center_coords_and_normals(surface_id)
        
        self.add_symbol_render("incident_plane_wave", coords, wave_vector, color=color_names.BLUE)
    
    def _build_mass_source(self, property_name: str, surface_id: int):
        coords, normal = self._get_center_coords_and_normals(surface_id)
        color_fir_sphere = color_names.RED.copy()
        self.add_symbol_render("mass_source_first_layer", coords, normal, color=color_fir_sphere)
        
        color_sec_sphere = color_names.YELLOW.copy()
        color_sec_sphere.a = 150
        self.add_symbol_render("mass_source_second_layer", coords, normal, color=color_sec_sphere)
        
        color_third_sphere = color_names.GREEN.copy()
        color_third_sphere.a = 100
        self.add_symbol_render("mass_source_third_layer", coords, normal, color=color_third_sphere)
        
        color_fourth_sphere = color_names.BLUE.copy()
        color_fourth_sphere.a = 50
        self.add_symbol_render("mass_source_fourth_layer", coords, normal, color=color_fourth_sphere)
        
    # Specifications on how each symbol should look like
    def add_symbol_render(self, shape: str, position: Triple, orientation: Triple, color: Color, scale: float = 1):
        self.add_symbol(
            shape_name=shape,
            position=position,
            orientation=orientation,
            color=color,
            scale=scale
        )

    # Preload the symbol shapes (they are likelly used in many symbols)
    def _register_shapes(self):
        self.register_shape("arrow", create_arrow_source())
        self.register_shape("long_arrow", create_long_arrow_source())
        self.register_shape("double_arrow", create_double_arrow_source())
        self.register_shape("outwards_arrow", create_outwards_arrow_source())
        self.register_shape("cone", create_cone_source())
        self.register_shape("cube", create_cube_source())
        self.register_shape("spring", create_spring_source())
        self.register_shape("damper", create_damper_source())
        self.register_shape("mass", create_mass_source())
        self.register_shape("perforated_plate_model", create_perforated_plate_source())
        self.register_shape("impedance", create_impedance_source())
        self.register_shape("incident_plane_wave", create_incident_plane_wave_source())
        self.register_shape("outwards_incident_plane_wave", create_outwards_incident_plane_wave_source())
        self.register_shape("transfer_impedance", create_transfer_impedance_source())
        self.register_shape("anechoic_termination", create_anechoic_termination_source())
        self.register_shape("mass_flow_rate", create_mass_flow_rate_source())
        self.register_shape("distributed_loads", create_triple_arrow_source())
        self.register_shape("distributed_loads_outwards", create_outwards_triple_arrow_source())
        self.register_shape("normal_pressure_load", create_normal_pressure_load())
        self.register_shape("outwards_normal_pressure_load", create_outwards_normal_pressure_load())
        self.register_shape("degrees_of_freedom_decoupling", create_degrees_of_freedom_decoupling_source())
        self.register_shape("absorption_surface", create_absorption_surface_source())
        self.register_shape("acoustic_pressure", create_acoustic_pressure_source())
        self.register_shape("compressor_discharge", create_compressor_discharge_source())
        self.register_shape("compressor_suction", create_compressor_suction_source())
        self.register_shape("dissipation_model", create_dissipation_model_source())
        self.register_shape("acoustic_transfer_element_data", create_acoustic_transfer_element_data_source())
        self.register_shape("surface_velocity", create_surface_velocity_source())
        self.register_shape("mass_source_first_layer", create_mass_load_first_layer_source())
        self.register_shape("mass_source_second_layer", create_mass_load_second_layer_source())
        self.register_shape("mass_source_third_layer", create_mass_load_third_layer_source())
        self.register_shape("mass_source_fourth_layer", create_mass_load_fourth_layer_source())
