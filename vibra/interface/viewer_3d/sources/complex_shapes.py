from vibra import SYMBOLS_DIR
from vibra.utils.polydata_utils import read_obj_file, read_stl_file, transform_polydata


def create_spring_source():
    polydata = read_stl_file(SYMBOLS_DIR / "stl_files/spring_symbol.STL")
    return transform_polydata(
        polydata,
        position=(-1.25, -0.18, 0.18),
        rotation=(0, 90, 0),
    )


def create_damper_source():
    polydata = read_obj_file(SYMBOLS_DIR / "structural/lumped_damper.obj")
    return transform_polydata(
        polydata,
        position=(-0.145, 0, 0),
    )


def create_mass_source():
    return transform_polydata(
        read_obj_file(SYMBOLS_DIR / "structural/new_lumped_mass.obj"),
        rotation=(0, -90, 0),
    )
