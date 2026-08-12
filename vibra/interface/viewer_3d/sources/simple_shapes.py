from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import vtkAppendPolyData
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkCubeSource,
    vtkCylinderSource,
    vtkPlaneSource,
    vtkSphereSource,
)

from vibra.utils.vtk_utils import transform_polydata


def create_cone_source():
    source = vtkConeSource()
    source.SetHeight(1)
    source.SetRadius(0.5)
    source.SetResolution(12)
    source.Update()
    s = 0.6
    return transform_polydata(source.GetOutput(), position=(-s / 2, 0, 0), scale=(s, s, s))


def create_axis_source(shift=0):
    source = vtkCylinderSource()
    source.SetResolution(12)
    source.SetRadius(0.15)
    source.SetHeight(0.1)
    source.Update()
    return transform_polydata(
        source.GetOutput(),
        rotation=(0, 0, 90),
        position=(shift, 0, 0),
    )


def create_double_cone_source():
    cone1 = vtkConeSource()
    cone1.SetHeight(0.3)
    cone1.SetRadius(0.6)
    cone1.SetResolution(12)
    cone1.Update()

    cone2 = vtkConeSource()
    cone2.SetHeight(0.3)
    cone2.SetRadius(0.6)
    cone2.SetResolution(12)
    cone2.Update()

    transform = vtkTransform()
    transform.Translate(-0.2, 0, 0)

    transformFilter = vtkTransformPolyDataFilter()
    transformFilter.SetInputConnection(cone2.GetOutputPort())
    transformFilter.SetTransform(transform)
    transformFilter.Update()

    source = vtkAppendPolyData()
    source.AddInputData(cone1.GetOutput())
    source.AddInputData(transformFilter.GetOutput())
    source.Update()
    s = 0.6
    return transform_polydata(source.GetOutput(), position=(-s / 2, 0, 0), scale=(s, s, s))


def create_cube_source():
    source = vtkCubeSource()
    source.SetBounds(0, 1, 0, 1, 0, 1)
    source.Update()
    return source.GetOutput()


def create_plane_source():
    source = vtkPlaneSource()
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
    return transform_polydata(get_sphere_source(1).GetOutput(), scale=(0.3, 0.3, 0.3))


def create_mass_load_second_layer_source():
    return transform_polydata(get_sphere_source(1.5).GetOutput(), scale=(0.3, 0.3, 0.3))


def create_mass_load_third_layer_source():
    return transform_polydata(get_sphere_source(2).GetOutput(), scale=(0.3, 0.3, 0.3))


def create_mass_load_fourth_layer_source():
    return transform_polydata(get_sphere_source(2.5).GetOutput(), scale=(0.3, 0.3, 0.3))
