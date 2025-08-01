from enum import Enum
import numpy as np
from molde.colors import color_names, Color
from molde.actors import CommonSymbolsActorVariableSize

from typing import Callable

from vibra import app
from vibra.interface.viewer_3d import sources

Triple = tuple[float, float, float]

class SymbolsActor(CommonSymbolsActorVariableSize):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure_appearance()
        self.build()
        self.set_zbuffer_offsets(1, -6600)

    def configure_appearance(self):
        self.GetProperty().SetAmbient(0.5)
        self.PickableOff()

    def build(self):
        self.clear_symbols()
        self._build_nodal_normals()
        
        line_properties = app().project.model.properties.line_properties
        for (property_name, line_id) in line_properties.keys():
            if property_name == "nodal_loads":
                self._build_nodal_loads(property_name, line_id=line_id)
        
        surface_properties = app().project.model.properties.surface_properties
        for (property_name, surface_id) in surface_properties.keys():
            if property_name == "surface_velocity":
                self._build_surface_velocity(surface_id)
            
            elif property_name == "prescribed_dofs":
                self._build_prescribed_dofs(property_name, surface_id)
            
            elif property_name == "nodal_loads":
                self._build_nodal_loads(property_name, surface_id=surface_id)
            
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

    def _get_center_coords_and_normals_line(self, line_id: int) -> tuple[np.ndarray, np.ndarray]:
        mesh = app().project.model.mesh
        line_nodes = mesh.nodes_from_lines.get(line_id)
        line_coordinates = mesh.nodal_coordinates[line_nodes, 1:]
        center_coords = np.average(line_coordinates, axis=0)
        dist = np.linalg.norm(line_coordinates - center_coords, axis=1)
        index = np.argmin(dist)
        
        return line_coordinates[index, :]

    def _build_surface_velocity(self, surface_id: int):
        if surface_id is None:
            return
        
        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol(sources.create_surface_velocity_source, coords, normal, color=color_names.RED_6)

    def _build_nodal_normals(self):
        mesh = app().project.model.mesh
        for node_id, normal_vector in mesh.nodal_normals_data.items():
            coords = mesh.nodal_coordinates[node_id, 1:]
            self.add_symbol(sources.create_outwards_arrow_source, coords, normal_vector, color=color_names.GRAY)

    def _build_prescribed_dofs(self, property_name, surface_id):
        coords, _ = self._get_center_coords_and_normals(surface_id)
            
        surface_properties = app().project.model.properties.surface_properties
        property = surface_properties[property_name, surface_id]
        x, y, z, *_ = property["values"]

        # alternate add_symbol function to a generic one
        if x is not None:
            self.add_symbol(sources.create_cone_source, coords, (1, 0, 0), color=color_names.GREEN)

        if y is not None:
            self.add_symbol(sources.create_cone_source, coords, (0, 1, 0), color=color_names.GREEN)

        if z is not None:
            self.add_symbol(sources.create_cone_source, coords, (0, 0, 1), color=color_names.GREEN)

    def _build_nodal_loads(self, property_name: str, surface_id = -1, line_id = -1):
        if surface_id != -1:
            surface_properties = app().project.model.properties.surface_properties
            property = surface_properties[property_name, surface_id]
            coords, normal = self._get_center_coords_and_normals(surface_id)
            
            x, y, z, *_ = [(i if i is not None else 0) for i in property["values"]]
            orientation = np.real((x, y, z))
            is_pointing = np.dot(normal, orientation) < 0
            shape = sources.create_arrow_source if is_pointing else sources.create_outwards_arrow_source
            self.add_symbol(shape, coords, orientation, color=color_names.RED_2)
        
        if line_id != -1:
            line_properties = app().project.model.properties.line_properties
            property = line_properties[property_name, line_id]
            x, y, z, *_ = [(i if i is not None else 0) for i in property["values"]]
            orientation = np.real((x, y, z))
            coord = self._get_center_coords_and_normals_line(line_id)
            
            self.add_symbol(sources.create_arrow_source, coord, orientation, color=color_names.RED_2)
            
    def _build_distributed_loads(self, property_name: str, surface_id: int):
        surface_properties = app().project.model.properties.surface_properties
        property = surface_properties[property_name, surface_id]
        
        coords, normal = self._get_center_coords_and_normals(surface_id)
        x, y, z, *_ = [(i if i is not None else 0) for i in property["values"]]
        orientation = np.real((x, y, z))
        is_pointing = np.dot(normal, orientation) < 0
        shape = sources.create_triple_arrow_source if is_pointing else sources.create_outwards_arrow_source
        self.add_symbol(shape, coords, orientation, color=color_names.RED_2)
    
    def _build_normal_pressure_load(self, property_name: str, surface_id: int):
        surface_properties = app().project.model.properties.surface_properties
        property = surface_properties[property_name, surface_id]
        
        coords, normal = self._get_center_coords_and_normals(surface_id)
        x = property["values"]
        shape = sources.create_outwards_normal_pressure_load if x[0].real > 0 else sources.create_normal_pressure_load
        self.add_symbol(shape, coords, normal, color=color_names.RED_2)
    
    def _build_specific_impedance(self, property_name: str, surface_id: int):
        surface_properties = app().project.model.properties.surface_properties
        property = surface_properties[property_name, surface_id]
        
        coords, normal = self._get_center_coords_and_normals(surface_id)
        shape = sources.create_anechoic_termination_source if "anechoic_termination" in property.keys() else sources.create_impedance_source
        self.add_symbol(shape, coords, normal, color=color_names.PURPLE_2)
   
    def _build_transfer_impedance(self, surface_id: int):
        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol(sources.create_transfer_impedance_source, coords, normal, color=color_names.PURPLE_2)
    
    def _build_perforated_plate_model(self, surface_id: int):
        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol(sources.create_perforated_plate_source, coords, normal, color=color_names.RED)

    def _build_mass_flow_rate(self, surface_id: int):
        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol(sources.create_mass_flow_rate_source, coords, normal, color=color_names.PINK)
    
    def _build_dofs_decoupling(self, surface_id: int):
        surface_properties = app().project.model.properties.surface_properties
        if ("perforated_plate_model", surface_id) in surface_properties.keys():
            return
        if ("transfer_impedance", surface_id) in surface_properties.keys():
            return 

        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol(sources.create_degrees_of_freedom_decoupling_source, coords, normal, color=color_names.GREEN)
    
    def _build_absorption_surface(self, surface_id: int):
        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol(sources.create_absorption_surface_source, coords, normal, color=color_names.GREEN)
    
    def _build_acoustic_pressure(self, surface_id: int):
        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol(sources.create_acoustic_pressure_source, coords, normal, color=color_names.RED_2)
    
    def _build_reciprocating_compressor(self, property_name: str, surface_id: int):
        surface_properties = app().project.model.properties.surface_properties
        property = surface_properties[property_name, surface_id]
        
        if property["connection_type"] == "discharge":
            shape = sources.create_compressor_discharge_source
        elif property["connection_type"] == "suction":
            shape = sources.create_compressor_suction_source
        
        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol(shape, coords, normal, color=color_names.RED_2)
    
    def _build_dissipation_model(self, surface_id: int):
        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol(sources.create_dissipation_model_source, coords, normal, color=color_names.BLUE)
    
    def _build_viscous_thermal_loss_model(self, surface_id: int):
        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol(sources.create_dissipation_model_source, coords, normal, color=color_names.ORANGE)
    
    def _build_acoustic_transfer_element_data(self, surface_id: int):
        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol(sources.create_acoustic_transfer_element_data_source, coords, normal, color=color_names.TURQUOISE)
    
    def _build_incident_plane_wave(self, property_name: str, surface_id: int):
        surface_properties = app().project.model.properties.surface_properties
        property = surface_properties[property_name, surface_id]
        
        wave_vector = property.get("wave_vector")
        coords, _ = self._get_center_coords_and_normals(surface_id)
        
        self.add_symbol(sources.create_incident_plane_wave_source, coords, wave_vector, color=color_names.BLUE)
    
    def _build_mass_source(self, property_name: str, surface_id: int):
        coords, normal = self._get_center_coords_and_normals(surface_id)
        color_fir_sphere = color_names.RED.copy()
        self.add_symbol(sources.create_mass_load_first_layer_source, coords, normal, color=color_fir_sphere)
        
        color_sec_sphere = color_names.YELLOW.copy()
        color_sec_sphere.a = 150
        self.add_symbol(sources.create_mass_load_second_layer_source, coords, normal, color=color_sec_sphere)
        
        color_third_sphere = color_names.GREEN.copy()
        color_third_sphere.a = 100
        self.add_symbol(sources.create_mass_load_third_layer_source, coords, normal, color=color_third_sphere)
        
        color_fourth_sphere = color_names.BLUE.copy()
        color_fourth_sphere.a = 50
        self.add_symbol(sources.create_mass_load_fourth_layer_source, coords, normal, color=color_fourth_sphere)