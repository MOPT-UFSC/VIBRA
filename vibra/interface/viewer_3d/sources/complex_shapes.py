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

def create_perforated_plate_source():
    polydata = read_obj_file(SYMBOLS_DIR / "acoustic/perforated_plate_many_holes.obj")
    return transform_polydata(
        polydata,
        rotation=(0, 0, 90),
        scale=(0.1, 1, 1),
    )

def create_impedance_source():
    polydata = read_stl_file(SYMBOLS_DIR / "stl_files/impedance_symbol.STL")
    return transform_polydata(
        polydata,
        rotation=(0, 90, 0),
        scale=(2, 2, 2),
    )