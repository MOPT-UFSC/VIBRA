from pathlib import Path

import numpy as np

from vibra import PROJECT_DIR
from vibra.engine.analysis_info import AnalysisID, FrequencySpacing
from vibra.engine.mesher.geometry_info import GeometryInfo
from vibra.engine.mesher.mesh_setup import MeshSetup
from vibra.engine.project import Project
from vibra.engine.serialization.project_paths import ProjectPaths
from vibra.engine.serialization.project_reader import ProjectReader
from vibra.engine.serialization.project_writer import ProjectWriter


def test_geometry_info_write_and_read_round_trip(datadir: Path):
    paths = ProjectPaths(datadir / "geometry_info_round_trip")
    geometry_info = GeometryInfo()
    geometry_info.points = [1, 2]
    geometry_info.curves = [3]
    geometry_info.surfaces = [4]
    geometry_info.solids = [5]

    geometry_info._solids_to_surfaces[5] = [4]
    geometry_info._surfaces_to_curves[4] = [3]
    geometry_info._curves_to_points[3] = [1, 2]
    geometry_info._cache_solids_to_surfaces[5] = [4]
    geometry_info._cache_surfaces_to_curves[4] = [3]
    geometry_info._cache_curves_to_points[3] = [1, 2]

    geometry_info._solids_centers[5] = [1.0, 2.0, 3.0]
    geometry_info._surfaces_centers[4] = [4.0, 5.0, 6.0]
    geometry_info._curves_centers[3] = [7.0, 8.0, 9.0]
    geometry_info._points_centers[1] = [10.0, 11.0, 12.0]
    geometry_info._points_centers[2] = [13.0, 14.0, 15.0]

    geometry_info._surfaces_normals[4] = [0.0, 0.0, 1.0]
    geometry_info._solids_volumes[5] = 16.0
    geometry_info._surfaces_areas[4] = 17.0
    geometry_info._curves_lengths[3] = 18.0
    geometry_info._bounding_solids[5] = [0.0, 0.0, 0.0, 1.0, 1.0, 1.0]
    geometry_info._bounding_surfaces[4] = [0.0, 0.0, 0.0, 1.0, 1.0, 0.0]
    geometry_info._bounding_curves[3] = [0.0, 0.0, 0.0, 1.0, 0.0, 0.0]
    geometry_info._straight_curves = {3}
    geometry_info._straight_surfaces = {4}
    geometry_info._create_inverse_maps()

    ProjectWriter(paths).write_geometry_info(geometry_info)
    loaded_geometry_info = ProjectReader(paths).read_geometry_info()

    assert loaded_geometry_info.points == geometry_info.points
    assert loaded_geometry_info.curves == geometry_info.curves
    assert loaded_geometry_info.surfaces == geometry_info.surfaces
    assert loaded_geometry_info.solids == geometry_info.solids
    assert loaded_geometry_info._solids_to_surfaces == geometry_info._solids_to_surfaces
    assert loaded_geometry_info._surfaces_to_curves == geometry_info._surfaces_to_curves
    assert loaded_geometry_info._curves_to_points == geometry_info._curves_to_points
    assert loaded_geometry_info._cache_solids_to_surfaces == geometry_info._cache_solids_to_surfaces
    assert loaded_geometry_info._cache_surfaces_to_curves == geometry_info._cache_surfaces_to_curves
    assert loaded_geometry_info._cache_curves_to_points == geometry_info._cache_curves_to_points
    assert loaded_geometry_info._surfaces_to_solids == geometry_info._surfaces_to_solids
    assert loaded_geometry_info._curves_to_surfaces == geometry_info._curves_to_surfaces
    assert loaded_geometry_info._points_to_curves == geometry_info._points_to_curves
    assert loaded_geometry_info._solids_volumes == geometry_info._solids_volumes
    assert loaded_geometry_info._surfaces_areas == geometry_info._surfaces_areas
    assert loaded_geometry_info._curves_lengths == geometry_info._curves_lengths
    assert loaded_geometry_info._straight_curves == geometry_info._straight_curves
    assert loaded_geometry_info._straight_surfaces == geometry_info._straight_surfaces

    for original, loaded in (
        (geometry_info._solids_centers, loaded_geometry_info._solids_centers),
        (geometry_info._surfaces_centers, loaded_geometry_info._surfaces_centers),
        (geometry_info._curves_centers, loaded_geometry_info._curves_centers),
        (geometry_info._points_centers, loaded_geometry_info._points_centers),
        (geometry_info._surfaces_normals, loaded_geometry_info._surfaces_normals),
        (geometry_info._bounding_solids, loaded_geometry_info._bounding_solids),
        (geometry_info._bounding_surfaces, loaded_geometry_info._bounding_surfaces),
        (geometry_info._bounding_curves, loaded_geometry_info._bounding_curves),
    ):
        assert original.keys() == loaded.keys()
        for entity_id in original:
            np.testing.assert_array_equal(loaded[entity_id], original[entity_id])


