from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import vtkAppendPolyData
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersSources import vtkArrowSource, vtkCubeSource, vtkCylinderSource

from vibra.utils.vtk_utils import transform_polydata


def create_arrow_source():
    source = vtkArrowSource()
    source.SetTipLength(0.25)
    source.Update()

    return transform_polydata(
        source.GetOutput(),
        position=(-1.5, 0, 0),
        scale=(1.5, 1.5, 1.5),
    )

def create_pencil_source():
    source = vtkArrowSource()
    source.SetTipLength(0.25)
    source.SetTipRadius(.06)
    source.SetShaftRadius(.06)
    source.Update()

    return transform_polydata(
        source.GetOutput(),
        position=(-1, 0, 0),
        scale=(1, 1, 1),
    )

def create_quadruple_arrow_source():
    arrow = vtkArrowSource()
    arrow.SetTipLength(0.25)
    arrow.Update()
    
    pos, on_x = .2, 0
    source0 = transform_polydata(
        arrow.GetOutput(),
        position=(on_x, pos, pos),
    )
    
    source1 = transform_polydata(
        arrow.GetOutput(),
        position=(on_x, pos, -pos),
    )
    
    source2 = transform_polydata(
        arrow.GetOutput(),
        position=(on_x, -pos, pos),
    )
    
    source3 = transform_polydata(
        arrow.GetOutput(),
        position=(on_x, -pos, -pos),
    )

    source = vtkAppendPolyData()
    source.AddInputData(source0)
    source.AddInputData(source1)
    source.AddInputData(source2)
    source.AddInputData(source3)
    source.Update()
    
    return transform_polydata(
        source.GetOutput(),
        position=(-1.5, 0, 0),
        scale=(1.5, 1.5, 1.5),
    )

def create_triple_arrow_source():
    arrow = vtkArrowSource()
    arrow.SetTipLength(0.25)
    arrow.Update()
    
    pos, on_x, on_z = .2, 0, 0
    source0 = transform_polydata(
        arrow.GetOutput(),
        position=(on_x, -pos, on_z),
    )
    
    source1 = transform_polydata(
        arrow.GetOutput(),
        position=(on_x, 0, on_z),
    )
    
    source2 = transform_polydata(
        arrow.GetOutput(),
        position=(on_x, pos, on_z),
    )

    source = vtkAppendPolyData()
    source.AddInputData(source0)
    source.AddInputData(source1)
    source.AddInputData(source2)
    source.Update()
    
    return transform_polydata(
        source.GetOutput(),
        position=(-1.5, 0, 0),
        scale=(1.5, 1.5, 1.5),
    )

def create_long_arrow_source():
    source = vtkArrowSource()
    source.SetTipResolution(4)
    source.SetShaftResolution(4)
    source.SetTipLength(0.85)
    source.Update()

    return transform_polydata(
        source.GetOutput(),
        position=(-1, 0, 0),
    )


def create_double_arrow_source():
    arrow1 = vtkArrowSource()
    arrow1.SetTipLength(0.45)
    arrow1.Update()

    arrow2 = vtkArrowSource()
    arrow2.SetTipLength(0.3)
    arrow2.Update()

    source = vtkAppendPolyData()
    source.AddInputData(arrow1.GetOutput())
    source.AddInputData(arrow2.GetOutput())
    source.Update()

    return transform_polydata(
        source.GetOutput(),
        position=(-1.5, 0, 0),
        scale=(1.5, 1.5, 1.5)
    )


def create_outwards_arrow_source():
    source = vtkArrowSource()
    source.SetTipLength(0.25)
    source.Update()
    return transform_polydata(
        source.GetOutput(),
        scale=(1.5, 1.5, 1.5),
    )

def create_outwards_triple_arrow_source():
    arrow = vtkArrowSource()
    arrow.SetTipLength(0.25)
    arrow.Update()
    
    pos, on_x = .2, 0
    source0 = transform_polydata(
        arrow.GetOutput(),
        position=(on_x, pos, pos),
    )
    
    source1 = transform_polydata(
        arrow.GetOutput(),
        position=(on_x, pos, -pos),
    )
    
    source2 = transform_polydata(
        arrow.GetOutput(),
        position=(on_x, -pos, pos),
    )
    
    source3 = transform_polydata(
        arrow.GetOutput(),
        position=(on_x, -pos, -pos),
    )

    source = vtkAppendPolyData()
    source.AddInputData(source0)
    source.AddInputData(source1)
    source.AddInputData(source2)
    source.AddInputData(source3)
    source.Update()
    
    return transform_polydata(
        source.GetOutput(),
        scale=(1.5, 1.5, 1.5),
    )

