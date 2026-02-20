from __future__ import annotations

import logging
import shutil
import zipfile
from dataclasses import asdict
from pathlib import Path
from typing import TYPE_CHECKING, Optional

import h5py
import numpy as np
from PIL import Image

if TYPE_CHECKING:
    # This is to avoid circular imports since
    # this file is imported by NewProject
    from vibra.engine.new_project import NewProject

from vibra.engine.analysis_info import HarmonicAnalysisSetup, ModalAnalysisSetup
from vibra.engine.mesher.mesh import Mesh
from vibra.engine.model import Model
from vibra.engine.properties.fluid import Fluid
from vibra.engine.properties.libraries.fluid_library import FluidLibrary
from vibra.engine.properties.libraries.material_library import MaterialLibrary
from vibra.engine.properties.material import Material
from vibra.engine.properties.model_properties import ModelProperties
from vibra.engine.solvers import HarmonicSolver, ModalSolver
from vibra.project_files.file_helpers import read_json, update_json, write_image, write_json
from vibra.project_files.lazy_hdf5_matrix import LazyHDF5MatrixLoader, LazyHDF5MatrixWriter

from .project_hasher import HashEnum, ProjectHasher
from .project_paths import ProjectPaths


class ProjectWriter:
    def __init__(self, project_paths: ProjectPaths):
        self.project_paths = project_paths

    def write_file(self, vibra_path: Path | str):
        logging.info(f'Writing working directory "{self.project_paths.working_directory}" into file "{vibra_path}".')

        vibra_path = Path(vibra_path)
        working_dir = self.project_paths.working_directory

        with zipfile.ZipFile(vibra_path, "w", zipfile.ZIP_STORED) as file:
            for path in working_dir.rglob("*"):
                if not path.is_file():
                    continue

                arcname = path.relative_to(working_dir)
                file.write(path, arcname)

    def write_project(self, project: NewProject):
        logging.info("Writing Project.")

        self.write_project_setup(project)
        self.write_model(project.model)

        if isinstance(project.solver, ModalSolver) and (project.solver.solution is not None):
            self.write_modal_solution(project.solver)

        if project.thumbnail is not None:
            self.write_thumbnail(project.thumbnail)

    def write_model(self, model: Model):
        logging.info("Writing Model.")

        self.write_model_properties(model.properties)

        if model.geometry_path is not None:
            self.write_geometry(model.geometry_path)

        if model.mesh is not None:
            self.write_mesh(model.mesh)

    def write_project_setup(self, project: NewProject):
        logging.info("Writing project setup.")

        project_setup = {
            "mesh_setup": {},
            "analysis_setup": {},
        }

        if isinstance(project.model.geometry_path, Path):
            project_setup["geometry_filename"] = project.model.geometry_path.name
            project_setup["length_unit"] = project.model.length_unit
            project_setup["geometry_qf"] = project.model.geometry_qf

        project_setup["analysis_setup"]["analysis_id"] = int(project.current_analysis_id)

        if isinstance(project.model.new_analysis_setup, ModalAnalysisSetup | HarmonicAnalysisSetup):
            project_setup["analysis_setup"].update(project.model.new_analysis_setup.as_dict())

        mesh_setup = project.model.mesh_setup_new
        if mesh_setup is not None:
            project_setup["mesh_setup"].update(
                asdict(mesh_setup),
            )
            project_setup["mesh_setup"]["mesh_refinement_parameters"] = [
                (i.entity_type, i.element_size, i.entity_ids) 
                for i in mesh_setup.refinement_parameterss
            ]  # fmt: skip

        write_json(self.project_paths.project_setup_filepath, project_setup)

    def write_analysis_setup(self, analysis_setup: HarmonicAnalysisSetup | ModalAnalysisSetup | None):
        logging.info("Writing AnalysisSetup.")

        if isinstance(analysis_setup, HarmonicAnalysisSetup | ModalAnalysisSetup):
            analysis_setup_dict = asdict(analysis_setup)
        else:
            analysis_setup_dict = dict()

        with update_json(self.project_paths.project_setup_filepath) as project_setup:
            project_setup["analysis_setup"] = analysis_setup_dict

    def write_geometry(self, geometry_path: Path | str) -> Path:
        geometry_path = Path(geometry_path)
        if not geometry_path.is_file():
            raise FileExistsError("Geometry file path does not exist.")

        logging.info("Writing geometry.")

        shutil.rmtree(self.project_paths.geometry_folder, ignore_errors=True)
        self.project_paths.geometry_folder.mkdir(exist_ok=True)
        internal_path = self.project_paths.geometry_folder / geometry_path.name
        shutil.copy(geometry_path, internal_path)
        return internal_path

    def write_mesh(self, mesh: Mesh):
        logging.info("Writing Mesh.")
        print(self.project_paths.working_directory)

        current_hash = ProjectHasher.hash_mesh(mesh)
        previous_hash = self._read_hash(HashEnum.MESH)
        required_paths = [
            self.project_paths.mesh_data_filepath,
            self.project_paths.mesh_quality_data_filepath,
            self.project_paths.hashes_filepath,
            self.project_paths.geometry_data_filepath,
        ]
        required_paths_exist = all([i.exists() for i in required_paths])

        if (previous_hash == current_hash) and required_paths_exist:
            logging.info("Mesh was not written since it did not changed.")
            return

        with h5py.File(self.project_paths.mesh_data_filepath, "w") as file:
            file["connectivity/lines_connectivity"] = mesh.lines_connectivity
            file["connectivity/faces_connectivity"] = mesh.faces_connectivity
            file["connectivity/solids_connectivity"] = mesh.solids_connectivity

            file["nodal_data/nodal_coordinates"] = mesh.nodal_coordinates
            file["nodal_data/nodes_from_points"] = np.array(list(mesh.nodes_from_points.items()))

            if mesh.has_decoupling():
                file["connectivity/cache_lines_connectivity"] = mesh.cache_lines_connectivity
                file["connectivity/cache_faces_connectivity"] = mesh.cache_faces_connectivity
                file["connectivity/cache_solids_connectivity"] = mesh.cache_solids_connectivity

            for i, normals in mesh.normals_surface.items():
                file[f"normals/normals_surface/{i}"] = normals

            for i, curvatures in mesh.curvatures_surface.items():
                file[f"curvatures/curvatures_surface/{i}"] = curvatures

        self.write_geometry_related_mesh_parameters(mesh)
        self.write_mesh_quality_data_in_file(mesh)
        previous_hash = self._write_hash(HashEnum.MESH, current_hash)

    def write_geometry_related_mesh_parameters(self, mesh: Mesh):
        with h5py.File(self.project_paths.geometry_data_filepath, "w") as file:
            for key, val in mesh.geometry_information.items():
                file[f"entities/{key}"] = val

            file["properties/length_from_lines"] = self._dict_to_array(mesh.length_from_lines)
            file["properties/area_from_surfaces"] = self._dict_to_array(mesh.area_from_surfaces)
            file["properties/volume_from_bodies"] = self._dict_to_array(mesh.volume_from_bodies)

            for line, points in mesh.points_from_line.items():
                file[f"adjacencies/points_from_line_{line}"] = points

            for surface, lines in mesh.lines_from_surface.items():
                file[f"adjacencies/lines_from_surface_{surface}"] = lines

            for volume, surfaces in mesh.surfaces_from_volume.items():
                file[f"adjacencies/surfaces_from_volume_{volume}"] = surfaces

            if mesh.has_decoupling():
                for line, points in mesh.points_from_line.items():
                    file[f"adjacencies/cache_points_from_line_{line}"] = points

                for surface, lines in mesh.lines_from_surface.items():
                    file[f"adjacencies/cache_lines_from_surface_{surface}"] = lines

                for volume, surfaces in mesh.surfaces_from_volume.items():
                    file[f"adjacencies/cache_surfaces_from_volume_{volume}"] = surfaces

    def write_mesh_quality_data_in_file(self, mesh: Mesh):
        if not mesh.mesh_quality_data:
            return

        write_json(
            self.project_paths.mesh_quality_data_filepath,
            mesh.mesh_quality_data,
        )

    def write_model_properties(self, model_properties: ModelProperties):
        logging.info("Writing ModelProperties.")

        self.write_fluid_library(model_properties.fluid_library)
        self.write_material_library(model_properties.material_library)
        self.write_tables_in_file(
            model_properties.acoustic_imported_tables,
            model_properties.structural_imported_tables,
        )

        data = dict(
            volume_properties=self._normalize_property(model_properties.volume_properties),
            surface_properties=self._normalize_property(model_properties.surface_properties),
            line_properties=self._normalize_property(model_properties.line_properties),
            point_properties=self._normalize_property(model_properties.point_properties),
            element_properties=self._normalize_property(model_properties.element_properties),
            nodal_properties=self._normalize_property(model_properties.nodal_properties),
            group_properties=self._normalize_property(model_properties.group_properties),
        )
        write_json(self.project_paths.model_properties_filepath, data)

    def write_material_library(self, material_library: MaterialLibrary):
        logging.info("Writing MaterialLibrary.")

        material_library_dict = dict()
        for material_id, material in material_library.items():
            material_library_dict[material_id] = asdict(material)

        write_json(self.project_paths.material_library_filepath, material_library_dict)

    def write_fluid_library(self, fluid_library: FluidLibrary):
        logging.info("Writing FluidLibrary.")

        fluid_library_dict = dict()
        for fluid_id, fluid in fluid_library.items():
            fluid_library_dict[fluid_id] = asdict(fluid)

        write_json(self.project_paths.fluid_library_filepath, fluid_library_dict)

    def write_tables_in_file(
        self,
        acoustic_tables: dict[str, np.ndarray],
        structural_tables: dict[str, np.ndarray],
    ):
        if not any([acoustic_tables, structural_tables]):
            return

        logging.info("Writing project tables.")

        current_hash = ProjectHasher.hash_tables(acoustic_tables, structural_tables)
        previous_hash = self._read_hash(HashEnum.TABLES)

        if self.project_paths.imported_table_data_filepath.exists():
            if current_hash == previous_hash:
                logging.info("Mesh was not written since it did not changed.")
                return

        with h5py.File(self.project_paths.imported_table_data_filepath, "w") as file:
            for name, array in acoustic_tables.items():
                file[f"acoustic/{name}"] = array

            for name, array in structural_tables.items():
                file[f"structural/{name}"] = array

        self._write_hash(HashEnum.TABLES, current_hash)

    def write_thumbnail(self, thumbnail: Image):
        logging.info("Writing thumbnail")
        write_image(self.project_paths.thumbnail_filepath, thumbnail)

    def write_harmonic_solution(self, solver: HarmonicSolver):
        # In this case the solution was already saved
        if isinstance(solver.solution, LazyHDF5MatrixLoader):
            return

        logging.info("Writing harmonic solution")

        current_hash = ProjectHasher.hash_harmonic_solution(solver)
        previous_hash = self._read_hash(HashEnum.HARMONIC_SOLUTION)

        if self.project_paths.imported_table_data_filepath.exists():
            if current_hash == previous_hash:
                logging.info("Harmonic solution was not written since it did not changed.")
                return

        with h5py.File(self.project_paths.harmonic_solution_filepath, "w") as file:
            file["frequencies"] = solver.frequencies
            file["solution"] = solver.solution
            file["solution_status"] = np.ones_like(solver.frequencies, dtype=bool)

            if solver.displacement_dof is not None:
                file["displacement_dof"] = solver.displacement_dof

        self._write_hash(HashEnum.HARMONIC_SOLUTION, current_hash)

    def write_modal_solution(self, solver: ModalSolver):
        # In this case the solution was already saved
        if isinstance(solver.solution, LazyHDF5MatrixLoader):
            return

        logging.info("Writing modal solution")

        current_hash = ProjectHasher.hash_modal_solution(solver)
        previous_hash = self._read_hash(HashEnum.MODAL_SOLUTION)

        if self.project_paths.imported_table_data_filepath.exists():
            if current_hash == previous_hash:
                logging.info("Modal solution was not written since it did not changed.")
                return

        with h5py.File(self.project_paths.modal_solution_filepath, "w") as file:
            file["frequencies"] = solver.natural_frequencies
            file["solution"] = solver.solution
            file["solution_status"] = np.ones_like(solver.natural_frequencies, dtype=bool)

            if solver.displacement_dof is not None:
                file["displacement_dof"] = solver.displacement_dof

        self._write_hash(HashEnum.MODAL_SOLUTION, current_hash)

    def get_solution_writer(self, num_rows, columns, dtype, is_resume):
        return LazyHDF5MatrixWriter(
            self.project_paths.harmonic_solution_filepath,
            num_rows,
            columns,
            dtype,
            is_resume,
        )

    def delete_results_data(self):
        logging.info("Deleting solution data.")

        self.project_paths.results_data_filepath.unlink(missing_ok=True)
        self.project_paths.harmonic_solution_filepath.unlink(missing_ok=True)

    def delete_mesh_data(self):
        logging.info("Deleting mesh data")
        self.project_paths.mesh_data_filepath.unlink(missing_ok=True)
        self._remove_hash(HashEnum.MESH)

    def _read_hash(self, name: HashEnum) -> str | None:
        data = read_json(self.project_paths.hashes_filepath)
        if data is None:
            return
        return data.get(name)

    def _write_hash(self, name: HashEnum, hash: str):
        with update_json(self.project_paths.hashes_filepath, dict) as file:
            file[name] = hash

    def _remove_hash(self, name: HashEnum, hash: str):
        with update_json(self.project_paths.hashes_filepath, dict) as file:
            try:
                file.pop(name)
            except Exception:
                ...

    def _property_key(self, property_name: str, tags: tuple[int] | int) -> Optional[str]:
        """
        Turn the key (property_name, (tag_1, tag_2, tag_3)) into a string
        "property_name tag_1 tag_2 tag_3"
        """

        if isinstance(tags, tuple):
            spaced_tags = " ".join(str(i) for i in tags)
            return f"{property_name} {spaced_tags}"
        elif isinstance(tags, int):
            return f"{property_name} {tags}"
        else:
            return None

    def _normalize_property(self, prop: dict):
        """
        Sadly json doesn't accepts tuple keys,
        so we need to convert it to a string like:
        "property id" = value
        """
        output = dict()
        for (property, tags), data in prop.items():
            key = self._property_key(property, tags)
            if key is None:
                continue

            if isinstance(data, Fluid):
                output[key] = {"fluid_id": data.identifier}

            elif isinstance(data, Material):
                output[key] = {"material_id": data.identifier}

            elif isinstance(data, dict):
                aux = dict()
                for _key, _data in data.items():
                    if _key in ["values"]:
                        continue
                    elif isinstance(_data, Fluid):
                        aux[_key] = _data.get_data()
                    else:
                        aux[_key] = _data
                output[key] = aux
        return output

    def _dict_to_array(self, data: dict[int | float, int | float]):
        return np.array(list(data.items()))
