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
    create_degrees_of_freedom_decoupling_source,
    create_absorption_surface_source,
    create_acoustic_pressure_source,
    create_reciprocating_compressor_source,
    create_dissipation_model_source,
    create_acoustic_transfer_element_data_source,
    create_incident_plane_wave_source,
    create_surface_velocity_source,
)

Triple = tuple[float, float, float]

class Shape(Enum):
    ARROW = "arrow"
    LONG_ARROW = "long_arrow"
    DOUBLE_ARROW = "double_arrow"
    OUTWARDS_ARROW = "outwards_arrow"
    CONE = "cone"
    CUBE = "cube"
    SPRING = "spring"
    DAMPER = "damper"
    MASS = "mass"
    PERFORATED_PLATE_MODEL = "perforated_plate_model"
    IMPEDANCE = "impedance"
    TRANSFER_IMPEDANCE = "transfer_impedance"
    INCIDENT_PLANE_WAVE = "incident_plane_wave"
    ANECHOIC_TERMINATION = "anechoic_termination"
    SURFACE_VELOCITY = "surface_velocity"
    MASS_FLOW_RATE = "mass_flow_rate"
    DISTRIBUTED_LOADS = "distributed_loads"
    DISTRIBUTED_LOADS_OUTWARDS = "distributed_loads_outwards"
    NORMAL_PRESSURE_LOAD = "normal_pressure_load"
    DEGREES_OF_FREEDOM_DECOUPLING = "degrees_of_freedom_decoupling"
    ABSORPTION_SURFACE = "absorption_surface"
    ACOUSTIC_PRESSURE = "acoustic_pressure"
    RECIPROCATING_COMPRESSOR = "reciprocating_compressor"
    DISSIPATION_MODEL = "dissipation_model"
    ACOUSTIC_TRANSFER_ELEMENT_DATA = "acoustic_transfer_element_data"

    @classmethod
    def get_shapes(cls):
        return [v.value for v in cls.__members__.values()]

