import numpy as np
from molde.colors import color_names
from molde.actors import CommonSymbolsActorFixedSize

from vibra import app
from vibra.interface.viewer_3d import sources


class SymbolsActorAcousticFixedSize(CommonSymbolsActorFixedSize):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._build_dict_property_name_to_build_function()
        self.configure_appearance()
        self.build()
        # self.set_zbuffer_offsets(1, -6600)

    def configure_appearance(self):
        self.GetProperty().SetAmbient(0.5)
        self.PickableOff()

    def _build_dict_property_name_to_build_function(self):
        self.prop_name_to_build_func = {
            "reciprocating_compressor_excitation": self._build_reciprocating_compressor,
        }

    def _call_build_functions(self, property_name: str, surface_id: int = -1, line_id: int = -1, point_id: int = -1, node_id: int = -1):
        if property_name in self.prop_name_to_build_func.keys():
            self.prop_name_to_build_func[property_name](
                property_name=property_name,
                surface_id=surface_id,
                line_id=line_id,
                point_id=point_id,
                node_id=node_id                                                                                 
            )

    def build(self):
        self.clear_symbols()
        
        surface_properties = app().project.model.properties.surface_properties
        for property_name, surface_id in surface_properties.keys():
            self._call_build_functions(property_name, surface_id=surface_id)
            # self._call_build_functions("reciprocating_compressor_excitation", surface_id=8)

        super().build()

    def _get_center_coords_and_normals(self, surface_id: int) -> tuple[np.ndarray, np.ndarray]:
        geometry = app().project.model.geometry


        avg_normal = geometry.surface_normal(surface_id)
        center_coords = geometry.surface_center(surface_id)
        surface_area = geometry.surface_area(surface_id)

        radius = np.sqrt(surface_area/np.pi)

        return center_coords, avg_normal, radius

    def _build_reciprocating_compressor(self, property_name: str, surface_id: int = -1, *args, **kwargs):
        if surface_id == -1:
            return
        
        surface_properties = app().project.model.properties.surface_properties
        property = surface_properties[property_name, surface_id]

        color = None
        if property["connection_type"] == "discharge":
            shape = sources.create_compressor_discharge_source
            # vermelho, seta entra é azul
            color = color_names.RED_3
        elif property["connection_type"] == "suction":
            shape = sources.create_compressor_suction_source
            color = color_names.BLUE_3

        coords, normal, max_dist = self._get_center_coords_and_normals(surface_id)
        self.add_symbol(shape, coords, normal, color=color, scale=1.985 * max_dist)