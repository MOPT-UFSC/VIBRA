from vibra import app

from vibra.engine.properties.fluid import Fluid
from vibra.engine.properties.material import Material
from vibra.interface.general.print_message_input import PrintMessageInput
# from vibra.project_file import *

from fileboxes import Filebox

import os
import io
import h5py
import numpy as np
from pathlib import Path

window_title_1 = "Error"
window_title_2 = "Warning"


class ProjectFileIO:
    
    def __init__(self, path : str, override=False):
        super().__init__()

        self.path = path
        self.vibra_file = Filebox(Path(path), override=override)

        self.model = app().main_window.project.model
        self.properties = self.model.properties

        self._initialize()
        self._default_filenames()
        self._default_foldernames()

    def _initialize(self):
        self.project_folder_path = Path(os.path.dirname(self.path))

    def _default_filenames(self):
        self.project_setup_filename = "project_setup.json"
        self.fluid_library_filename = "fluid_library.config"
        self.material_library_filename = "material_library.config"
        self.model_properties = "model_properties.json"
        self.mesh_data_filename = "mesh_data.hdf5"

    def _default_foldernames(self):
        pass

    def write_geometry_in_file(self, path):

        basename = os.path.basename(path)
        internal_path = f"geometry_files/{basename}"
        self.vibra_file.write_from_path(internal_path, path, encoding="iso-8859-1")

        try:

            project_setup = self.vibra_file.read(self.project_setup_filename)
            if project_setup is None:
                project_setup = {   "geometry_filenames" : [basename],
                                    "mesh_setup" : dict(),
                                    "analysis_setup" : dict()   }

            else:

                filenames = project_setup["geometry_filenames"]
                if basename not in filenames:
                    filenames.append(basename)
                    project_setup["geometry_filenames"] = filenames
            
            self.vibra_file.write(self.project_setup_filename, project_setup)

        except Exception as error_log:
            print(str(error_log))

    def read_geometry_from_file(self):

        geometry_file_paths = list()
        project_setup = self.vibra_file.read(self.project_setup_filename)

        if "geometry_filenames" in project_setup.keys():
            for geom_name in project_setup["geometry_filenames"]:

                dirname = self.project_folder_path / "geometry" 
                temp_path = dirname / geom_name
                internal_path = f"geometry_files/{geom_name}"

                if not os.path.exists(dirname):
                    os.mkdir(dirname)

                self.vibra_file.read_to_path(internal_path, temp_path, encoding="iso-8859-1")
                geometry_file_paths.append(str(temp_path))

        return geometry_file_paths

    def write_mesh_setup_in_file(self, mesh_setup):

        project_setup = self.vibra_file.read(self.project_setup_filename)
        if project_setup is None:
            return   

        project_setup["mesh_setup"] = mesh_setup           
        self.vibra_file.write(self.project_setup_filename, project_setup)
    
    def read_mesh_setup_from_file(self):

        mesh_setup = None
        project_setup = self.vibra_file.read(self.project_setup_filename)

        if project_setup is None:
            return

        if "mesh_setup" in project_setup.keys():
            mesh_setup = project_setup["mesh_setup"]

        return mesh_setup

    def write_mesh_data_in_file(self):

        mesh_data = dict(
                            nodal_coordinates = self.model.mesh.nodal_coordinates,
                            nodes_from_points = self.model.mesh.nodes_from_points,
                            nodes_from_lines = self.model.mesh.nodes_from_lines,
                            nodes_from_surfaces = self.model.mesh.nodes_from_surfaces,
                            nodes_from_volumes = self.model.mesh.nodes_from_volumes,

                            lines_connectivity = self.model.mesh.lines_connectivity,
                            faces_connectivity = self.model.mesh.faces_connectivity,
                            solids_connectivity = self.model.mesh.solids_connectivity,
                            connectivity_from_surfaces = self.model.mesh.connectivity_from_surfaces,

                            map_line_elements = self.model.mesh.get_array_based_elements_mapping(entity = "lines"),
                            map_face_elements = self.model.mesh.get_array_based_elements_mapping(entity = "faces"),
                            map_solid_elements = self.model.mesh.get_array_based_elements_mapping(entity = "solids"),

                            gmsh_elements_from_lines = self.model.mesh.gmsh_elements_from_lines,
                            gmsh_elements_from_surfaces = self.model.mesh.gmsh_elements_from_surfaces,
                            gmsh_elements_from_volumes = self.model.mesh.gmsh_elements_from_volumes,

                            surfaces_from_volumes = self.model.mesh.surfaces_from_volumes
                        )

        aux_file = self.project_folder_path / self.mesh_data_filename
        if os.path.exists(self.project_folder_path):
            f = h5py.File(aux_file, "w")
            f.close()

        # aux_file = io.BytesIO()
        with h5py.File(aux_file, "w") as f:

            for key, data in mesh_data.items():

                if "nodes" in key or "nodal" in key:
                    _key = f"nodal_data/{key}"

                elif "connectivity" in key:
                    _key = f"connectivity/{key}"

                elif "map" in key:
                    _key = f"maps/{key}"

                elif "gmsh" in key:
                    _key = f"gmsh_data/{key}"

                elif key == "surfaces_from_volumes":
                    _key = f"geometry_info/{key}"

                else:
                    _key = key

                if isinstance(data, dict):

                    for _id, _values in data.items():
                        name = f"{_key}_{_id}"
                        f.create_dataset(name, data=_values, dtype=int)

                else:

                    if key == "nodal_coordinates":
                        dtype = float 
                    else:
                        dtype = int

                    f.create_dataset(_key, data=data, dtype=dtype)

        f.close()
        # self.vibra_file.write_file(self.mesh_data_filename, aux_file)


    def read_mesh_data_from_file(self):

        mesh_data = dict()

        # aux_file = self.vibra_file.read_file(self.mesh_data_filename)
        # with self.vibra_file.open(self.mesh_data_filename, mode = "r") as internal_file:
        # with h5py.File(aux_file, "r") as f:

        file_path = self.project_folder_path / self.mesh_data_filename 
        if os.path.exists(file_path):
            f = h5py.File(file_path, 'r')

            groups = list(f.keys())

            for group in groups:
                for key, values in f.get(group).items():

                    try:
                        mesh_data[key] = np.array(values)

                    except:
                        mesh_data[key] = int(values)

            f.close()

        if mesh_data:
            return mesh_data
        
        return None
    

    def write_analysis_setup_in_file(self, analysis_setup):

        project_setup = self.vibra_file.read(self.project_setup_filename)
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
        self.vibra_file.write(self.project_setup_filename, project_setup)

    def read_analysis_setup_from_file(self):

        analysis_setup = None
        project_setup = self.vibra_file.read(self.project_setup_filename)

        if project_setup is None:
            return

        if "analysis_setup" in project_setup.keys():
            analysis_setup = project_setup["analysis_setup"]

        return analysis_setup

    def write_model_setup_in_file(self, project_setup : dict):
        self.vibra_file.write(self.project_setup_filename, project_setup)

    def read_model_setup_from_file(self):
        return self.vibra_file.read(self.project_setup_filename)

    def write_fluid_library_in_file(self, config):
        self.vibra_file.write(self.fluid_library_filename, config)

    def read_fluid_library_from_file(self):
        return self.vibra_file.read(self.fluid_library_filename)

    def write_model_properties_in_file(self):

        try:

            def normalize(prop: dict):
                """
                Sadly json doesn't accepts tuple keys,
                so we need to convert it to a string like:
                "property id" = value
                """
                output = dict()
                for (property, tag), data in prop.items():

                    key = f"{property} {tag}"

                    if property in ["fluid", "material"]:
                        if isinstance(data, (Fluid, Material)):
                            output[key] = data.identifier
                    else:
                        output[key] = data

                return output

            data = dict(
                        # global_properties = normalize(self.properties.global_properties),
                        volume_properties = normalize(self.properties.volume_properties),
                        surface_properties = normalize(self.properties.surface_properties),
                        line_properties = normalize(self.properties.line_properties),
                        element_properties = normalize(self.properties.element_properties),
                        nodal_properties = normalize(self.properties.nodal_properties),
                        )

            self.vibra_file.write(self.model_properties, data)

        except Exception as error_log:

            title = "Error while exporting model properties"
            message = str(error_log)
            PrintMessageInput([window_title_1, title, message])


    def read_model_properties_from_file(self):

        def denormalize(prop: dict):
            new_prop = dict()
            for key, val in prop.items():
                p, i = key.split()
                p = p.strip()
                i = int(i)
                new_prop[p, i] = val
            return new_prop

        data = self.vibra_file.read(self.model_properties)

        model_properties = dict(
                                # global_properties = denormalize(data["global_properties"]),
                                volume_properties = denormalize(data["volume_properties"]),
                                surface_properties = denormalize(data["surface_properties"]),
                                line_properties = denormalize(data["line_properties"]),
                                element_properties = denormalize(data["element_properties"]),
                                nodal_properties = denormalize(data["nodal_properties"])
                                )

        return model_properties