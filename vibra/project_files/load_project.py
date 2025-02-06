
from vibra import app
from vibra.engine.properties.fluid import Fluid
from vibra.engine.properties.material import Material
from vibra.engine.mesher.element_type import *
from vibra.utils.utils import *
from vibra.utils.progress_status import ProgressStatus

from vibra.interface.loading_bar import load_function

import logging
import numpy as np

from collections import defaultdict

class LoadProject:
    def __init__(self):
        super().__init__()

    def initialize(self):
        self.file = app().file
        self.model = app().project.model
        self.properties = app().project.model.properties

    def load(self):
        self.load_geometry()
        self.load_project_libraries()
        self.load_mesh_setup()
        self.load_imported_table_data_from_file()
        self.load_model_properties()
        self.load_analysis_setup()
        # self.load_thumbnail()
        self.load_analysis_results()

    def load_geometry(self):
        geometry_path = self.file.read_geometry_from_file()
        app().main_window.import_geometry(geometry_path)

    def load_project_libraries(self):
        self.load_fluid_library()
        self.load_material_library()

    def load_fluid_library(self):

        self.library_fluids = dict()
        config = self.file.read_fluid_library_from_file()

        if config is None:
            return

        for tag in config.sections():

            section = config[tag]
            keys = section.keys()

            name = section['name']
            fluid_density =  float(section['fluid_density'])
            speed_of_sound =  float(section['speed_of_sound'])
            color =  get_color_rgb(section['color'])
            identifier =  int(section['identifier'])

            if 'isentropic_exponent' in keys:
                isentropic_exponent = float(section['isentropic_exponent'])
            else:
                isentropic_exponent = ""

            if 'thermal_conductivity' in keys:
                thermal_conductivity = float(section['thermal_conductivity'])
            else:
                thermal_conductivity = ""

            if 'specific_heat_Cp' in keys:
                specific_heat_Cp = float(section['specific_heat_Cp'])
            else:
                specific_heat_Cp = ""

            if 'dynamic_viscosity' in keys:
                dynamic_viscosity = float(section['dynamic_viscosity'])
            else:
                dynamic_viscosity = ""
            
            if 'temperature' in keys:
                temperature = float(section['temperature'])
            else:
                temperature = None

            if 'pressure' in keys:
                pressure = float(section['pressure'])
            else:
                pressure = None

            # if 'key_mixture' in keys:
            #     key_mixture = section['key_mixture']
            # else:
            #     key_mixture = None

            # if 'molar_fractions' in keys:
            #     str_molar_fractions = section['molar_fractions']
            #     molar_fractions = get_list_of_values_from_string(str_molar_fractions, int_values=False)
            # else:
            #     molar_fractions = None

            if 'molar_mass' in keys:
                if section['molar_mass'] == "None":
                    molar_mass = None
                else:
                    molar_mass = float(section['molar_mass'])
            else:
                molar_mass = None

            fluid = Fluid(  name = name,
                            fluid_density = fluid_density,
                            speed_of_sound = speed_of_sound,
                            color =  color,
                            identifier = identifier,
                            isentropic_exponent = isentropic_exponent,
                            thermal_conductivity = thermal_conductivity,
                            specific_heat_Cp = specific_heat_Cp,
                            dynamic_viscosity = dynamic_viscosity,
                            temperature = temperature,
                            pressure = pressure,
                            molar_mass = molar_mass  )

            self.library_fluids[identifier] = fluid

    def load_material_library(self):

        self.library_materials = dict()
        config = self.file.read_material_library_from_file()

        if config is None:
            return

        for tag in config.sections():

            section = config[tag]
            # keys = section.keys()

            name = section['name']
            identifier = int(section['identifier'])
            density = float(section['material_density'])
            poisson_ratio = float(section['poisson'])
            young_modulus = float(section['young_modulus']) * 1e9
            thermal_expansion_coefficient = float(section['thermal_expansion_coefficient'])

            material = Material(
                                name = name,
                                identifier = identifier, 
                                density = density,
                                poisson_ratio = poisson_ratio,
                                young_modulus = young_modulus,
                                thermal_expansion_coefficient = thermal_expansion_coefficient, 
                                # color = getColorRGB(section['color'])
                                )
            
            self.library_materials[identifier] = material

    def load_mesh_data_from_file(self, mesh_data: dict):

        logging.info("Loading mesh..." + ProgressStatus(20, 100))

        self.model.mesh.nodal_coordinates = mesh_data["nodal_coordinates"]
        self.model.mesh.lines_connectivity = mesh_data["lines_connectivity"]
        self.model.mesh.faces_connectivity = mesh_data["faces_connectivity"]
        self.model.mesh.solids_connectivity = mesh_data["solids_connectivity"]

        map_line_elements = dict(zip(   mesh_data["map_line_elements"][:, 0],
                                        mesh_data["map_line_elements"][:, 1]   ))

        map_face_elements = dict(zip(   mesh_data["map_face_elements"][:, 0],
                                        mesh_data["map_face_elements"][:, 1]   ))

        map_solid_elements = dict(zip(  mesh_data["map_solid_elements"][:, 0],
                                        mesh_data["map_solid_elements"][:, 1]  ))

        nodes_from_points = dict()
        nodes_from_lines = dict()
        nodes_from_surfaces = dict()
        nodes_from_volumes = dict()

        gmsh_elements_from_lines = dict()
        gmsh_elements_from_surfaces = dict()
        gmsh_elements_from_volumes = dict()

        connectivity_from_surfaces = dict()
        surfaces_from_volumes = dict()
        volume_from_surface = defaultdict(list)

        logging.info("Loading mesh..." + ProgressStatus(60, 100))

        for key, data in mesh_data.items():

            if "nodes_from_points" in key:
                id = int(key.replace("nodes_from_points_", ""))
                nodes_from_points[id] = data              
            
            elif "nodes_from_lines" in key:
                id = int(key.replace("nodes_from_lines_", ""))
                nodes_from_lines[id] = data

            elif "nodes_from_surfaces" in key:
                id = int(key.replace("nodes_from_surfaces_", ""))
                nodes_from_surfaces[id] = data

            elif "nodes_from_volumes" in key:
                id = int(key.replace("nodes_from_volumes_", ""))
                nodes_from_volumes[id] = data

            elif "gmsh_elements_from_lines" in key:
                id = int(key.replace("gmsh_elements_from_lines_", ""))
                gmsh_elements_from_lines[id] = data

            elif "gmsh_elements_from_surfaces" in key:
                id = int(key.replace("gmsh_elements_from_surfaces_", ""))
                gmsh_elements_from_surfaces[id] = data

            elif "gmsh_elements_from_volumes" in key:
                id = int(key.replace("gmsh_elements_from_volumes_", ""))
                gmsh_elements_from_volumes[id] = data

            elif "connectivity_from_surfaces" in key:
                id = int(key.replace("connectivity_from_surfaces_", ""))
                connectivity_from_surfaces[id] = data

            elif "surfaces_from_volumes" in key:
                id = int(key.replace("surfaces_from_volumes_", ""))
                surfaces_from_volumes[id] = data

        for vol_id, face_ids in surfaces_from_volumes.items():
            for face_id in face_ids:
                volume_from_surface[face_id].append(vol_id) 

        self.model.mesh.nodes_from_points = nodes_from_points
        self.model.mesh.nodes_from_lines = nodes_from_lines
        self.model.mesh.nodes_from_surfaces = nodes_from_surfaces
        self.model.mesh.nodes_from_volumes = nodes_from_volumes

        self.model.mesh.map_line_elements = map_line_elements
        self.model.mesh.map_face_elements = map_face_elements
        self.model.mesh.map_solid_elements = map_solid_elements

        self.model.mesh.gmsh_elements_from_lines = gmsh_elements_from_lines
        self.model.mesh.gmsh_elements_from_surfaces = gmsh_elements_from_surfaces
        self.model.mesh.gmsh_elements_from_volumes = gmsh_elements_from_volumes

        self.model.mesh.connectivity_from_surfaces = connectivity_from_surfaces
        self.model.mesh.surfaces_from_volumes = surfaces_from_volumes
        self.model.mesh.volume_from_surface = volume_from_surface

        logging.info("Loading mesh..." + ProgressStatus(80, 100))

        self.model.mesh._maps_lines_by_elements()
        self.model.mesh._maps_surfaces_by_elements()
        self.model.mesh._maps_volumes_by_elements()

        self.model.generated_mesh = True

        logging.info("Loading mesh..." + ProgressStatus(95, 100))
        self.model.mesh._process_solid_elements_connected_to_nodes()

        # logging.info("Loading mesh..." + ProgressStatus(95, 100))
        # self.model.mesh._process_element_average_coordinates()

    def load_mesh_setup(self):

        mesh_setup = self.file.read_mesh_setup_from_file()

        if "element_type" in mesh_setup.keys():
            if "shape_function" in mesh_setup.keys():

                element_type = mesh_setup["element_type"]
                shape_function = mesh_setup["shape_function"]
                
                if element_type == " Tetrahedral" and shape_function == " Linear":
                    solid_element = TETRAHEDRON_4

                elif element_type == " Tetrahedral" and shape_function == " Quadratic":
                    solid_element = TETRAHEDRON_10

                elif element_type == " Hexahedral" and shape_function == " Linear":
                    solid_element = HEXAHEDRON_8

                elif element_type == " Hexahedral" and shape_function == " Quadratic":
                    solid_element = HEXAHEDRON_20

                else:
                    raise NotImplementedError(f"Element type not defined!")
                
                mesh_setup["element_type"] = solid_element
                mesh_setup.pop("shape_function")

                app().project.reset_solutions()
                app().project.set_mesh_setup(mesh_setup)

                mesh_data = self.file.read_mesh_data_from_file()

                if mesh_data:
                    self.load_mesh_data_from_file(mesh_data)
                else:
                    app().project.generate_mesh()
                    app().file.write_mesh_data_in_file()

                self.update_render()

        app().main_window.action_model_workspace_callback()

    def update_render(self):

        logging.info("Updating render..." + ProgressStatus(20, 100))
        app().main_window.configure_mesh_information()

        logging.info("Updating render..." + ProgressStatus(90, 100))
        app().main_window.update_plots()

    def load_imported_table_data_from_file(self):

        imported_tables = app().file.read_imported_table_data_from_file()

        if "acoustic" in imported_tables.keys():
            app().project.model.properties.acoustic_imported_tables = imported_tables["acoustic"]

        if "structural" in imported_tables.keys():
            app().project.model.properties.structural_imported_tables = imported_tables["structural"]

    def load_model_properties(self):

        _properties = self.file.read_model_properties_from_file()

        for key, data in _properties.items():
            if isinstance(data, dict):
                for (property, id), prop_data in data.items():

                    if property == "fluid":
                        fluid_id = prop_data["fluid_id"]
                        if fluid_id not in self.library_fluids.keys():
                            continue
                        else:
                            prop_data = self.library_fluids[fluid_id]

                    elif property == "material":
                        material_id = prop_data["material_id"]
                        if material_id not in self.library_materials.keys():
                            continue
                        else:
                            prop_data = self.library_materials[material_id]

                    if key == "volume_properties":
                        self.properties._set_property(property, prop_data, volume=id)

                    elif key == "surface_properties":
                        self.properties._set_property(property, prop_data, surface=id)

                    elif key == "line_properties":
                        self.properties._set_property(property, prop_data, line=id)

                    elif key == "element_properties":
                        self.properties._set_property(property, prop_data, element=id)

                    elif key == "nodal_properties":
                        self.properties._set_property(property, prop_data, node=id)

                    else:
                        self.properties._set_property(property, prop_data)

    def load_analysis_setup(self):

        analysis_setup = self.file.read_analysis_setup_from_file()

        if analysis_setup:

            f_min = None
            if "f_min" in analysis_setup.keys():
                f_min = analysis_setup["f_min"]

            f_max = None
            if "f_max" in analysis_setup.keys():
                f_max = analysis_setup["f_max"]

            f_step = None
            if "f_step" in analysis_setup.keys():
                f_step = analysis_setup["f_step"]

            if ([f_min, f_max, f_step]).count(None) == 0:
                analysis_setup["frequencies"] = np.arange(f_min, f_max + f_step, f_step)

        app().project.set_analysis_data(analysis_setup)
        app().project.create_solver()

    def load_thumbnail(self):
        thumbnail = self.file.read_thumbnail()
        if thumbnail is not None:
            app().project.thumbnail = thumbnail

    def load_analysis_results(self):
    
        act_modal_analysis = False
        str_modal_analysis = False
        act_harmonic_analysis = False
        str_harmonic_analysis = False

        results_data = self.file.read_results_data_from_file()

        if results_data:
            logging.info("Loading results..." + ProgressStatus(20, 100))
            for key, data in results_data.items():

                if key == "modal_acoustic":
                        if app().project.acoustic_modal_solver is not None:
                            act_modal_analysis = True
                            app().project.acoustic_modal_solver.natural_frequencies = data["natural_frequencies"]
                            app().project.acoustic_modal_solver.modal_shape = data["modal_shape"]
                    
                elif key == "modal_structural":
                        if app().project.structural_modal_solver is not None:
                            str_modal_analysis = True
                            app().project.structural_modal_solver.natural_frequencies = data["natural_frequencies"]
                            app().project.structural_modal_solver.modal_shape = data["modal_shape"]

                elif key == "harmonic_acoustic":
                        if app().project.acoustic_harmonic_solver is not None:
                            act_harmonic_analysis = True
                            app().project.acoustic_harmonic_solver.frequencies = data["frequencies"]
                            app().project.acoustic_harmonic_solver.solution = data["solution"]
                            app().main_window.disable_advanced_acoustic_plots_buttons(False)

                elif key == "harmonic_structural":
                        if app().project.structural_harmonic_solver is not None:
                            str_harmonic_analysis = True
                            app().project.structural_harmonic_solver.frequencies = data["frequencies"]
                            app().project.structural_harmonic_solver.solution = data["solution"]
                else:
                    continue
            
            logging.info("Updating analysis render..." + ProgressStatus(85, 100))
            if act_modal_analysis:
                app().main_window.configure_acoustic_modal_analysis_render_widget()
                app().main_window.menu_widget.update_items()

            elif str_modal_analysis:
                app().main_window.configure_structural_modal_analysis_render_widget()
                app().main_window.menu_widget.update_items()

            elif act_harmonic_analysis:
                app().main_window.configure_acoustic_harmonic_analysis_render_widget()
                app().main_window.menu_widget.update_items()

            elif str_harmonic_analysis:
                return
                app().main_window.viewer_tabs.show_structural_harmonic_analysis()
                app().main_window.menu_widget.update_items()

            else:
                return