def create_normal_pressure_load():
    arrow = vtkArrowSource()
    arrow.SetTipLength(0.25)
    arrow.Update()
    transform = vtkTransform()
    transform.Translate(0.06, 0, 0)
    transform_arrow = vtkTransformPolyDataFilter()
    transform_arrow.SetInputConnection(arrow.GetOutputPort())
    transform_arrow.SetTransform(transform)
    transform_arrow.Update()
    
    cylinder = vtkCylinderSource()
    cylinder.SetRadius(.3)
    cylinder.SetHeight(0.1)
    cylinder.SetResolution(50)
    cylinder.Update()
    transform = vtkTransform()
    transform.RotateZ(90)
    transform_cylinder = vtkTransformPolyDataFilter()
    transform_cylinder.SetInputConnection(cylinder.GetOutputPort())
    transform_cylinder.SetTransform(transform)
    transform_cylinder.Update()
    
    source = vtkAppendPolyData()
    source.AddInputData(transform_arrow.GetOutput())
    source.AddInputData(transform_cylinder.GetOutput())
    source.Update()
    
    return transform_polydata(
        source.GetOutput(),
        scale=(1.5, 1.5, 1.5),
    )

def create_outwards_normal_pressure_load():
    arrow = vtkArrowSource()
    arrow.SetTipLength(0.25)
    arrow.Update()
    transform = vtkTransform()
    transform.Translate(0.06, 0, 0)
    transform_arrow = vtkTransformPolyDataFilter()
    transform_arrow.SetInputConnection(arrow.GetOutputPort())
    transform_arrow.SetTransform(transform)
    transform_arrow.Update()
    
    cylinder = vtkCylinderSource()
    cylinder.SetRadius(.3)
    cylinder.SetHeight(0.1)
    cylinder.SetResolution(50)
    cylinder.Update()
    transform = vtkTransform()
    transform.RotateZ(90)
    transform_cylinder = vtkTransformPolyDataFilter()
    transform_cylinder.SetInputConnection(cylinder.GetOutputPort())
    transform_cylinder.SetTransform(transform)
    transform_cylinder.Update()
    
    source = vtkAppendPolyData()
    source.AddInputData(transform_arrow.GetOutput())
    source.AddInputData(transform_cylinder.GetOutput())
    source.Update()
    
    return transform_polydata(
        source.GetOutput(),
        position=(1.5, 0, 0),
        scale=(-1.5, 1.5, 1.5),
    )

def create_incident_plane_wave_source():
    source = vtkAppendPolyData()

    x_y_length = .5
    step = .17
    for i in range(3):
        plane = vtkCubeSource()
        plane.SetXLength(.05)
        plane.SetYLength(x_y_length)
        plane.SetZLength(x_y_length)
        plane.SetCenter(i * step + 0.05, 0, 0)
        plane.Update()
        source.AddInputData(plane.GetOutput())
    
    arrow = vtkArrowSource()
    arrow.SetTipLength(0.25)
    arrow.Update()
    
    source.AddInputData(arrow.GetOutput())
    source.Update()
    
    return transform_polydata(
        source.GetOutput(),
        position=(-1.5, 0, 0),
        scale=(1.5, 1.5, 1.5),
    )

def create_outwards_incident_plane_wave_source():
    source = vtkAppendPolyData()

    x_y_length = .5
    step = .17
    for i in range(3):
        plane = vtkCubeSource()
        plane.SetXLength(.05)
        plane.SetYLength(x_y_length)
        plane.SetZLength(x_y_length)
        plane.SetCenter(i * step + 0.05, 0, 0)
        plane.Update()
        source.AddInputData(plane.GetOutput())
    
    arrow = vtkArrowSource()
    arrow.SetTipLength(0.25)
    arrow.Update()
    
    source.AddInputData(arrow.GetOutput())
    source.Update()
    
    return transform_polydata(
        source.GetOutput(),
        position=(0, 0, 0),
        scale=(1.5, 1.5, 1.5),
    )

def create_surface_velocity_source():
    arrow = vtkArrowSource()
    arrow.SetTipLength(0.25)
    arrow.Update()
    
    cylinder = vtkCylinderSource()
    cylinder.SetRadius(.3)
    cylinder.SetHeight(0.5)
    cylinder.SetResolution(50)
    cylinder.Update()
    transform = vtkTransform()
    transform.RotateZ(90)
    transform_cylinder = vtkTransformPolyDataFilter()
    transform_cylinder.SetInputConnection(cylinder.GetOutputPort())
    transform_cylinder.SetTransform(transform)
    transform_cylinder.Update()
    
    source = vtkAppendPolyData()
    source.AddInputData(arrow.GetOutput())
    source.AddInputData(transform_cylinder.GetOutput())
    source.Update()
    
    return transform_polydata(
        source.GetOutput(),
        scale=(1.5, 1.5, 1.5),
    )