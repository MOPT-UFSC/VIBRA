from __future__ import annotations

import logging
import typing
import zipfile
from pathlib import Path
from typing import Optional

import h5py
import numpy as np
from PIL.Image import Image

from vibra.engine.analysis_info import AnalysisID, AnalysisSetup, HarmonicAnalysisSetup, ModalAnalysisSetup
from vibra.engine.assemblers import AcousticAssembler, StructuralAssembler
from vibra.engine.mesher.element_setup import ElementSetup
from vibra.engine.mesher.mesh import Mesh
from vibra.engine.mesher.mesh_setup import LocalMeshSizeControlSetup, MeshSetup
from vibra.engine.model import Model
from vibra.engine.properties import Fluid, FluidLibrary, Material, MaterialLibrary
from vibra.engine.properties.model_properties import ModelProperties
from vibra.engine.serialization.file_helpers import read_image, read_json
from vibra.engine.solution import HarmonicSolution, ModalSolution, Solution
from vibra.engine.solution.common_solution import Array2D
from vibra.engine.solvers import HarmonicSolver, ModalSolver

from .project_paths import ProjectPaths

logger = logging.getLogger(__name__)


class ProjectReader:
    """
    This class reads every component of a NewProject.

    A whole project can be loaded directly, or it can
    be loaded by part.
    """

    def __init__(self, project_paths: ProjectPaths):
        self.project_paths = project_paths

    def unpack_into_working_directory(self, vibra_path: Path | str):
        """
        This method reads the vibra file into the working directory
        defined on the constructor.

        If no working directory is defined, a temporary directory
        will be created and used.
        """
        vibra_path = Path(vibra_path)

        if not vibra_path.is_file():
            raise FileExistsError("Vibra file path does not exist.")

        logger.info(f'Reading file "{vibra_path}" into working directory "{self.project_paths.working_directory}".')

        self.project_paths.clear_data()
        with zipfile.ZipFile(vibra_path, "r") as file:
            file.extractall(path=self.project_paths.working_directory)

    def read_model(self, model: Optional[Model] = None) -> Model:
        if model is None:
            model = Model()

        logger.info("Reading the model data... (25%)")

        model.reset_variables()
        model.thumbnail = self.read_thumbnail()
        model.geometry_path = self.read_geometry_path()

        analysis_setup = self.read_analysis_setup()

        if analysis_setup is not None:
            model.set_analysis_setup(analysis_setup)

        if self.project_paths.mesh_data_filepath.exists():
            model.mesh = self.read_mesh()

        mesh_setup = self.read_mesh_setup()
        model.set_mesh_setup(mesh_setup)

        model.properties = self.read_model_properties()
        model.solution = self.read_solution(model)

        model.update_domains_mappings()

        return model

    def read_current_analysis_id(self) -> AnalysisID:
        logger.info("Reading AnalysisID")

        project_setup = read_json(self.project_paths.project_setup_filepath)
        if not isinstance(project_setup, dict):
            return AnalysisID.NO_ANALYSIS

        analysis_setup = project_setup.get("analysis_setup")
        if not isinstance(analysis_setup, dict):
            return AnalysisID.NO_ANALYSIS

        analysis_id = analysis_setup.get("analysis_id", AnalysisID.NO_ANALYSIS)
        return AnalysisID(analysis_id)

    def read_analysis_setup(self) -> Optional[AnalysisSetup]:
        logger.info("Reading AnalysisSetup")

        project_setup = read_json(self.project_paths.project_setup_filepath)
        if not isinstance(project_setup, dict):
            return None

        analysis_setup_dict = project_setup.get("analysis_setup")
        if not isinstance(analysis_setup_dict, dict):
            return None

        analysis_id = AnalysisID(analysis_setup_dict.get("analysis_id", AnalysisID.NO_ANALYSIS))
        analysis_setup_dict.update({"analysis_id": analysis_id})

        if analysis_id.is_harmonic():
            return HarmonicAnalysisSetup(**analysis_setup_dict)

        elif analysis_id.is_modal():
            return ModalAnalysisSetup(**analysis_setup_dict)

        else:
            return None

    def read_mesh_setup(self) -> Optional[MeshSetup]:
        logger.info("Reading MeshSetup.")

        project_setup = read_json(self.project_paths.project_setup_filepath)
        if not isinstance(project_setup, dict):
            return None

        mesh_setup_dict: dict = project_setup.get("mesh_setup", dict())
        if not mesh_setup_dict:
            return None

        size_controls = mesh_setup_dict.get(
            "local_mesh_size_control_parameters",
            mesh_setup_dict.get("mesh_refinement_parameters", []),
        )
        size_control_parameters = [LocalMeshSizeControlSetup(*refinement) for refinement in size_controls]

        custom_element = mesh_setup_dict.get("custom_element_setup")
        if custom_element is not None:
            custom_element = ElementSetup(**custom_element)

        if "element_type" in mesh_setup_dict.keys():
            element_geometry = mesh_setup_dict.get("element_type")
        else:
            element_geometry = mesh_setup_dict.get("element_geometry", "tetrahedral")

        if "shape_function" in mesh_setup_dict.keys():
            element_order = mesh_setup_dict.get("shape_function")
        else:
            element_order = mesh_setup_dict.get("element_order", "linear")

        mesh_setup = MeshSetup(
            minimum_element_size=mesh_setup_dict.get("minimum_element_size", 0),
            maximum_element_size=mesh_setup_dict.get("maximum_element_size", float("inf")),
            geometry_tolerance=mesh_setup_dict.get("geometry_tolerance", 1e-6),
            size_factor=mesh_setup_dict.get("size_factor", 1),
            element_geometry=element_geometry,
            element_order=element_order,
            compute_quality_metrics=mesh_setup_dict.get("compute_quality_metrics", False),
            merge_connected_volumes=mesh_setup_dict.get("merge_connected_volumes", False),
            local_mesh_size_control_parameters=size_control_parameters,
            custom_element_setup=custom_element,
            random_seed=mesh_setup_dict.get("random_seed", 1234),
        )

        return mesh_setup

    def read_geometry_path(self) -> Optional[Path]:
        logger.info("Reading geometry path.")

        project_setup = read_json(self.project_paths.project_setup_filepath)
        if not isinstance(project_setup, dict):
            return None

        geometry_filename = project_setup.get("geometry_filename")
        if geometry_filename is None:
            return None

        return self.project_paths.geometry_folder / geometry_filename

    def read_mesh(
        self,
        mesh: Optional[Mesh] = None,
    ) -> Mesh:
        mesh_data_path = self.project_paths.mesh_data_filepath
        if not mesh_data_path.exists():
            raise FileNotFoundError("The mesh file is missing.")

        geometry_data_path = self.project_paths.geometry_data_filepath
        if not geometry_data_path.exists():
            raise FileNotFoundError("The geometry file is missing.")

        if mesh is None:
            mesh = Mesh()

        cache_paths = [
            "nodal_data/cache_nodal_coordinates",
            "connectivity/cache_lines_connectivity",
            "connectivity/cache_faces_connectivity",
            "connectivity/cache_solids_connectivity",
        ]

        logger.info("Reading Mesh")
        with h5py.File(mesh_data_path, "r") as file:
            mesh.nodes_from_points = {int(key): int(value) for key, value in file["nodal_data/nodes_from_points"]}
            mesh.points_from_nodes = {value: key for key, value in mesh.nodes_from_points.items()}

            mesh.nodal_coordinates = np.array(file["nodal_data/nodal_coordinates"])
            mesh.lines_connectivity = np.array(file["connectivity/lines_connectivity"])
            mesh.faces_connectivity = np.array(file["connectivity/faces_connectivity"])
            mesh.solids_connectivity = np.array(file["connectivity/solids_connectivity"])

            curvatures = file.get("curvatures", dict())
            for key, value in curvatures.get("curvatures_surface", dict()).items():
                mesh.curvatures_surface[int(key)] = value[:]

            normals = file.get("normals", dict())
            for key, value in normals.get("normals_surface", dict()).items():
                mesh.normals_surface[int(key)] = value[:]

            if all(key in file for key in cache_paths):
                mesh.cache_nodal_coordinates = np.array(file["nodal_data/cache_nodal_coordinates"])
                mesh.cache_lines_connectivity = np.array(file["connectivity/cache_lines_connectivity"])
                mesh.cache_faces_connectivity = np.array(file["connectivity/cache_faces_connectivity"])
                mesh.cache_solids_connectivity = np.array(file["connectivity/cache_solids_connectivity"])

            mesh.process_cylindrical_surfaces()

        logger.info("Reading Geometry related Mesh informations")
        with h5py.File(geometry_data_path, "r") as file:
            for key, value in file.get("entities", dict()).items():
                mesh.geometry_information[key] = [int(val) for val in value]

            if "properties" in file:
                properties = file["properties"]
                mesh.length_from_lines = {int(k): v for k, v in properties.get("length_from_lines", default=dict())}
                mesh.area_from_surfaces = {int(k): v for k, v in properties.get("area_from_surfaces", default=dict())}
                mesh.volume_from_bodies = {int(k): v for k, v in properties.get("volume_from_bodies", default=dict())}

            for key, value in file.get("adjacencies", dict()).items():
                key: str
                tag = int(key.split("_")[-1])
                value = [int(i) for i in value]

                # This "startswith" is very sad
                if key.startswith("points_from_line"):
                    mesh.points_from_line[tag] = value

                elif key.startswith("lines_from_surface"):
                    mesh.lines_from_surface[tag] = value

                elif key.startswith("surfaces_from_volume"):
                    mesh.surfaces_from_volume[tag] = value

                elif key.startswith("cache_points_from_line"):
                    mesh.cache_points_from_line[tag] = value

                elif key.startswith("cache_lines_from_surface"):
                    mesh.cache_lines_from_surface[tag] = value

                elif key.startswith("cache_surfaces_from_volume"):
                    mesh.cache_surfaces_from_volume[tag] = value

        mesh.process_upwards_adjacencies_from_entities()
        mesh.process_mesh_related_mappings()
        mesh.update_element_topology_based_on_connectivity()
        mesh.process_disconnected_nodes_criterion()
        mesh.mesh_quality_data = self.read_mesh_quality_metrics()

        return mesh

    def read_mesh_quality_metrics(self):
        tmp = read_json(self.project_paths.mesh_quality_data_filepath)

        if tmp is None:
            return dict()

        mesh_quality_data = dict()
        for key, value in tmp.items():
            tmp_dict = dict()

            for metric, data in value.items():
                if key == "histograms_data":
                    hist, bin_edges, percentile_5, percentile_95 = data
                    tmp_dict[metric] = [
                        np.array(hist),
                        np.array(bin_edges),
                        percentile_5,
                        percentile_95,
                    ]
                else:
                    tmp_dict[metric] = np.array(data)

            mesh_quality_data[key] = tmp_dict

        return mesh_quality_data

    def read_model_properties(self, model_properties: Optional[ModelProperties] = None) -> ModelProperties:
        if model_properties is None:
            model_properties = ModelProperties()
        model_properties._reset_variables()

        logger.info("Reading ModelProperties")

        fluid_library = self.read_fluid_library()
        material_library = self.read_material_library()
        self.read_acoustic_tables()

        model_properties.fluid_library = fluid_library
        model_properties.material_library = material_library
        model_properties.acoustic_imported_tables = self.read_acoustic_tables()
        model_properties.structural_imported_tables = self.read_structural_tables()

        property_data = read_json(self.project_paths.model_properties_filepath)
        if property_data is None:
            return model_properties

        for key, data in property_data.items():
            if not isinstance(data, dict):
                continue

            for prop_key, prop_data in data.items():
                property, ids = self._property_key(prop_key)

                if property == "fluid":
                    fluid_id = prop_data.get("fluid_id")
                    prop_data = fluid_library.get(fluid_id)
                    if prop_data is None:
                        continue

                elif property == "material":
                    material_id = prop_data.get("material_id")
                    prop_data = material_library.get(material_id)
                    if prop_data is None:
                        continue

                elif property == "perforated_plate_model":
                    fluid = Fluid(**prop_data["fluid"])
                    prop_data["fluid"] = fluid

                position_kwargs = self._property_kwargs(key, ids)
                model_properties._set_property(property, prop_data, **position_kwargs)

        return model_properties

    def read_material_library(self, import_path: Path | None = None) -> MaterialLibrary:
        logger.info("Reading MaterialLibrary")

        if import_path is None:
            import_path = self.project_paths.material_library_filepath

        material_library_data = read_json(import_path)
        if material_library_data is None:
            return MaterialLibrary.default()

        material_library = MaterialLibrary()
        for material_id, material_data in material_library_data.items():
            material_id = int(material_id)
            material = Material(**material_data)
            material_library[material_id] = material

        return material_library

    def read_fluid_library(self, import_path: Path | None = None) -> FluidLibrary:
        logger.info("Reading FluidLibrary")

        if import_path is None:
            import_path = self.project_paths.fluid_library_filepath

        fluid_library_data = read_json(import_path)
        if fluid_library_data is None:
            return FluidLibrary.default()

        fluid_library = FluidLibrary()
        for fluid_id, fluid_data in fluid_library_data.items():
            fluid_id = int(fluid_id)
            fluid = Fluid(**fluid_data)
            fluid_library[fluid_id] = fluid

        return fluid_library

    def read_acoustic_tables(self) -> dict[str, np.ndarray]:
        tables = dict()

        table_data_path = self.project_paths.imported_table_data_filepath
        if not table_data_path.exists():
            return tables

        with h5py.File(table_data_path, "r") as file:
            if "acoustic" not in file:
                return tables

            for name, dataset in file["acoustic"].items():
                tables[name] = np.array(dataset)

        return tables

    def read_structural_tables(self) -> dict[str, np.ndarray]:
        tables = dict()

        table_data_path = self.project_paths.imported_table_data_filepath
        if not table_data_path.exists():
            return tables

        with h5py.File(table_data_path, "r") as file:
            if "structural" not in file:
                return tables

            for name, dataset in file["structural"].items():
                tables[name] = np.array(dataset)

        return tables

    def read_thumbnail(self) -> Optional[Image]:
        if not self.project_paths.thumbnail_filepath.exists():
            return None

        logger.info("Reading Thumbnail")

        return read_image(self.project_paths.thumbnail_filepath)

    def read_solution(self, model: Model) -> Optional[Solution]:
        if model.analysis_id.is_harmonic():
            return self.read_harmonic_solution(model)
        elif model.analysis_id.is_modal():
            return self.read_modal_solution(model)
        else:
            return None

    def read_harmonic_solution(self, model: Model) -> Optional[HarmonicSolution]:
        if not self.project_paths.harmonic_solution_filepath.exists():
            return None

        with h5py.File(self.project_paths.harmonic_solution_filepath, "r") as file:
            file: h5py.File

            logger.info("Reading harmonic solution [5/100]")

            frequencies = np.array(file["frequencies"])
            logger.info("Reading harmonic solution [20/100]")

            solution_status = np.array(file["solution_status"])
            logger.info("Reading harmonic solution [80/100]")

            displacement_dof = file.get("displacement_dof")
            if displacement_dof is not None:
                displacement_dof = np.array(displacement_dof)
            logger.info("Reading harmonic solution [90/100]")

            structural_solution = file.get("structural_solution")
            acoustic_solution = file.get("acoustic_solution")
            coupled_solution = file.get("coupled_solution")
            logger.info("Reading harmonic solution [95/100]")

            if all(s is None for s in [structural_solution, acoustic_solution, coupled_solution]):
                # Remove after version 0.8
                solution = file.get("solution")
                if solution is None:
                    raise ValueError("No solution found")
                logger.warning("This file is deprecated and will not be supported after version 0.8")

                if model.analysis_id.is_structural():
                    return HarmonicSolution(
                        analysis_id=model.analysis_id,
                        frequencies=frequencies,
                        structural_solution=solution,
                        status=solution_status,
                        displacement_dof=displacement_dof,
                    )

                elif model.analysis_id.is_acoustic():
                    return HarmonicSolution(
                        analysis_id=model.analysis_id,
                        frequencies=frequencies,
                        acoustic_solution=solution,
                        status=solution_status,
                    )

                else:
                    raise ValueError("Invalid analysis")

            else:
                # Keep only this part after version 0.8
                return HarmonicSolution(
                    analysis_id=model.analysis_id,
                    frequencies=frequencies,
                    structural_solution=structural_solution,
                    acoustic_solution=acoustic_solution,
                    coupled_solution=coupled_solution,
                    status=solution_status,
                    displacement_dof=displacement_dof,
                )

    def read_modal_solution(self, model: Model) -> Optional[ModalSolution]:
        if not self.project_paths.modal_solution_filepath.exists():
            return None

        with h5py.File(self.project_paths.modal_solution_filepath, "r") as file:
            file: h5py.File

            structural_modal_shapes = file.get("structural_modal_shapes")
            acoustic_modal_shapes = file.get("acoustic_modal_shapes")
            coupled_modal_shapes = file.get("coupled_modal_shapes")

            if all(s is None for s in [structural_modal_shapes, acoustic_modal_shapes, coupled_modal_shapes]):
                # Remove after version 0.8

                solution = file.get("solution")
                if solution is None:
                    raise ValueError("No solution found")
                logger.warning("This file is deprecated and will not be supported after version 0.8")

                solution = np.array(solution)

                if model.analysis_id.is_structural():
                    return ModalSolution(
                        analysis_id=model.analysis_id,
                        natural_frequencies=file["frequencies"],
                        structural_modal_shapes=solution,
                        displacement_dof=file.get("displacement_dof"),
                        complex_natural_frequencies=file.get("complex_natural_frequencies"),
                    )

                elif model.analysis_id.is_acoustic():
                    return ModalSolution(
                        analysis_id=model.analysis_id,
                        natural_frequencies=file["frequencies"],
                        acoustic_modal_shapes=solution,
                        complex_natural_frequencies=file.get("complex_natural_frequencies"),
                    )

                else:
                    raise ValueError("Invalid analysis")

            else:
                # Keep only this part after version 0.8
                return ModalSolution(
                    analysis_id=model.analysis_id,
                    natural_frequencies=file["frequencies"],
                    structural_modal_shapes=file["structural_modal_shapes"],
                    acoustic_modal_shapes=file["acoustic_modal_shapes"],
                    coupled_modal_shapes=file["coupled_modal_shapes"],
                    displacement_dof=file.get("displacement_dof"),
                    complex_natural_frequencies=file.get("complex_natural_frequencies"),
                )

    def read_assembler_and_solver(self, model: Model) -> tuple[AcousticAssembler | StructuralAssembler | None, HarmonicSolver | ModalSolver | None]:

        # TODO: create Solution classes, so we don't need to create pointless Assemblers and Solvers here
        logger.info("Reading Solution.")

        if model.analysis_id.is_acoustic():
            assembler = AcousticAssembler(model)
        elif model.analysis_id.is_structural():
            assembler = StructuralAssembler(model)
        else:
            return None, None

        if model.analysis_id.is_harmonic():
            solver = HarmonicSolver(assembler)
            solver.solution = model.solution
        elif model.analysis_id.is_modal():
            solver = ModalSolver(assembler)
            solver.solution = model.solution
        else:
            return None, None

        return assembler, solver

    def _property_key(self, str: str) -> tuple[str, int | tuple[int, ...]]:
        """
        According to the way the properties are organized in the file,
        a property named "my_property" set on volume 8, for example will look like

            "volume_properties": {
                "my_property 8": {
                    ...
                }
            }
        }

        This function transforms the string "my_property 8" to

        ("my_property", 8)
        """

        property, *_ids = str.split()
        property = property.strip()

        if len(_ids) == 1:
            ids = int(_ids[0])
        else:
            ids = tuple([int(_id) for _id in _ids])

        return property, ids

    @typing.overload
    def _property_kwargs(self, key: str, id: tuple[int, ...]) -> dict[str, tuple[int]]: ...

    @typing.overload
    def _property_kwargs(self, key: str, id: int) -> dict[str, int]: ...

    def _property_kwargs(self, key, id):
        """
        In the file the properties are stored as keys of a dict.
        But in the model property class, for some reason.
        """

        match key:
            case "volume_properties":
                return dict(volume=id)
            case "group_properties":
                return dict(group=id)
            case "surface_properties":
                return dict(surface=id)
            case "line_properties":
                return dict(line=id)
            case "point_properties":
                return dict(point=id)
            case "element_properties":
                return dict(element=id)
            case "nodal_properties":
                return dict(node=id)
            case _:
                return dict()