def test_write_and_read_acoustic_project(fluid, datadir: Path):
    geometry_path = PROJECT_DIR / "examples/geometry_files/cylinder.step"
    project_path = datadir / "project.vibra"

    mesh_setup = MeshSetup(
        minimum_element_size=50,
        maximum_element_size=50,
    )

    data_Vn = {
        "real_values": [1.0],
        "imag_values": [0.0],
        "element_integration": False,
    }

    project_a = Project()
    project_a.import_geometry(geometry_path)
    # project_a.configure_mesh()
    project_a.generate_mesh(mesh_setup)

    project_a.model.properties._set_property("fluid", fluid, volume=1)
    project_a.model.properties._set_property("fluid", fluid, volume=2)
    project_a.model.properties._set_property("fluid", fluid, surface=1)
    project_a.model.properties._set_property("surface_velocity", data_Vn, surface=1)

    ## Define the analysis frequency setup
    analysis_setup = project_a.model.get_harmonic_analysis_setup(
        frequency_spacing=FrequencySpacing.EQUALLY_DISTRIBUTED,
        analysis_id=AnalysisID.ACOUSTIC_HARMONIC,
        f_min=100,
        f_max=500,
        f_step=200,
    )

    project_a.configure_analysis(analysis_setup)
    solution_a = project_a.solve_acoustic_harmonic_analysis()
    project_a.save_project(project_path)

    project_b = Project()
    project_b.load_project(project_path)
    solution_b = project_b.model.solution

    project_path.unlink()
    assert solution_a == solution_b


def test_write_and_read_structural_project(material, datadir: Path):
    geometry_path = PROJECT_DIR / "examples/geometry_files/cylinder.step"
    project_path = datadir / "project.vibra"

    mesh_setup = MeshSetup(
        minimum_element_size=50,
        maximum_element_size=50,
    )

    data_prescribed_dofs = {
        "element_type": "3d_element",
        "real_values": [0, 0, 0],
        "imag_values": [0, 0, 0],
    }

    data_load = {
        "element_type": "3d_element",
        "real_values": [1, 0, 0],
        "imag_values": [0, 0, 0],
        "element_integration": True,
    }

    project_a = Project()
    project_a.import_geometry(geometry_path)
    # project_a.configure_mesh()
    project_a.generate_mesh(mesh_setup)

    project_a.model.properties._set_property("material", material, volume=1)
    project_a.model.properties._set_property("material", material, volume=2)
    project_a.model.properties._set_property("material", material, surface=1)
    project_a.model.properties._set_property("prescribed_dof", data_prescribed_dofs, surface=3)
    project_a.model.properties._set_property("nodal_loads", data_load, surface=4)

    ## Define the analysis frequency setup
    analysis_setup = project_a.model.get_harmonic_analysis_setup(
        frequency_spacing=FrequencySpacing.EQUALLY_DISTRIBUTED,
        analysis_id=AnalysisID.STRUCTURAL_HARMONIC,
        f_min=100,
        f_max=500,
        f_step=200,
    )

    project_a.configure_analysis(analysis_setup)
    solution_a = project_a.run_analysis()
    project_a.save_project(project_path)

    project_b = Project()
    project_b.load_project(project_path)
    solution_b = project_b.model.solution

    project_path.unlink()
    assert solution_a == solution_b
