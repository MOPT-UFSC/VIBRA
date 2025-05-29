from vtkmodules.vtkFiltersSources import vtkArrowSource
from vtkmodules.vtkFiltersCore import vtkAppendPolyData
from vibra.utils.polydata_utils import transform_polydata


def create_arrow_source():
    source = vtkArrowSource()
    source.SetTipLength(0.25)
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
    
    pos, on_x = .15, 0
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
        position=(0, 0, 0),
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
        position=(-1, 0, 0),
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
    
    pos, on_x = .15, 0
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