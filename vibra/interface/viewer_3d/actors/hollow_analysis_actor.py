import numpy as np
from vtkmodules.util.numpy_support import vtk_to_numpy
from vtkmodules.vtkCommonCore import vtkFloatArray

from vibra import app
from vibra.engine.analysis_info.analysis_enums import PhysicalDomain

from ..coloring.color_table import ColorTable
from .hollow_solids_actor import HollowSolidsActor


class HollowAnalysisActor(HollowSolidsActor):
    def __init__(self, *args, physical_domain: PhysicalDomain | None = None, **kwargs):
        self.physial_domain = physical_domain
        super().__init__(*args, **kwargs)

    def get_hidden_surfaces(self) -> set:
        mesh = app().project.mesh
        if mesh is None:
            return set()

        match self.physial_domain:
            case PhysicalDomain.ACOUSTIC:
                domain_specific_volumes = app().project.model.model_domains.get("acoustic", set())
            case PhysicalDomain.STRUCTURAL:
                domain_specific_volumes = app().project.model.model_domains.get("structural", set())
            case _:
                domain_specific_volumes = mesh.all_solid_ids()

        visible_surfaces = set()
        for volume in domain_specific_volumes:
            surfaces = mesh.surfaces_from_volume.get(volume, [])
            visible_surfaces |= set(surfaces)

        visible_surfaces &= app().main_window.entity_visibility.get_visible_surfaces()
        return mesh.all_surface_ids() - visible_surfaces

    def apply_deformation(self, deformed_coordinates: np.ndarray):
        self.update_coordinates(deformed_coordinates)

    def plot_color_bar(self, values, min_value, max_value, colormap="jet"):
        color_table = ColorTable(values, min_value, max_value, colormap)
        self.set_color_table(color_table)

    def set_color_table(self, color_table: ColorTable):
        if self.data is None:
            return

        self.color_table = color_table
        point_colors: vtkFloatArray = self.data.GetPointData().GetScalars()
        point_colors.Fill(0)

        _tmp = vtk_to_numpy(point_colors)
        _tmp[:] = self.color_table.values_vector

        self.data.Modified()
        self.GetMapper().UseLookupTableScalarRangeOn()
        self.GetMapper().SetLookupTable(self.color_table)
        self.GetMapper().SetScalarModeToUsePointData()
        self.GetMapper().ScalarVisibilityOff()  # Just to force color updates
        self.GetMapper().ScalarVisibilityOn()

    def configure_appearance(self):
        super().configure_appearance()
        self.GetProperty().SetSpecular(0)

    def apply_cutter(self, origin, normal):
        self.apply_cut(origin, normal)
