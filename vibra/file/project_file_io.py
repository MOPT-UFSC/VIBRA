import os
from vibra import app

from vibra.engine.properties.fluid import Fluid
from vibra.engine.properties.material import Material
from vibra.project_file import *

from fileboxes import Filebox

class ProjectFileIO:
    
    def __init__(self, path, override=False):
        super().__init__()
        
        self.vibra_file = Filebox(path, override=override)

        self.model = app().main_window.project.model
        self.properties = self.model.properties

        self._initialize()
        self._set_default_filenames()
        # self._set_default_foldernames()

    def _initialize(self):
        user_path = os.path.expanduser("~")
        self.project_folder_path = Path(user_path) / "temp_vibra"

    def _set_default_filenames(self):
        self.project_setup_filename = "project_setup.json"
        self.fluid_library_filename = "fluid_library.dat"
        self.material_library_filename = "material_library.dat"
        self.acoustic_model_setup_filename = "acoustic_model_setup.dat"
        self.structural_model_setup_filename = "strucutral_model_setup.dat"

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
                        volume_properties=normalize(self.properties.volume_properties),
                        surface_properties=normalize(self.properties.surface_properties),
                        line_properties=normalize(self.properties.line_properties),
                        element_properties=normalize(self.properties.element_properties),
                        nodal_properties=normalize(self.properties.nodal_properties),
                        )

            path = app().main_window.project.model_properties
            self.vibra_file.write(path, data)

        except Exception as error_log:

            title = "Error while exporting model properties"
            message = str(error_log)
            PrintMessageInput([window_title_1, title, message])

        # return json.dumps(data, indent=2)

    def read_model_properties_from_file(self, data: dict):

        def denormalize(prop: dict):
            new_prop = dict()
            for key, val in prop.items():
                p, i = key.split()
                p = p.strip()
                i = int(i)
                new_prop[p, i] = val
            return new_prop

        self.global_properties = denormalize(data["global_properties"])
        self.volume_properties = denormalize(data["volume_properties"])
        self.surface_properties = denormalize(data["surface_properties"])
        self.line_properties = denormalize(data["line_properties"])
        self.element_properties = denormalize(data["element_properties"])
        self.nodal_properties = denormalize(data["nodal_properties"])