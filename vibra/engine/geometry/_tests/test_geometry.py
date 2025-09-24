from data.data_test_helper import get_data_path

from vibra.engine.geometry.geometry import Geometry
import numpy as np
import pytest


@pytest.fixture(scope="module")
def geometry() -> Geometry:
    path = get_data_path("examples/geometry_files/cylinder.step")
    return Geometry(path)


def test_geometry_numbers(geometry: Geometry):
    assert len(geometry.solids) == 1
    assert len(geometry.surfaces) == 4
    assert len(geometry.curves) == 6
    assert len(geometry.points) == 4


def test_geometry_measures(geometry: Geometry):
    r = 0.25
    height = 2
    circumference = 2 * np.pi * r
    circle_area = np.pi * r**2
    volume = circle_area * height
    surface_area = circle_area * 2 + circumference * height

    assert np.allclose(height, geometry.arc_length(2))
    assert np.allclose(height, geometry.arc_length(4))
    assert np.allclose(circumference / 2, geometry.arc_length(1))
    assert np.allclose(circumference / 2, geometry.arc_length(5))
    assert np.allclose(circumference, geometry.arc_length(3, 6))

    assert np.allclose(circle_area, geometry.surface_area(3))
    assert np.allclose(circle_area, geometry.surface_area(4))
    assert np.allclose(surface_area, geometry.surface_area(1, 2, 3, 4))

    assert np.allclose(volume, geometry.volume(1))


def test_geometry_straightness(geometry: Geometry):
    assert not geometry.is_surface_straight(1)
    assert not geometry.is_surface_straight(2)
    assert geometry.is_surface_straight(3)
    assert geometry.is_surface_straight(4)

    assert not geometry.is_curve_straight(1)
    assert geometry.is_curve_straight(2)
    assert not geometry.is_curve_straight(3)
    assert geometry.is_curve_straight(4)
    assert not geometry.is_curve_straight(5)
    assert not geometry.is_curve_straight(6)


def test_geometry_centers(geometry: Geometry):
    assert np.allclose(geometry.solid_center(1), (0, 1, 0))

    assert np.allclose(geometry.surface_center(1), (0.25, 1, 0))
    assert np.allclose(geometry.surface_center(2), (-0.25, 1, 0))
    assert np.allclose(geometry.surface_center(3), (0, 2, 0))
    assert np.allclose(geometry.surface_center(4), (0, 0, 0))

    assert np.allclose(geometry.curve_center(1), (0.25, 2, 0))
    assert np.allclose(geometry.curve_center(2), (0, 1, 0.25))
    assert np.allclose(geometry.curve_center(3), (0.25, 0, 0))
    assert np.allclose(geometry.curve_center(4), (0, 1, -0.25))
    assert np.allclose(geometry.curve_center(5), (-0.25, 2, 0))
    assert np.allclose(geometry.curve_center(6), (-0.25, 0, 0))

    assert np.allclose(geometry.point_center(1), (0, 2, 0.25))
    assert np.allclose(geometry.point_center(2), (0, 2, -0.25))
    assert np.allclose(geometry.point_center(3), (0, 0, 0.25))
    assert np.allclose(geometry.point_center(4), (0, 0, -0.25))


def test_convert_all_length_units(geometry: Geometry):
    geometry._curves_lengths = {1: 10.0}        # mm
    geometry._surfaces_areas = {1: 100.0}       # mm²
    geometry._solids_volumes = {1: 1000.0}      # mm³

    geometry._solids_centers = {1: np.array([10.0, 0.0, 0.0])}
    geometry._surfaces_centers = {1: np.array([0.0, 20.0, 0.0])}
    geometry._curves_centers = {1: np.array([0.0, 0.0, 30.0])}
    geometry._points_centers = {1: np.array([5.0, 5.0, 5.0])}

    geometry.set_length_unit("inch")

    assert geometry._curves_lengths[1] == 0.39370078740157477
    assert (np.isclose(geometry._surfaces_areas[1], 100*0.03937**2, atol=1e-6))
    assert (np.isclose(geometry._solids_volumes[1], 1000*0.03937**3, atol=1e-6))

    geometry._points_centers[2] = np.zeros(3)

    geometry.set_length_unit("inch")

    scale = geometry._get_length_unit_factor("millimeter") / geometry._get_length_unit_factor("inch")
    assert np.allclose(geometry._solids_centers[1], np.array([10.0, 0.0, 0.0]) * scale)
    assert np.allclose(geometry._surfaces_centers[1], np.array([0.0, 20.0, 0.0]) * scale)
    assert np.allclose(geometry._curves_centers[1], np.array([0.0, 0.0, 30.0]) * scale)
    assert np.allclose(geometry._points_centers[1], np.array([5.0, 5.0, 5.0]) * scale)
    assert np.allclose(geometry._points_centers[2], np.zeros(3))


def test_entities_relactions(geometry: Geometry):
    set1 = geometry.curves_to_points(1)
    set2 = geometry.curves_to_surfaces(1)
    set3 = geometry.curves_to_solids(1)
    set4 = geometry.surfaces_to_curves(1)
    set5 = geometry.surfaces_to_points(1)
    set6 = geometry.surfaces_to_solids(1)
    set7 = geometry.solids_to_points(1)
    set8 = geometry.solids_to_curves(1)
    set9 = geometry.solids_to_surfaces(1)

    assert (set1 == {1, 2})
    assert (set2 == {1, 3})
    assert (set3 == {1})
    assert (set4 == {1, 2, 3, 4})
    assert (set5 == {1, 2, 3, 4}) 
    assert (set6 == {1})
    assert (set7 == {1, 2, 3, 4})
    assert (set8 == {1, 2, 3, 4, 5, 6})
    assert (set9 == {1, 2, 3, 4})