class SymbolsActor(CommonSymbolsActorVariableSize):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure_appearance()
        self._register_shapes()
        self.build()
        # self.set_zbuffer_offsets(1, -(1 << 16))

    def configure_appearance(self):
        self.GetProperty().SetAmbient(0.5)
        self.PickableOff()

    def build(self):
        self.clear_symbols()
        self._build_nodal_normals()
        
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
                self._build_normal_pressure_load(surface_id)
            
            elif property_name == "specific_impedance":
                self._build_specific_impedance(property_name, surface_id)
                
            elif property_name == "transfer_impedance":
                self._build_transfer_impedance(surface_id)
            
            elif property_name == "perforated_plate_model":
                self._build_perforated_plate_model(surface_id)
            
            elif property_name == "mass_flow_rate":
                self._build_mass_flow_rate(surface_id)
            
            elif property_name == "degrees_of_freedom_decoupling":
                self._build_dofs_decoupling(surface_id)
            
            elif property_name == "absorption_surface":    
                self._build_absorption_surface(surface_id)
            
            elif property_name == "acoustic_pressure":
                self._build_acoustic_pressure(surface_id)
            
            elif property_name == "reciprocating_compressor":
                self._build_reciprocating_compressor(surface_id)
            
            elif property_name == "dissipation_model":
                self._build_dissipation_model(surface_id)
            
            elif property_name == "acoustic_transfer_element_data":
                self._build_acoustic_transfer_element_data(surface_id)
            
            elif property_name == "incident_plane_wave":
                self._build_incident_plane_wave(surface_id)

        super().build()

    def _get_center_coords_and_normals(self, surface_id: int) -> float:
        mesh = app().project.model.mesh

        surface_nodes = mesh.nodes_from_surfaces[surface_id]
        surface_normals = mesh.normals_surface.get(surface_id)
        surface_coordinates = mesh.nodal_coordinates[surface_nodes, 1:]

        curvatures_surface = mesh.curvatures_surface.get(surface_id)
        contains_curvature = (curvatures_surface is not None) and np.any(curvatures_surface)
        center_coords = np.average(surface_coordinates, axis=0)

        if contains_curvature:
            # Finds the node that is closest to the center coords
            dist = np.linalg.norm(surface_coordinates - center_coords, axis=1)
            index = np.argmin(dist)
            return surface_coordinates[index, :], surface_normals[index, :]

        else:
            return center_coords, np.average(surface_normals, axis=0)


    def _build_surface_velocity(self, surface_id: int):
        if surface_id is None:
            return
        
        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_normal_surface_velocity_symbol(coords, normal)

    def _build_nodal_normals(self):
        mesh = app().project.model.mesh
        for node_id, normal_vector in mesh.nodal_normals_data.items():
            coords = mesh.nodal_coordinates[node_id, 1:]
            self.add_normal_symbol(coords, normal_vector)

    def _build_prescribed_dofs(self, property_name, surface_id):
        coords, _ = self._get_center_coords_and_normals(surface_id)
            
        surface_properties = app().project.model.properties.surface_properties
        property = surface_properties[property_name, surface_id]
        x, y, z, *_ = property["values"]

        # alternate add_symbol function to a generic one
        if x is not None:
            self.add_prescribed_dof_symbol(coords, (1, 0, 0))

        if y is not None:
            self.add_prescribed_dof_symbol(coords, (0, 1, 0))

        if z is not None:
            self.add_prescribed_dof_symbol(coords, (0, 0, 1))

    def _build_nodal_loads(self, property_name: str, surface_id: int):
        surface_properties = app().project.model.properties.surface_properties
        property = surface_properties[property_name, surface_id]
        coords, normal = self._get_center_coords_and_normals(surface_id)
        
        x, y, z, *_ = [(i if i is not None else 0) for i in property["values"]]
        orientation = np.real((x, y, z))
        is_pointing = np.dot(normal, orientation) < 0
        shape = Shape.ARROW if is_pointing else Shape.OUTWARDS_ARROW
        self.add_symbol_render(shape, coords, orientation, color=color_names.RED_2, scale=1)
        # self.add_force_symbol(coords, orientation, is_pointing)
            
    def _build_distributed_loads(self, property_name: str, surface_id: int):
        surface_properties = app().project.model.properties.surface_properties
        property = surface_properties[property_name, surface_id]
        
        coords, normal = self._get_center_coords_and_normals(surface_id)
        x, y, z, *_ = [(i if i is not None else 0) for i in property["values"]]
        orientation = np.real((x, y, z))
        is_pointing = np.dot(normal, orientation) < 0
        shape = Shape.DISTRIBUTED_LOADS if is_pointing else Shape.DISTRIBUTED_LOADS_OUTWARDS
        self.add_symbol_render(shape, coords, orientation, color=color_names.RED_2, scale=1)
        # self.add_distributed_loads_symbol(coords, orientation, is_pointing)
    
    def _build_normal_pressure_load(self, surface_id: int):
        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol_render(Shape.NORMAL_PRESSURE_LOAD, coords, normal, color=color_names.RED_2, scale=1)
        # self.add_normal_pressure_load_symbol(coords, normal)
    
    def _build_specific_impedance(self, property_name: str, surface_id: int):
        surface_properties = app().project.model.properties.surface_properties
        property = surface_properties[property_name, surface_id]
        
        coords, normal = self._get_center_coords_and_normals(surface_id)
        shape = Shape.ANECHOIC_TERMINATION if "anechoic_termination" in property.keys() else Shape.IMPEDANCE
        self.add_symbol_render(shape, coords, normal, color=color_names.PURPLE_2, scale=1)
   
    def _build_transfer_impedance(self, surface_id: int):
        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol_render(Shape.TRANSFER_IMPEDANCE, coords, normal, color=color_names.PURPLE_2, scale=1)
        # self.add_transfer_impedance_symbol(coords, normal)
    
    def _build_perforated_plate_model(self, surface_id: int):
        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol_render(Shape.PERFORATED_PLATE_MODEL, coords, normal, color=color_names.RED, scale=1)
        # self.add_perforated_plate_symbol(coords, normal)

    def _build_mass_flow_rate(self, surface_id: int):
        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol_render(Shape.MASS_FLOW_RATE, coords, normal, color=color_names.PINK, scale=1)
        # self.add_mass_flow_rate_symbol(coords, normal)
    
    def _build_dofs_decoupling(self, surface_id: int):
        surface_properties = app().project.model.properties.surface_properties
        if ("perforated_plate_model", surface_id) in surface_properties.keys():
            return
        if ("transfer_impedance", surface_id) in surface_properties.keys():
            return 

        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol_render(Shape.DEGREES_OF_FREEDOM_DECOUPLING, coords, normal, color=color_names.GREEN, scale=1)
        # self.add_dofs_decoupling_symbol(coords, normal)
    
    def _build_absorption_surface(self, surface_id: int):
        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol_render(Shape.ABSORPTION_SURFACE, coords, normal, color=color_names.GREEN, scale=1)
        # self.add_absorption_surface_symbol(coords, normal)
    
    def _build_acoustic_pressure(self, surface_id: int):
        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol_render(Shape.ACOUSTIC_PRESSURE, coords, normal, color=color_names.RED_2, scale=1)
        # self.add_acoustic_pressure_symbol(coords, normal)
    
    def _build_reciprocating_compressor(self, surface_id: int):
        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol_render(Shape.RECIPROCATING_COMPRESSOR, coords, normal, color=color_names.RED_2, scale=1)
        # self.add_reciprocating_compressor_symbol(coords, normal)
    
    def _build_dissipation_model(self, surface_id: int):
        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol_render(Shape.DISSIPATION_MODEL, coords, normal, color=color_names.BLUE, scale=1)
        # self.add_dissipation_model_symbol(coords, normal)
    
    def _build_viscous_thermal_loss_model(self, surface_id: int):
        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol_render(Shape.DISSIPATION_MODEL, coords, normal, color=color_names.ORANGE, scale=1)
        # self.add_viscous_thermal_loss_model_symbol(coords, normal)
    
    def _build_acoustic_transfer_element_data(self, surface_id: int):
        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol_render(Shape.ACOUSTIC_TRANSFER_ELEMENT_DATA, coords, normal, color=color_names.TURQUOISE, scale=1)
        # self.add_acoustic_transfer_element_data_symbol(coords, normal)
    
    def _build_incident_plane_wave(self, surface_id: int):
        coords, normal = self._get_center_coords_and_normals(surface_id)
        self.add_symbol_render(Shape.INCIDENT_PLANE_WAVE, coords, normal, color=color_names.BLUE, scale=1)
        # self.add_incident_plane_wave_symbol(coords, normal)

    # Specifications on how each symbol should look like
    def add_symbol_render(self, shape: Shape, position: Triple, orientation: Triple, color: Color, scale: float = 1):
        self.add_symbol(
            shape_name=shape.value,
            position=position,
            orientation=orientation,
            color=color,
            scale=1,
        )
    
    def add_force_symbol(self, position, orientation, pointing=True):
        shape_name = "arrow" if pointing else "outwards_arrow"
        self.add_symbol(
            shape_name,
            position,
            orientation,
            color=color_names.RED_2,
            scale=1,
        )
    
    def add_distributed_loads_symbol(self, position, orientation, pointing=False):
        shape_name = "distributed_loads_outwards" if pointing else "distributed_loads"
        self.add_symbol(
            shape_name,
            position,
            orientation,
            color=color_names.RED_2,
            scale=1,
        )
    
    def add_normal_pressure_load_symbol(self, position, orientation):
        self.add_symbol(
            "normal_pressure_load",
            position,
            orientation,
            color=color_names.RED_2,
            scale=1,
        )

    def add_spring_symbol(self, position, orientation):
        self.add_symbol(
            "spring",
            position,
            orientation,
            color=color_names.ORANGE,
            scale=0.8,
        )

    def add_prescribed_dof_symbol(self, position, orientation):
        self.add_symbol(
            "cone",
            position,
            orientation,
            color=color_names.GREEN,
            scale=0.4,
        )

    def add_normal_surface_velocity_symbol(self, position, orientation):
        self.add_symbol(
            "surface_velocity",
            position,
            orientation,
            color=color_names.RED_6,
            scale=1,
        )

    def add_damper_symbol(self, position, orientation):
        self.add_symbol(
            "damper",
            position,
            orientation,
            color=color_names.PINK,
            scale=0.8,
        )

    def add_mass_symbol(self, position, orientation):
        self.add_symbol(
            "mass",
            position,
            orientation,
            color=color_names.BLUE,
            scale=2,
        )
    
    def add_acoustic_pressure_symbol(self, position, orientation):
        self.add_symbol(
            "acoustic_pressure",
            position,
            orientation,
            color=color_names.RED_2,
            scale=1,
        )

    def add_impedance_symbol(self, position, orientation):
        self.add_symbol(
            "impedance",
            position,
            orientation,
            color=color_names.PURPLE_2,
            scale=1,
        )

    def add_normal_symbol(self, position, orientation):
        self.add_symbol(
            "outwards_arrow",
            position,
            orientation,
            color=color_names.GRAY,
            scale=1,
        )
    
    def add_perforated_plate_symbol(self, position, orientation):
        self.add_symbol(
            "perforated_plate",
            position,
            orientation,
            color=color_names.RED,
            scale=1,
        )
    
    def add_mass_flow_rate_symbol(self, position, orientation):
        self.add_symbol(
            "mass_flow_rate",
            position,
            orientation,
            color=color_names.PINK_4,
            scale=1,
        )
    
    def add_dofs_decoupling_symbol(self, position, orientation):
        self.add_symbol(
            "degrees_of_freedom_decoupling",
            position,
            orientation,
            color=color_names.GREEN,
            scale=1,
        )
    
    def add_absorption_surface_symbol(self, position, orientation):
        self.add_symbol(
            "absorption_surface",
            position,
            orientation,
            color=color_names.GREEN,
            scale=1,
        )
    
    def add_reciprocating_compressor_symbol(self, position, orientation):
        self.add_symbol(
            "reciprocating_compressor",
            position,
            orientation,
            color=color_names.RED_2,
            scale=1,
        )
    
    def add_dissipation_model_symbol(self, position, orientation):
        self.add_symbol(
            "dissipation_model",
            position,
            orientation,
            color=color_names.BLUE,
            scale=1,
        )
    
    def add_viscous_thermal_loss_model_symbol(self, position, orientation):
        self.add_symbol(
            "dissipation_model",
            position,
            orientation,
            color=color_names.ORANGE,
            scale=1,
        )
    
    def add_anechoic_termination_symbol(self, position, orientation):
        self.add_symbol(
            "anechoic_termination",
            position,
            orientation,
            color=color_names.PURPLE_2,
            scale=1,
        )
    
    def add_transfer_impedance_symbol(self, position, orientation):
        self.add_symbol(
            "transfer_impedance",
            position,
            orientation,
            color=color_names.PURPLE_2,
            scale=1,
        )
    
    def add_acoustic_transfer_element_data_symbol(self, position, orientation):
        self.add_symbol(
            "acoustic_transfer_element_data",
            position,
            orientation,
            color=color_names.TURQUOISE,
            scale=1,
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
        self.register_shape("transfer_impedance", create_transfer_impedance_source())
        self.register_shape("anechoic_termination", create_anechoic_termination_source())
        self.register_shape("mass_flow_rate", create_mass_flow_rate_source())
        self.register_shape("distributed_loads", create_triple_arrow_source())
        self.register_shape("distributed_loads_outwards", create_outwards_triple_arrow_source())
        self.register_shape("normal_pressure_load", create_normal_pressure_load())
        self.register_shape("degrees_of_freedom_decoupling", create_degrees_of_freedom_decoupling_source())
        self.register_shape("absorption_surface", create_absorption_surface_source())
        self.register_shape("acoustic_pressure", create_acoustic_pressure_source())
        self.register_shape("reciprocating_compressor", create_reciprocating_compressor_source())
        self.register_shape("dissipation_model", create_dissipation_model_source())
        self.register_shape("acoustic_transfer_element_data", create_acoustic_transfer_element_data_source())
        self.register_shape("surface_velocity", create_surface_velocity_source())
