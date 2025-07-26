from vibra.utils.polydata_utils import transform_polydata
from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkCubeSource,
    vtkSphereSource,
)
from vtkmodules.vtkFiltersCore import vtkAppendPolyData

def create_cone_source():
    source = vtkConeSource()
    source.SetHeight(1)
    source.SetRadius(0.5)
    source.SetResolution(12)
    source.Update()
    s = 0.6
    return transform_polydata(
        source.GetOutput(),
        position=(-s/2, 0, 0),
        scale=(s, s, s)
    )

def create_cube_source():
    source = vtkCubeSource()
    source.SetBounds(0, 1, 0, 1, 0, 1)
    source.Update()
    return source.GetOutput()

def get_sphere_source(raio: float = 1.0):
        esfera = vtkSphereSource()
        esfera.SetRadius(raio)
        esfera.SetThetaResolution(64)
        esfera.SetPhiResolution(64)
        esfera.Update()
        return esfera

def create_mass_load_first_layer_source():
    return transform_polydata(
        get_sphere_source(1).GetOutput(),
        scale=(0.3, 0.3, 0.3)
    )

def create_mass_load_second_layer_source():
    return transform_polydata(
        get_sphere_source(1.5).GetOutput(),
        scale=(0.3, 0.3, 0.3)
    )

def create_mass_load_third_layer_source():
    return transform_polydata(
        get_sphere_source(2).GetOutput(),
        scale=(0.3, 0.3, 0.3)
    )

def create_mass_load_fourth_layer_source():
    return transform_polydata(
        get_sphere_source(2.5).GetOutput(),
        scale=(0.3, 0.3, 0.3)
    )