def test_geometry_normals(geometry: Geometry):
    def _norm(*coords):
        return np.array(coords) / np.linalg.norm(coords)

    assert np.allclose(geometry.surface_normal(1), _norm(1, 0, 0))
    assert np.allclose(geometry.surface_normal(2), _norm(-1, 0, 0))
    assert np.allclose(geometry.surface_normal(3), _norm(0, 1, 0))
    assert np.allclose(geometry.surface_normal(4), _norm(0, -1, 0))

    assert np.allclose(geometry.curve_normal(1), _norm(1, 1, 0))
    assert np.allclose(geometry.curve_normal(2), _norm(0, 0, 1))
    assert np.allclose(geometry.curve_normal(3), _norm(1, -1, 0))
    assert np.allclose(geometry.curve_normal(4), _norm(0, 0, -1))
    assert np.allclose(geometry.curve_normal(5), _norm(-1, 1, 0))
    assert np.allclose(geometry.curve_normal(6), _norm(-1, -1, 0))

    assert np.allclose(geometry.point_normal(1), _norm(0, 1, 2))
    assert np.allclose(geometry.point_normal(2), _norm(0, 1, -2))
    assert np.allclose(geometry.point_normal(3), _norm(0, -1, 2))
    assert np.allclose(geometry.point_normal(4), _norm(0, -1, -2))


def test_geometry_relations(geometry: Geometry):
    # I hope this is correct

    # Points
    assert set(sorted(geometry.points_to_curves(1))) == {1, 2, 5}
    assert set(sorted(geometry.points_to_curves(2))) == {1, 4, 5}
    assert set(sorted(geometry.points_to_curves(3))) == {2, 3, 6}
    assert set(sorted(geometry.points_to_curves(4))) == {3, 4, 6}

    assert set(sorted(geometry.points_to_surfaces(1))) == {1, 2, 3}
    assert set(sorted(geometry.points_to_surfaces(2))) == {1, 2, 3}
    assert set(sorted(geometry.points_to_surfaces(3))) == {1, 2, 4}
    assert set(sorted(geometry.points_to_surfaces(4))) == {1, 2, 4}

    assert set(sorted(geometry.points_to_solids(1))) == {1}
    assert set(sorted(geometry.points_to_solids(2))) == {1}
    assert set(sorted(geometry.points_to_solids(3))) == {1}
    assert set(sorted(geometry.points_to_solids(4))) == {1}

    # Curves
    assert set(sorted(geometry.curves_to_points(1))) == {1, 2}
    assert set(sorted(geometry.curves_to_points(2))) == {1, 3}
    assert set(sorted(geometry.curves_to_points(3))) == {3, 4}
    assert set(sorted(geometry.curves_to_points(4))) == {2, 4}
    assert set(sorted(geometry.curves_to_points(5))) == {1, 2}
    assert set(sorted(geometry.curves_to_points(6))) == {3, 4}

    assert set(sorted(geometry.curves_to_surfaces(1))) == {1, 3}
    assert set(sorted(geometry.curves_to_surfaces(2))) == {1, 2}
    assert set(sorted(geometry.curves_to_surfaces(3))) == {1, 4}
    assert set(sorted(geometry.curves_to_surfaces(4))) == {1, 2}
    assert set(sorted(geometry.curves_to_surfaces(5))) == {2, 3}
    assert set(sorted(geometry.curves_to_surfaces(6))) == {2, 4}

    assert set(sorted(geometry.curves_to_solids(1))) == {1}
    assert set(sorted(geometry.curves_to_solids(2))) == {1}
    assert set(sorted(geometry.curves_to_solids(3))) == {1}
    assert set(sorted(geometry.curves_to_solids(4))) == {1}
    assert set(sorted(geometry.curves_to_solids(5))) == {1}
    assert set(sorted(geometry.curves_to_solids(6))) == {1}

    # Surfaces
    assert set(sorted(geometry.surfaces_to_points(1))) == {1, 2, 3, 4}
    assert set(sorted(geometry.surfaces_to_points(2))) == {1, 2, 3, 4}
    assert set(sorted(geometry.surfaces_to_points(3))) == {1, 2}
    assert set(sorted(geometry.surfaces_to_points(4))) == {3, 4}

    assert set(sorted(geometry.surfaces_to_curves(1))) == {1, 2, 3, 4}
    assert set(sorted(geometry.surfaces_to_curves(2))) == {2, 4, 5, 6}
    assert set(sorted(geometry.surfaces_to_curves(3))) == {1, 5}
    assert set(sorted(geometry.surfaces_to_curves(4))) == {3, 6}

    assert set(sorted(geometry.surfaces_to_solids(1))) == {1}
    assert set(sorted(geometry.surfaces_to_solids(2))) == {1}
    assert set(sorted(geometry.surfaces_to_solids(3))) == {1}
    assert set(sorted(geometry.surfaces_to_solids(4))) == {1}

    # Solids
    assert set(sorted(geometry.solids_to_curves(1))) == {1, 2, 3, 4, 5, 6}
    assert set(sorted(geometry.solids_to_points(1))) == {1, 2, 3, 4}
    assert set(sorted(geometry.solids_to_surfaces(1))) == {1, 2, 3, 4}
