from typing import TYPE_CHECKING

from vibra.engine.properties.fluid import Fluid
from vibra.engine.properties.material import Material
from vibra.interface.general.print_message_input import PrintMessageInput

if TYPE_CHECKING:
    from vibra.project_files.project import Project

import os
from copy import deepcopy
from pathlib import Path

import h5py
import numpy as np
from fileboxes import Filebox

window_title_1 = "Error"
window_title_2 = "Warning"


class ProjectFile:
    def __init__(self, project: "Project", path : str, override=False):
        super().__init__()

        self.path = path
        self.project = project
        self.filebox = Filebox(Path(path), override=override)
        self.data_modified = False

        self._initialize()
        self._default_filenames()
        self._default_foldernames()

    def _initialize(self):
        self.project_folder_path = Path(os.path.dirname(self.path))

    def _default_filenames(self):
        self.project_setup_filename = "project_setup.json"
        self.fluid_library_filename = "fluid_library.config"
        self.material_library_filename = "material_library.config"
        self.geometry_data_filename = "geometry_data.hdf5"
        self.model_properties_filename = "model_properties.json"
        self.mesh_data_filename = "mesh_data.hdf5"
        self.imported_table_data_filename = "imported_tables_data.hdf5"
        self.results_data_filename = "results_data.hdf5"
        self.thumbnail_filename = "thumbnail.png"

    def _default_foldernames(self):
        pass

    def write_geometry_in_file(self, path, length_unit: str = "milimeter", geometry_qf: float = 1.0):

        basename = os.path.basename(path)
        internal_path = f"geometry_file/{basename}"

        try:
            self.filebox.remove("geometry_file")
        except:
            pass

        self.filebox.write_from_path(internal_path, path, encoding="iso-8859-1")

        try:

            project_setup = self.filebox.read(self.project_setup_filename)
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
            
            self.filebox.write(self.project_setup_filename, project_setup)
            self.project_data_modified = True

        except Exception as error_log:
            from traceback import print_exception
            print_exception(error_log)

    def read_geometry_from_file(self):

        project_setup = self.filebox.read(self.project_setup_filename)

        if "geometry_filename" in project_setup.keys():

            geometry_filename = project_setup["geometry_filename"]
            dirname = self.project_folder_path / "geometry" 
            temp_path = dirname / geometry_filename
            internal_path = f"geometry_file/{geometry_filename}"

            if os.path.exists(dirname):
                for filename in os.listdir(dirname).copy():
                    file_path = dirname / filename
                    os.remove(file_path)
            else:
                os.mkdir(dirname)

            self.filebox.read_to_path(internal_path, temp_path)

        return str(temp_path)

    def read_geometry_setup_from_file(self):
        project_setup = self.filebox.read(self.project_setup_filename)
        length_unit = project_setup.get("length_unit", "milimeter")  
        geometry_qf = project_setup.get("geometry_qf", 3.0)  
        return length_unit, geometry_qf

    def write_geometry_data_in_file(self):

        mesh = self.project.model.mesh

        geometry_data = dict(
                            geometry_info = mesh.geometry_information,
                            length_from_lines = mesh.length_from_lines,
                            area_from_surfaces = mesh.area_from_surfaces,
                            volume_from_bodies = mesh.volume_from_bodies,
                            surfaces_from_volume = mesh.surfaces_from_volume,
                            lines_from_surface = mesh.lines_from_surface,
                            points_from_line = mesh.points_from_line,
                            )

        if self.project.model.properties.is_the_surface_property_present_in_the_model("degrees_of_freedom_decoupling"):

            geometry_data.update(dict(
                                      cache_surfaces_from_volume = mesh.cache_surfaces_from_volume,
                                      cache_lines_from_surface = mesh.cache_lines_from_surface,
                                      cache_points_from_line = mesh.cache_points_from_line,
                                      ))

        with self.filebox.open(self.geometry_data_filename, "w") as internal_file:
            with h5py.File(internal_file, "w") as f:

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

        self.filebox.remove(self.results_data_filename)
        self.project_data_modified = True

    def read_geometry_data_from_file(self):

        geometry_data = dict()

        try:
            with self.filebox.open(self.geometry_data_filename) as internal_file:
                with h5py.File(internal_file, "r") as f:

                    for group in list(f.keys()):
                        for key, values in f.get(group).items():

                            try:
                                geometry_data[key] = np.array(values)

                            except:
                                geometry_data[key] = int(values)

        except Exception:
            # from traceback import print_exception
            # print_exception(error_log)
            return dict()

        return geometry_data

    def write_mesh_setup_in_file(self, mesh_setup):

        project_setup = self.filebox.read(self.project_setup_filename)
        if project_setup is None:
            return   

        project_setup["mesh_setup"] = mesh_setup           
        self.filebox.write(self.project_setup_filename, project_setup)
        self.project_data_modified = True
    
    def read_mesh_setup_from_file(self):

        project_setup = self.filebox.read(self.project_setup_filename)
        if project_setup is None:
            return

        mesh_setup = project_setup.get("mesh_setup")

        return mesh_setup

    def write_mesh_data_in_file(self):

        mesh = self.project.model.mesh

        mesh_data = dict(
                         nodal_coordinates = mesh.nodal_coordinates,
                         nodes_from_points = convert_numeric_dictionary_in_array(mesh.nodes_from_points, int),
                         lines_connectivity = mesh.lines_connectivity,
                         faces_connectivity = mesh.faces_connectivity,
                         solids_connectivity = mesh.solids_connectivity,
                         normals_surface = mesh.normals_surface,
                         curvatures_surface = mesh.curvatures_surface,
                         )

        if self.project.model.properties.is_the_surface_property_present_in_the_model("degrees_of_freedom_decoupling"):

            mesh_data.update(dict(
                                  cache_nodal_coordinates = mesh.cache_nodal_coordinates,
                                  cache_solids_connectivity = mesh.cache_solids_connectivity,
                                  cache_faces_connectivity = mesh.cache_faces_connectivity,
                                  cache_lines_connectivity = mesh.cache_lines_connectivity,
                                  ))

        with self.filebox.open(self.mesh_data_filename, "w") as internal_file:
            with h5py.File(internal_file, "w") as f:

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

        self.filebox.remove(self.results_data_filename)
        self.project_data_modified = True

    def read_mesh_data_from_file(self):

        mesh_data = dict()

        try:
            with self.filebox.open(self.mesh_data_filename) as internal_file:
                with h5py.File(internal_file, "r") as f:

                    for group in list(f.keys()):
                        for key, values in f.get(group).items():

                            try:
                                mesh_data[key] = np.array(values)

                            except:
                                mesh_data[key] = int(values)

        except Exception:
            # from traceback import print_exception
            # print_exception(error_log)
            return dict()

        return mesh_data


    def write_analysis_setup_in_file(self, analysis_setup: dict):

        project_setup = self.filebox.read(self.project_setup_filename)
        if project_setup is None:
            return   

        aux = dict()
        for key, data in analysis_setup.items():
            if key == "frequencies":
                continue
            # if isinstance(data, np.ndarray):
            #     data = list(data)
            aux[key] = data

        project_setup["analysis_setup"] = aux         
        self.filebox.write(self.project_setup_filename, project_setup)
        self.project_data_modified = True

    def read_analysis_setup_from_file(self):

        analysis_setup = None
        project_setup = self.filebox.read(self.project_setup_filename)

        if project_setup is None:
            return

        if "analysis_setup" in project_setup.keys():
            analysis_setup = project_setup["analysis_setup"]

        return analysis_setup

    def write_model_setup_in_file(self, project_setup : dict):
        self.filebox.write(self.project_setup_filename, project_setup)
        self.project_data_modified = True

    def read_model_setup_from_file(self):
        return self.filebox.read(self.project_setup_filename)

    def write_material_library_in_file(self, config):
        self.filebox.write(self.material_library_filename, config)
        self.project_data_modified = True

    def read_material_library_from_file(self):
        return self.filebox.read(self.material_library_filename)

    def write_fluid_library_in_file(self, config):
        self.filebox.write(self.fluid_library_filename, config)
        self.project_data_modified = True

    def read_fluid_library_from_file(self):
        return self.filebox.read(self.fluid_library_filename)

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

                    else:
                        continue

                    aux = dict()
                    if isinstance(data, dict):
                        for _key, _data in data.items():
                            if _key in ["values"]:
                                continue
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

            properties = self.project.model.properties
            data = dict(
                        # global_properties = normalize(properties.global_properties),
                        volume_properties = normalize(properties.volume_properties),
                        surface_properties = normalize(properties.surface_properties),
                        line_properties = normalize(properties.line_properties),
                        element_properties = normalize(properties.element_properties),
                        nodal_properties = normalize(properties.nodal_properties),
                        )

            self.filebox.write(self.model_properties_filename, data)
            self.project_data_modified = True

        except Exception as error_log:

            title = "Error while exporting model properties"
            message = str(error_log)
            PrintMessageInput([window_title_1, title, message])

    def read_model_properties_from_file(self):

        def denormalize(prop: dict):
            new_prop = dict()
            for key, val in prop.items():

                key: str
                p, *_ids = key.split()
                p = p.strip()

                if len(_ids) == 1:
                    ids = int(_ids[0])
                else:
                    ids = tuple([int(_id) for _id in _ids])

                new_prop[p, ids] = val

            return new_prop

        data = self.filebox.read(self.model_properties_filename)

        if data is None:
            return dict()

        model_properties = dict(
                                # global_properties = denormalize(data["global_properties"]),
                                volume_properties = denormalize(data["volume_properties"]),
                                surface_properties = denormalize(data["surface_properties"]),
                                line_properties = denormalize(data["line_properties"]),
                                element_properties = denormalize(data["element_properties"]),
                                nodal_properties = denormalize(data["nodal_properties"])
                                )

        return model_properties

    def write_imported_table_data_in_file(self):

        self.filebox.remove(self.imported_table_data_filename)
        acoustic_imported_tables = self.project.model.properties.acoustic_imported_tables
        structural_imported_tables = self.project.model.properties.structural_imported_tables

        if acoustic_imported_tables or structural_imported_tables:

            with self.filebox.open(self.imported_table_data_filename, "w") as internal_file:
                with h5py.File(internal_file, "w") as f:

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

                    self.project_data_modified = True

    def read_imported_table_data_from_file(self):

        try:
            tables_data = dict()
            with self.filebox.open(self.imported_table_data_filename) as internal_file:
                with h5py.File(internal_file, "r") as f:

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
        thumbnail = self.project.thumbnail
        if thumbnail is None:
            return
        self.filebox.write(self.thumbnail_filename, thumbnail)
        self.project_data_modified = True

    def read_thumbnail(self):
        return self.filebox.read(self.thumbnail_filename)
    
    def write_results_data_in_file(self):

        with self.filebox.open(self.results_data_filename, "w") as internal_file:
            with h5py.File(internal_file, "w") as f:

                acoustic_modal_solver = self.project.acoustic_modal_solver
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

                structural_modal_solver = self.project.structural_modal_solver
                if structural_modal_solver is not None:
                    if structural_modal_solver.solution is not None:
                        natural_frequencies = structural_modal_solver.natural_frequencies
                        solution_full = structural_modal_solver.solution
                        displacement_dofs = structural_modal_solver.displacement_dofs
                        f.create_dataset("modal_structural/natural_frequencies", data=natural_frequencies, dtype=float)
                        f.create_dataset("modal_structural/solution", data=solution_full, dtype=complex)
                        f.create_dataset("modal_structural/displacement_dofs", data=displacement_dofs, dtype=int)

                acoustic_harmonic_solver = self.project.acoustic_harmonic_solver
                if acoustic_harmonic_solver is not None:
                    if acoustic_harmonic_solver.solution is not None:
                        frequencies = self.project.model.frequencies
                        solution = acoustic_harmonic_solver.solution
                        f.create_dataset("harmonic_acoustic/frequencies", data=frequencies, dtype=float)
                        f.create_dataset("harmonic_acoustic/solution", data=solution, dtype=complex)
                
                structural_harmonic_solver = self.project.structural_harmonic_solver
                if structural_harmonic_solver is not None:
                    if structural_harmonic_solver.solution is not None:
                        frequencies = self.project.model.frequencies
                        solution = structural_harmonic_solver.solution
                        displacement_dofs = structural_harmonic_solver.displacement_dofs
                        f.create_dataset("harmonic_structural/frequencies", data=frequencies, dtype=float)
                        f.create_dataset("harmonic_structural/solution", data=solution, dtype=complex)
                        f.create_dataset("harmonic_structural/displacement_dofs", data=displacement_dofs, dtype=int)

                self.project_data_modified = True

    def read_results_data_from_file(self):
        
        results_data = dict()

        try:

            with self.filebox.open(self.results_data_filename) as internal_file:
                with h5py.File(internal_file, "r") as f:

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
        self.filebox.remove(self.geometry_data_filename)

    def remove_model_properties_from_project_file(self):
        self.filebox.remove(self.model_properties_filename)

    def remove_mesh_data_from_project_file(self):
        self.filebox.remove(self.mesh_data_filename)

    def remove_results_data_from_project_file(self):
        self.filebox.remove(self.results_data_filename)

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