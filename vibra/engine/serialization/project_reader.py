from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    # This is to avoid circular imports since
    # this file is also imported by NewProject
    from vibra.engine.new_project import NewProject

import typing
import zipfile
from pathlib import Path

import h5py
import numpy as np
from PIL.Image import Image

from vibra.engine.analysis_info import (
    AnalysisID,
    AnalysisSetup,
    FrequencySpacing,
    HarmonicAnalysisSetupList,
    HarmonicAnalysisSetupRange,
    ModalAnalysisSetup,
)
from vibra.engine.assemblers import AcousticAssembler, StructuralAssembler
from vibra.engine.mesher.mesh import Mesh
from vibra.engine.mesher.mesh_setup import MeshSetup
from vibra.engine.model import Model
from vibra.engine.properties import (
    Fluid,
    FluidLibrary,
    Material,
    MaterialLibrary,
)
from vibra.engine.properties.model_properties import ModelProperties
from vibra.engine.serialization.file_helpers import read_image, read_json
from vibra.engine.solvers import HarmonicSolver, ModalSolver
from vibra.project_files.lazy_hdf5_matrix import LazyHDF5MatrixLoader

from .project_paths import ProjectPaths


class ProjectReader:
    """
    This class reads every component of a NewProject.

    A whole project can be loaded directly, or it can
    be loaded by part.
    """

    def __init__(self, project_paths: ProjectPaths):
        self.project_paths = project_paths

    def read_file(self, vibra_path: Path | str):
        """
        This method reads the vibra file into the working directory
        defined on the constructor.

        If no working directory is defined, a temporary directory
        will be created and used.
        """
        vibra_path = Path(vibra_path)

        if not vibra_path.is_file():
            raise FileExistsError("Vibra file path does not exist.")

        logging.info(f'Reading file "{vibra_path}" into working directory "{self.project_paths.working_directory}".')

        self.project_paths.clear_data()
        with zipfile.ZipFile(vibra_path, "r") as file:
            file.extractall(path=self.project_paths.working_directory)

    def read_project(self, project: Optional[NewProject] = None) -> NewProject:
        if project is None:
            # This is to avoid circular imports since
            # this file is imported by NewProject
            from vibra.engine.new_project import NewProject

            project = NewProject()

        logging.info("Reading project.")

        project.reset_variables()
        project.model = self.read_model(project.model)
        project.assembler, project.solver = self.read_assembler_and_solver(project.model)

        return project

    def read_model(self, model: Optional[Model] = None) -> Model:
        if model is None:
            model = Model()

        logging.info("Reading model.")

        model.reset_variables()
        model.thumbnail = self.read_thumbnail()
        model.analysis_id = self.read_current_analysis_id()

        analysis_setup = self.read_analysis_setup()
        if analysis_setup is not None:
            model.new_set_analysis_setup(analysis_setup)

        model.mesh_setup = self.read_mesh_setup()
        model.properties = self.read_model_properties()
        model.geometry_path = self.read_geometry_path()

        if self.project_paths.mesh_data_filepath.exists():
            model.mesh = self.read_mesh()

        return model

    def read_current_analysis_id(self) -> AnalysisID:
        logging.info("Reading AnalysisID")

        project_setup = read_json(self.project_paths.project_setup_filepath)
        if not isinstance(project_setup, dict):
            return AnalysisID.NO_ANALYSIS

        analysis_setup = project_setup.get("analysis_setup")
        if not isinstance(analysis_setup, dict):
            return AnalysisID.NO_ANALYSIS

        analysis_id = analysis_setup.get("analysis_id", AnalysisID.NO_ANALYSIS)
        return AnalysisID(analysis_id)

    def read_analysis_setup(self) -> Optional[AnalysisSetup]:
        logging.info("Reading AnalysisSetup")

        project_setup = read_json(self.project_paths.project_setup_filepath)
        if not isinstance(project_setup, dict):
            return None

        analysis_setup_dict = project_setup.get("analysis_setup")
        if not isinstance(analysis_setup_dict, dict):
            return None

        analysis_id = AnalysisID(analysis_setup_dict.get("analysis_id", AnalysisID.NO_ANALYSIS))

        if analysis_id.is_harmonic():
            frequency_spacing = analysis_setup_dict.get(
                "frequency_spacing",
                FrequencySpacing.EQUALLY_DISTRIBUTED,
            )

            match frequency_spacing:
                case FrequencySpacing.EQUALLY_DISTRIBUTED:
                    return HarmonicAnalysisSetupRange(
                        f_min=analysis_setup_dict.get("f_min", 0),
                        f_max=analysis_setup_dict.get("f_max", 0),
                        f_step=analysis_setup_dict.get("f_step", 0),
                        analysis_method=analysis_setup_dict.get("analysis_method", "direct"),
                        global_damping=analysis_setup_dict.get("global_damping", (0, 0, 0)),
                        modes_number=analysis_setup_dict.get("modes_number", None),
                    )
                case FrequencySpacing.USER_DEFINED:
                    return HarmonicAnalysisSetupList(
                        analysis_setup_dict.get("frequencies", []),
                        analysis_setup_dict.get("solution_steps_mask"),
                        analysis_method=analysis_setup_dict.get("analysis_method", "direct"),
                        global_damping=analysis_setup_dict.get("global_damping", (0, 0, 0)),
                        modes_number=analysis_setup_dict.get("modes_number", None),
                    )

        elif analysis_id.is_modal():
            return ModalAnalysisSetup(
                modes_number=analysis_setup_dict.get("modes_number", 0),
                sigma_factor=analysis_setup_dict.get("sigma_factor", 0),
            )

        else:
            return None

    def read_mesh_setup(self) -> MeshSetup:
        logging.info("Reading MeshSetup.")

        project_setup = read_json(self.project_paths.project_setup_filepath)
        if not isinstance(project_setup, dict):
            project_setup = dict()

        mesh_setup = MeshSetup()
        for key, value in project_setup.get("mesh_setup", dict()).items():
            setattr(mesh_setup, key, value)

        return mesh_setup

    def read_geometry_path(self) -> Optional[Path]:
        logging.info("Reading geometry path.")

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

        logging.info("Reading Mesh")
        with h5py.File(mesh_data_path, "r") as file:
            mesh.nodes_from_points = {int(key): int(value) for key, value in file["nodal_data/nodes_from_points"]}
            mesh.points_from_nodes = {value: key for key, value in mesh.nodes_from_points.items()}

            mesh.nodal_coordinates = np.array(file["nodal_data/nodal_coordinates"])
            mesh.lines_connectivity = np.array(file["connectivity/lines_connectivity"])
            mesh.faces_connectivity = np.array(file["connectivity/faces_connectivity"])
            mesh.solids_connectivity = np.array(file["connectivity/solids_connectivity"])

            if all(key in file for key in cache_paths):
                mesh.cache_nodal_coordinates = np.array(file["nodal_data/cache_nodal_coordinates"])
                mesh.cache_lines_connectivity = np.array(file["connectivity/cache_lines_connectivity"])
                mesh.cache_faces_connectivity = np.array(file["connectivity/cache_faces_connectivity"])
                mesh.cache_solids_connectivity = np.array(file["connectivity/cache_solids_connectivity"])

        logging.info("Reading Geometry related Mesh informations")
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

        return mesh

    def read_model_properties(self, model_properties: Optional[ModelProperties] = None) -> ModelProperties:
        if model_properties is None:
            model_properties = ModelProperties()
        model_properties._reset_variables()

        logging.info("Reading ModelProperties")

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

    def read_material_library(self) -> MaterialLibrary:
        logging.info("Reading MaterialLibrary")

        material_library_data = read_json(self.project_paths.material_library_filepath)
        if material_library_data is None:
            return MaterialLibrary.default()

        material_library = MaterialLibrary()
        for material_id, material_data in material_library_data.items():
            material_id = int(material_id)
            material = Material(**material_data)
            material_library[material_id] = material

        return material_library

    def read_fluid_library(self) -> FluidLibrary:
        logging.info("Reading FluidLibrary")

        fluid_library_data = read_json(self.project_paths.fluid_library_filepath)
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

        logging.info("Reading Thumbnail")

        return read_image(self.project_paths.thumbnail_filepath)

    def read_assembler_and_solver(self, model: Model) -> tuple[AcousticAssembler | StructuralAssembler | None, HarmonicSolver | ModalSolver | None]:

        # TODO: create Solution classes, so we don't need to create pointless Assemblers and Solvers here
        logging.info("Reading Solution.")

        if model.analysis_id.is_acoustic():
            assembler = AcousticAssembler(model)
        elif model.analysis_id.is_structural():
            assembler = StructuralAssembler(model)
        else:
            return None, None

        if model.analysis_id.is_harmonic():
            solver = HarmonicSolver(assembler)
            if self.project_paths.harmonic_solution_filepath.exists():
                solver.solution = LazyHDF5MatrixLoader(self.project_paths.harmonic_solution_filepath)

        elif model.analysis_id.is_modal():
            solver = ModalSolver(assembler)
            if self.project_paths.modal_solution_filepath.exists():
                solver.solution = LazyHDF5MatrixLoader(self.project_paths.modal_solution_filepath)

        else:
            return None, None

        return assembler, solver

    def get_solution_loader(self) -> Optional[LazyHDF5MatrixLoader]:
        if not self.project_paths.harmonic_solution_filepath.exists():
            return None
        return LazyHDF5MatrixLoader(self.project_paths.harmonic_solution_filepath)

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
