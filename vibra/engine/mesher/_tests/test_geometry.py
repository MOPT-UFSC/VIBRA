from data.data_test_helper import get_data_path

from vibra.engine.mesher.geometry import Geometry


def test_cilinder():
    path = get_data_path("examples/geometry_files/cylinder.step")

    geometry = Geometry(path)



def test_cube():
    pass
