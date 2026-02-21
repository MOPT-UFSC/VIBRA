import zipfile
import shutil

from vibra import app
from vibra.engine.properties.fluid import Fluid
from vibra.engine.properties.material import Material
from vibra.interface.general.print_message_input import PrintMessageInput

import os
import h5py
import numpy as np

from copy import deepcopy
from pathlib import Path

from vibra.project_files.file_helpers import read_json, write_json, read_config, write_config, read_image, write_image
from vibra.project_files.lazy_hdf5_matrix import LazyHDF5MatrixWriter, LazyHDF5MatrixLoader

from vibra.utils.utils import get_color_rgb, get_list_of_values_from_string

window_title_1 = "Error"
window_title_2 = "Warning"


class ProjectFile:
    
    def __init__(self, path: str):
        super().__init__()

        self.path = Path(path)

        self._default_paths()

    def _default_paths(self):
        self.project_setup_filepath = self.path / "project_setup.json"
        self.fluid_library_filepath = self.path / "fluid_library.json"
        self.material_library_filepath = self.path / "material_library.json"
        self.geometry_data_filepath = self.path / "geometry_data.hdf5"
        self.model_properties_filepath = self.path / "model_properties.json"
        self.mesh_data_filepath = self.path / "mesh_data.hdf5"
        self.mesh_quality_data_filepath = self.path / "mesh_quality_data.json"
        self.errors_data_filepath = self.path / "errors_data.json"
        self.imported_table_data_filepath = self.path / "imported_tables_data.hdf5"
        self.results_data_filepath = self.path / "results_data.hdf5"
        self.thumbnail_filepath = self.path / "thumbnail.png"
        self.harmonic_solution_filepath = self.path / "harmonic_solution.hdf5"
        self.geometry_folder = self.path / "geometry_file"

    def write_geometry_in_file(self, path: Path, length_unit: str = "millimeter", geometry_qf: float = 1.0):
        basename = path.name
        internal_path = self.geometry_folder / basename

        shutil.rmtree(self.geometry_folder, ignore_errors=True)
        self.geometry_folder.mkdir(exist_ok=True)

        shutil.copy(path, internal_path)

        try:

            project_setup = read_json(self.project_setup_filepath)
            if project_setup is None:
                project_setup = {   
                                 "geometry_filename" : basename,
                                 "length_unit" : length_unit,
                                 "geometry_qf" : geometry_qf,
                                 "mesh_setup" : dict(),
                                 "analysis_setup" : dict()
                                }

            else:

                project_setup["geometry_filename"] = basename
            
            write_json(self.project_setup_filepath, project_setup)
            app().main_window.project_data_modified = True

        except Exception as error_log:
            from traceback import print_exception
            print_exception(error_log)

    def read_geometry_from_file(self):
        project_setup = read_json(self.project_setup_filepath)

        if "geometry_filename" in project_setup.keys():
            geometry_filename = project_setup["geometry_filename"]
            temp_path = self.geometry_folder / geometry_filename

            return str(temp_path)

    def read_geometry_setup_from_file(self):
        project_setup = read_json(self.project_setup_filepath)
        length_unit = project_setup.get("length_unit", "millimeter")  
        geometry_qf = project_setup.get("geometry_qf", 3.0)  
        return length_unit, geometry_qf

    def write_geometry_data_in_file(self):

        mesh = app().project.model.mesh

        geometry_data = dict(
            geometry_info = mesh.geometry_information,
            length_from_lines = mesh.length_from_lines,
            area_from_surfaces = mesh.area_from_surfaces,
            volume_from_bodies = mesh.volume_from_bodies,
            surfaces_from_volume = mesh.surfaces_from_volume,
            lines_from_surface = mesh.lines_from_surface,
            points_from_line = mesh.points_from_line,
        )

        if app().project.model.properties.is_the_surface_property_present_in_the_model("degrees_of_freedom_decoupling"):

            geometry_data.update(dict(
                cache_surfaces_from_volume = mesh.cache_surfaces_from_volume,
                cache_lines_from_surface = mesh.cache_lines_from_surface,
                cache_points_from_line = mesh.cache_points_from_line,
            ))

        with h5py.File(self.geometry_data_filepath, "w") as f:

            for key, input_data in geometry_data.items():

                if key == "geometry_info":
                    dtype = int
                    output_data = dict()

                    for _key, _data in input_data.items():
                        new_key = f"entities/{_key}"
                        output_data[new_key] = _data

                elif key in [
                    "surfaces_from_volume",
                    "lines_from_surface",
                    "points_from_line",
                    "cache_surfaces_from_volume",
                    "cache_lines_from_surface",
                    "cache_points_from_line",
                ]:

                    dtype = int
                    prefix = f"adjacencies/{key}"
                    output_data = deepcopy(input_data)

                elif key in [
                    "length_from_lines",
                    "area_from_surfaces",
                    "volume_from_bodies",
                ]:

                    if not input_data:
                        continue

                    dtype = float
                    prefix = f"properties/{key}"
                    output_data = convert_numeric_dictionary_in_array(input_data, float)

                else:
                    continue

                if isinstance(output_data, dict):
                    for _key, values in output_data.items():
                        if isinstance(_key, int):
                            name = f"{prefix}_{_key}"

                        elif isinstance(_key, str) and "entities" in _key:
                            name = _key

                        else:
                            continue

                        f.create_dataset(name, data=values, dtype=dtype)

                else:
                    f.create_dataset(prefix, data=output_data, dtype=dtype)

        self.remove_results_data_from_project_file()
        app().main_window.project_data_modified = True

    def read_geometry_data_from_file(self):

        if not self.geometry_data_filepath.exists():
            return dict()

        try:
            geometry_data = dict()
            with h5py.File(self.geometry_data_filepath, "r") as f:

                for group in list(f.keys()):
                    for key, values in f.get(group).items():

                        try:
                            geometry_data[key] = np.array(values)

                        except:
                            geometry_data[key] = int(values)

        except Exception as error_log:
            # from traceback import print_exception
            # print_exception(error_log)
            return dict()

        return geometry_data

    def write_mesh_setup_in_file(self, mesh_setup):
        project_setup = read_json(self.project_setup_filepath)
        if project_setup is None:
            return   

        project_setup["mesh_setup"] = mesh_setup           
        write_json(self.project_setup_filepath, project_setup)
        app().main_window.project_data_modified = True

    def write_mesh_quality_data_in_file(self):
        mesh_quality_data = app().project.model.mesh.mesh_quality_data
        if not mesh_quality_data:
            return
        
        def convert_ndarrays_to_lists(qm_data: dict):
            if isinstance(qm_data, dict):
                return {k: convert_ndarrays_to_lists(v) for k, v in qm_data.items()}
            elif isinstance(qm_data, list):
                return [convert_ndarrays_to_lists(i) for i in qm_data]
            elif isinstance(qm_data, np.ndarray):
                return qm_data.tolist()
            elif isinstance(qm_data, np.uint64):
                return int(qm_data)
            else:
                return qm_data

        mesh_quality_data_json_ready = convert_ndarrays_to_lists(mesh_quality_data)
        
        write_json(self.mesh_quality_data_filepath, mesh_quality_data_json_ready)
        app().main_window.project_data_modified = True    

    def read_mesh_quality_data_from_file(self):
        mesh_quality_data = dict()
        try:
            if not self.mesh_data_filepath.exists():
                return mesh_quality_data

            mesh_quality_data = read_json(self.mesh_quality_data_filepath)
            if mesh_quality_data:
                return mesh_quality_data

        except Exception as error_log:
            from traceback import print_exception
            print_exception(error_log)
            return mesh_quality_data

    def read_mesh_setup_from_file(self):
        project_setup = read_json(self.project_setup_filepath)
        if project_setup is None:
            return

        mesh_setup = project_setup.get("mesh_setup")

        return mesh_setup

    def write_mesh_data_in_file(self):
        mesh = app().project.model.mesh

        mesh_data = dict(
            nodal_coordinates = mesh.nodal_coordinates,
            nodes_from_points = convert_numeric_dictionary_in_array(mesh.nodes_from_points, int),
            lines_connectivity = mesh.lines_connectivity,
            faces_connectivity = mesh.faces_connectivity,
            solids_connectivity = mesh.solids_connectivity,
            normals_surface = mesh.normals_surface,
            curvatures_surface = mesh.curvatures_surface,
        )

        if app().project.model.properties.is_the_surface_property_present_in_the_model("degrees_of_freedom_decoupling"):

            mesh_data.update(dict(
                cache_nodal_coordinates = mesh.cache_nodal_coordinates,
                cache_solids_connectivity = mesh.cache_solids_connectivity,
                cache_faces_connectivity = mesh.cache_faces_connectivity,
                cache_lines_connectivity = mesh.cache_lines_connectivity,
            ))

        with h5py.File(self.mesh_data_filepath, "w") as f:

            for key, data in mesh_data.items():

                if "nodes" in key or "nodal" in key:
                    dtype = float
                    prefix = f"nodal_data/{key}"

                elif "connectivity" in key:
                    dtype = int
                    prefix = f"connectivity/{key}"

                elif "normals_surface" in key:
                    dtype = float
                    prefix = f"normals/{key}"

                elif "curvatures_surface" in key:
                    dtype = float
                    prefix = f"curvatures/{key}"

                else:
                    dtype = int
                    prefix = key

                if isinstance(data, dict):
                    for _id, values in data.items():
                        name = f"{prefix}_{_id}"
                        f.create_dataset(name, data=values, dtype=dtype)

                else:
                    f.create_dataset(prefix, data=data, dtype=dtype)

        self.remove_results_data_from_project_file()
        app().main_window.project_data_modified = True

    def read_mesh_data_from_file(self):

        if not self.mesh_data_filepath.exists():
            return dict()

        try:
            mesh_data = dict()
            with h5py.File(self.mesh_data_filepath, "r") as f:

                for group in list(f.keys()):
                    for key, values in f.get(group).items():

                        try:
                            mesh_data[key] = np.array(values)

                        except:
                            mesh_data[key] = int(values)

        except Exception as error_log:
            from traceback import print_exception
            print_exception(error_log)
            return dict()

        return mesh_data

    def write_analysis_setup_in_file(self, analysis_setup: dict):
        project_setup = read_json(self.project_setup_filepath)
        if project_setup is None:
            return
        
        aux = dict()
        for key, data in analysis_setup.items():

            if isinstance(data, np.ndarray):
                if data.size == 0:
                    continue

                data = list(data)

            aux[key] = data

        project_setup["analysis_setup"] = aux         
        write_json(self.project_setup_filepath, project_setup)
        app().main_window.project_data_modified = True

    def read_analysis_setup_from_file(self):
        project_setup = read_json(self.project_setup_filepath)
        if not isinstance(project_setup, dict):
            return dict()

        return project_setup.get("analysis_setup", dict)

    def write_model_setup_in_file(self, project_setup : dict):
        write_json(self.project_setup_filepath, project_setup)
        app().main_window.project_data_modified = True

    def read_model_setup_from_file(self):
        return read_json(self.project_setup_filepath)

    def write_material_library_in_file(self, config):
        write_json(self.material_library_filepath, config)
        app().main_window.project_data_modified = True

    def read_material_library_from_file(self):
        self.backward_compatibility_for_materials_data_file()
        return read_json(self.material_library_filepath)
        # return read_config(self.material_library_filepath)

    def write_fluid_library_in_file(self, fluid_data: dict):
        write_json(self.fluid_library_filepath, fluid_data)
        app().main_window.project_data_modified = True

    def read_fluid_library_from_file(self):
        self.backward_compatibility_for_fluids_data_file()
        return read_json(self.fluid_library_filepath)
        # return read_config(self.fluid_library_filepath)

    def write_model_properties_in_file(self):

        try:
            def normalize(prop: dict):
                """
                Sadly json doesn't accepts tuple keys,
                so we need to convert it to a string like:
                "property id" = value
                """
                output = dict()
                for (property, tags), data in prop.items():

                    if isinstance(tags, tuple):
                        key = f"{property}"
                        for tag in tags:
                            key += f" {tag}"

                    elif isinstance(tags, int):
                        key = f"{property} {tags}"

                    elif isinstance(tags, str):
                        key = tags

                    else:
                        continue

                    aux = dict()
                    if isinstance(data, dict):
                        for _key, _data in data.items():
                            if _key in ["values", "tables_frequencies"]:
                                continue
                            elif isinstance(_data, Fluid):
                                aux[_key] = _data.get_data()
                            else:
                                aux[_key] = _data

                    elif isinstance(data, Fluid):
                        aux["fluid_id"] = data.identifier

                    elif isinstance(data, Material):
                        aux["material_id"] = data.identifier

                    else:
                        continue
                        # output[key] = data

                    if aux:
                        output[key] = aux

                return output

            properties = app().project.model.properties

            data = dict(
                        global_properties = normalize(properties.global_properties),
                        volume_properties = normalize(properties.volume_properties),
                        surface_properties = normalize(properties.surface_properties),
                        line_properties = normalize(properties.line_properties),
                        point_properties = normalize(properties.point_properties),
                        element_properties = normalize(properties.element_properties),
                        nodal_properties = normalize(properties.nodal_properties),
                        group_properties = normalize(properties.group_properties)
                        )
                                        
            write_json(self.model_properties_filepath, data)
            app().main_window.project_data_modified = True

        except Exception as error_log:

            title = "Error while exporting model properties"
            message = str(error_log)
            PrintMessageInput([window_title_1, title, message])

    def read_model_properties_from_file(self):

        def denormalize(prop: dict):
            if prop is None:
                return dict()
            
            new_prop = dict()
            for key, val in prop.items():

                key: str
                property, *_ids = key.split()
                property = property.strip()

                if property == "perforated_plate_model":
                    fluid = Fluid(**val["fluid"])
                    val["fluid"] = fluid

                if len(_ids) == 1:
                    ids = int(_ids[0])
                else:
                    ids = tuple([int(_id) for _id in _ids])

                new_prop[property, ids] = val

            return new_prop

        data = read_json(self.model_properties_filepath)

        if data is None:
            return dict()

        model_properties = dict(
                                # global_properties = denormalize(data.get(""global_properties")),
                                volume_properties = denormalize(data.get("volume_properties")),
                                surface_properties = denormalize(data.get("surface_properties")),
                                line_properties = denormalize(data.get("line_properties")),
                                point_properties = denormalize(data.get("point_properties")),
                                element_properties = denormalize(data.get("element_properties")),
                                nodal_properties = denormalize(data.get("nodal_properties")),
                                group_properties = denormalize(data.get("group_properties"))
                                )

        return model_properties

    def write_imported_table_data_in_file(self):

        self.remove_table_data_from_project_file()
        acoustic_imported_tables = app().project.model.properties.acoustic_imported_tables
        structural_imported_tables = app().project.model.properties.structural_imported_tables

        if acoustic_imported_tables or structural_imported_tables:

            with h5py.File(self.imported_table_data_filepath, "w") as f:

                for group_label in ["acoustic", "structural"]:

                    if group_label == "acoustic":
                        imported_tables = acoustic_imported_tables
                    else:
                        imported_tables = structural_imported_tables

                    for table_name, data_array in imported_tables.items():

                        if table_name is None:
                            continue

                        data_name = f"{group_label}/{table_name}"
                        f.create_dataset(data_name, data=data_array, dtype=float)

                app().main_window.project_data_modified = True

    def read_imported_table_data_from_file(self):

        if not self.imported_table_data_filepath.exists():
            return dict()

        try:
            tables_data = dict()
            with h5py.File(self.imported_table_data_filepath, "r") as f:

                for group in list(f.keys()):
                    aux = dict()
                    for key, values in f.get(group).items():

                        try:
                            aux[key] = np.array(values)
                        except:
                            continue

                    if aux:
                        tables_data[group] = aux

        except:
            return dict()

        return tables_data

    def write_thumbnail(self):
        thumbnail = app().project.thumbnail
        if thumbnail is None:
            return
        write_image(self.thumbnail_filepath, thumbnail)
        app().main_window.project_data_modified = True

    def read_thumbnail(self):
        return read_image(self.thumbnail_filepath)
    
    def write_results_data_in_file(self):
        acoustic_harmonic_solver = app().project.acoustic_harmonic_solver
        structural_harmonic_solver = app().project.structural_harmonic_solver

        if acoustic_harmonic_solver is not None and acoustic_harmonic_solver.project_file is not None:
            return

        if structural_harmonic_solver is not None and structural_harmonic_solver.project_file is not None:
            return

        with h5py.File(self.results_data_filepath, "w") as f:

            acoustic_modal_solver = app().project.acoustic_modal_solver
            if acoustic_modal_solver is not None:
                if acoustic_modal_solver.solution is not None:
                    modal_shapes = acoustic_modal_solver.solution
                    natural_frequencies = acoustic_modal_solver.natural_frequencies
                    complex_natural_frequencies = acoustic_modal_solver.complex_natural_frequencies
                    if len(complex_natural_frequencies):
                        f.create_dataset("modal_acoustic/natural_frequencies", data=complex_natural_frequencies, dtype=complex)
                    else:
                        f.create_dataset("modal_acoustic/natural_frequencies", data=natural_frequencies, dtype=float)
                    f.create_dataset("modal_acoustic/solution", data=modal_shapes, dtype=complex)

            structural_modal_solver = app().project.structural_modal_solver
            if structural_modal_solver is not None:
                if structural_modal_solver.solution is not None:
                    natural_frequencies = structural_modal_solver.natural_frequencies
                    solution_full = structural_modal_solver.solution
                    displacement_dof = structural_modal_solver.displacement_dof
                    f.create_dataset("modal_structural/natural_frequencies", data=natural_frequencies, dtype=float)
                    f.create_dataset("modal_structural/solution", data=solution_full, dtype=complex)
                    f.create_dataset("modal_structural/displacement_dof", data=displacement_dof, dtype=int)

            acoustic_harmonic_solver = app().project.acoustic_harmonic_solver
            if acoustic_harmonic_solver is not None:
                if acoustic_harmonic_solver.solution is not None:
                    frequencies = app().project.model.frequencies
                    solution = acoustic_harmonic_solver.solution
                    f.create_dataset("harmonic_acoustic/frequencies", data=frequencies, dtype=float)
                    f.create_dataset("harmonic_acoustic/solution", data=solution, dtype=complex)

            structural_harmonic_solver = app().project.structural_harmonic_solver
            if structural_harmonic_solver is not None:
                if structural_harmonic_solver.solution is not None:
                    frequencies = app().project.model.frequencies
                    solution = structural_harmonic_solver.solution
                    displacement_dof = structural_harmonic_solver.displacement_dof
                    f.create_dataset("harmonic_structural/frequencies", data=frequencies, dtype=float)
                    f.create_dataset("harmonic_structural/solution", data=solution, dtype=complex)
                    f.create_dataset("harmonic_structural/displacement_dof", data=displacement_dof, dtype=int)

            app().main_window.project_data_modified = True

    def handling_harmonic_solution_results(self, solver_tag: str):

        if not self.results_data_filepath.exists():
            return

        with h5py.File(self.results_data_filepath, "r") as f_src:
            # Converting Harmonic solution in the old form.
            analysis = f_src.get(solver_tag)
            if analysis:
                for key in ["displacement_dofs", "displacement_dof"]:
                    displacement_dof = analysis.get(key)
                    if isinstance(displacement_dof, np.ndarray):
                        break

                frequencies = analysis.get("frequencies")
                solution_dset = analysis.get("solution")

                if (displacement_dof, frequencies, solution_dset).count(None):
                    return

                solution = solution_dset[()]
                writer = LazyHDF5MatrixWriter(self.harmonic_solution_filepath, solution.shape[0], frequencies, solution.dtype)

                if displacement_dof is not None:
                    writer.save_extra_data("displacement_dof", displacement_dof, dtype=int)

                for i in range(frequencies.size):
                    writer[:, i] = solution[:, i]

        self.remove_results_data_from_project_file()

    def get_solution_writer(self, num_rows, columns, dtype, is_resume):
        return LazyHDF5MatrixWriter(self.harmonic_solution_filepath, num_rows, columns, dtype, is_resume)

    def get_solution_loader(self):
        if not self.harmonic_solution_filepath.exists():
            return None
        return LazyHDF5MatrixLoader(self.harmonic_solution_filepath)

    def delete_harmonic_solution(self):
        if self.harmonic_solution_filepath.exists():
            self.harmonic_solution_filepath.unlink()

    def read_results_data_from_file(self):

        if not self.results_data_filepath.exists():
            return dict()

        try:
            results_data = dict()
            with h5py.File(self.results_data_filepath, "r") as f:

                for group in list(f.keys()):
                    aux = dict()
                    for key, values in f.get(group).items():

                        try:
                            aux[key] = np.array(values)
                        except:
                            continue

                    if aux:
                        results_data[group] = aux

        except:
            return dict()

        return results_data

    def remove_geometry_data_from_project_file(self):
        self.geometry_data_filepath.unlink(missing_ok=True)

    def remove_model_properties_from_project_file(self):
        self.model_properties_filepath.unlink(missing_ok=True)

    def remove_mesh_data_from_project_file(self):
        self.mesh_data_filepath.unlink(missing_ok=True)

    def remove_mesh_error_data_from_project_file(self):
        errors_data = self.read_errors_data_from_file()
        if "mesh_error" in errors_data.keys():
            errors_data.pop("mesh_error")
            write_json(self.errors_data_filepath, errors_data)

        if not errors_data:
            self.errors_data_filepath.unlink(missing_ok=True)

        app().main_window.project_data_modified = True

    def remove_mesh_quality_data_from_project_file(self):
        self.mesh_quality_data_filepath.unlink(missing_ok=True)

    def remove_table_data_from_project_file(self):
        self.imported_table_data_filepath.unlink(missing_ok=True)

    def remove_results_data_from_project_file(self):
        self.results_data_filepath.unlink(missing_ok=True)
        self.harmonic_solution_filepath.unlink(missing_ok=True)

    def archive_project(self, zip_path: Path):
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_STORED) as zipf:
            for path in self.path.rglob("*"):
                if path.is_file():
                    arcname = path.relative_to(self.path)
                    zipf.write(path, arcname)

    def extract_project(self, path: Path):
        with zipfile.ZipFile(path, 'r') as zipf:
            zipf.extractall(path=self.path)

    def read_errors_data_from_file(self):
        errors_data = read_json(self.errors_data_filepath)
        if errors_data is None:
            return dict()

        return errors_data

    def read_mesh_error_data_from_file(self):
        errors_data = self.read_errors_data_from_file()
        return errors_data.get("mesh_error")  

    def write_mesh_error_data_in_file(self):
        mesh_error = dict()
        mesh = app().project.model.mesh
        errors_data = self.read_errors_data_from_file()

        if mesh.disconnected_nodes_data:
            mesh_error["disconnected_nodes_data"] = mesh.disconnected_nodes_data

        if mesh.collapsed_elements_data:
            mesh_error["collapsed_elements_data"] = mesh.collapsed_elements_data

        if not mesh_error:
            return

        errors_data["mesh_error"] = mesh_error

        write_json(self.errors_data_filepath, errors_data)
        app().main_window.project_data_modified = True

    def backward_compatibility_for_fluids_data_file(self):
        path = deepcopy(str(self.fluid_library_filepath))
        cpath = Path(path.replace(".json", ".config"))
        if cpath.exists():
            fluid_data = self.convert_fluid_data_from_configparser_to_dictionary(cpath, remove_after_convert=True)
            if fluid_data:
                self.write_fluid_library_in_file(fluid_data)

    def backward_compatibility_for_materials_data_file(self):
        path = deepcopy(str(self.material_library_filepath))
        cpath = Path(path.replace(".json", ".config"))
        if cpath.exists():
            material_data = self.convert_material_data_from_configparser_to_dictionary(cpath, remove_after_convert=True)
            if material_data:
                self.write_material_library_in_file(material_data)

    def convert_fluid_data_from_configparser_to_dictionary(self, path: Path, remove_after_convert: bool=False) -> dict:

        fluid_data = dict()
        config = read_config(path)

        for tag in config.sections():

            section = config[tag]
            keys = section.keys()

            identifier = int(section.get('identifier', -1))

            fluid_parameters = {
                                "name" : section.get("name", ""),
                                "identifier" : identifier,
                                "fluid_density" : float(section.get('fluid_density', -1)),
                                "speed_of_sound" : float(section.get('speed_of_sound', -1)),
                                "isentropic_exponent" : float(section.get('isentropic_exponent', -1)),
                                "thermal_conductivity" : float(section.get('thermal_conductivity', -1)),
                                "specific_heat_Cp" : float(section.get('specific_heat_Cp', -1)),
                                "dynamic_viscosity" : float(section.get('dynamic_viscosity', -1)),
                                "temperature" : float(section.get('temperature', -1)),
                                "pressure" : float(section.get('pressure', -1)),
                                "molar_mass" : float(section.get('molar_mass', -1)),
                                "color" : get_color_rgb(section.get('color')),
                                }

            if 'key_mixture' in keys:
                fluid_parameters["key_mixture"] = section.get('key_mixture')

            if 'molar_fractions' in keys:
                str_molar_fractions = section.get('molar_fractions')
                molar_fractions = get_list_of_values_from_string(str_molar_fractions, int_values=False)
                fluid_parameters["molar_fractions"] = molar_fractions

            fluid_data[identifier] = fluid_parameters

        if remove_after_convert:
            path.unlink()

        return fluid_data

    def convert_material_data_from_configparser_to_dictionary(self, path: Path, remove_after_convert: bool=False) -> dict:

        material_library_data = dict()
        config = read_config(path)

        for tag in config.sections():

            section = config[tag]
            identifier = int(section.get('identifier', -1))

            material_parameters = {
                                    "name" : section.get("name", ""),
                                    "identifier" : identifier,
                                    "material_density" : float(section.get('material_density', -1)),
                                    "poisson_ratio" : float(section.get('poisson_ratio', -1)),
                                    "elasticity_modulus" : float(section.get('elasticity_modulus', -1)),
                                    "thermal_expansion_coefficient" : float(section.get('thermal_expansion_coefficient', -1)),
                                    "color" : get_color_rgb(section.get('color')),
                                    }

            material_library_data[identifier] = material_parameters

        if remove_after_convert:
            path.unlink()

        return material_library_data

def convert_numeric_dictionary_in_array(input_data: dict, data_type: int | float):
    """ This function converts a numeric dictionary into an equivalent 
        array with keys and values arranged in the first and second 
        columns, respectively.

        Parameters
        ----------
        input_data: dict
            the numeric dictionary to be converted 
            into an array of two columns

        dtype: str, int as default value
            configures the data type from the
            output array

        Return
        ------
        output_data: np.ndarray
            the output array of two columns

    """
    if len(input_data) == 0:
        return np.array([[]])

    keys = list(input_data.keys())
    values = list(input_data.values())

    # if isinstance(values[0], np.ndarray):
    #     values = [int(value) for value in values]
    
    output_data = np.array([keys, values], dtype=data_type).T

    return output_data