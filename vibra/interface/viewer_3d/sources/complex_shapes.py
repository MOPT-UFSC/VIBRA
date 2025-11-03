from vibra import SYMBOLS_DIR
from vibra.utils.vtk_utils import read_obj_file, read_stl_file, transform_polydata


def create_spring_source():
    polydata = read_stl_file(SYMBOLS_DIR / "stl_files/spring_symbol.stl")
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
    polydata = read_stl_file(SYMBOLS_DIR / "stl_files/specific_impedance_symbol.stl")
    return transform_polydata(
        polydata,
        rotation=(0, 90, 180),
        scale=(1, 1, 1),
    )

def create_anechoic_termination_source():
    polydata = read_stl_file(SYMBOLS_DIR / "stl_files/anechoic_termination_symbol.stl")
    return transform_polydata(
        polydata,
        rotation=(0, 90, 180),
        scale=(1, 1, 1),
    )

def create_transfer_impedance_source():
    polydata = read_stl_file(SYMBOLS_DIR / "stl_files/transfer_impedance_symbol.stl")
    return transform_polydata(
        polydata,
        rotation=(0, 90, 0),
        scale=(1, 1, 1),
    )

def create_mass_flow_rate_source():
    polydata = read_stl_file(SYMBOLS_DIR / "stl_files/mass_flow_rate_symbol.stl")
    return transform_polydata(
        polydata,
        rotation=(0, 90, 180),
        scale=(2, 2, 2),
    )

def create_degrees_of_freedom_decoupling_source():
    polydata = read_stl_file(SYMBOLS_DIR / "stl_files/degrees_of_freedom_decoupling_symbol.stl")
    return transform_polydata(
        polydata,
        rotation=(0, 90, 0),
        scale=(.5, .5, .5),
    )

def create_absorption_surface_source():
    polydata = read_stl_file(SYMBOLS_DIR / "stl_files/absorption_surface_symbol.stl")
    return transform_polydata(
        polydata,
        rotation=(0, 90, 180),
        scale=(2.3, 2.3, 2.3),
    )

def create_acoustic_pressure_source():
    polydata = read_stl_file(SYMBOLS_DIR / "stl_files/acoustic_pressure_symbol.stl")
    return transform_polydata(
        polydata,
        rotation=(0, 90, 180),
        scale=(.03, .03, .03),
    )

def create_compressor_discharge_source():
    polydata = read_stl_file(SYMBOLS_DIR / "stl_files/compressor_discharge.stl")
    return transform_polydata(
        polydata,
        rotation=(0, 0, 180),
        scale=(1, 1, 1),
        position=(1, 0, 0),
    )

def create_compressor_suction_source():
    polydata = read_stl_file(SYMBOLS_DIR / "stl_files/compressor_suction.stl")
    return transform_polydata(
        polydata,
        rotation=(0, 0, 180),
        scale=(1, 1, 1),
        position=(1, 0, 0)
    )   

def create_dissipation_model_source():
    polydata = read_stl_file(SYMBOLS_DIR / "stl_files/dissipation_model_symbol.stl")
    return transform_polydata(
        polydata,
        scale=(.5, .5, .5),
    )

def create_acoustic_transfer_element_data_source():
    polydata = read_stl_file(SYMBOLS_DIR / "stl_files/acoustic_transfer_element_data_symbol.stl")
    return transform_polydata(
        polydata,
        rotation=(0, 90, 180),
        scale=(1, 1, 1),
    )

def create_dof_cone_rotation_source():
    polydata = read_stl_file(SYMBOLS_DIR / "stl_files/dof_cone_rotation.stl")
    return transform_polydata(
        polydata,
        position=(0, 0, 0),
        rotation=(0, 0, -90),
        scale=(.4, .4, .4),
    )

def create_dof_cone_source():
    polydata = read_stl_file(SYMBOLS_DIR / "stl_files/dof_cone.stl")
    return transform_polydata(
        polydata,
        position=(0, 0, 0),
        rotation=(0, 0, -90),
        scale=(.4, .4, .4),
    )

def create_nodal_loads_momentum_arrow_source():
    polydata = read_stl_file(SYMBOLS_DIR / "stl_files/momentum_double_arrow.stl")
    return transform_polydata(
        polydata,
        position=(0, 0, 0),
        rotation=(90, 0, -90),
        scale=(.15, .15, .15),
    )

def create_nodal_loads_force_arrow_source():
    polydata = read_stl_file(SYMBOLS_DIR / "stl_files/force_arrow.stl")
    return transform_polydata(
        polydata,
        position=(0, 0, 0),
        rotation=(90, 0, -90),
        scale=(.15, .15, .15),
    )