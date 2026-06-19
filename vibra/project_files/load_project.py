
from vibra import app
from vibra.engine.properties.fluid import Fluid
from vibra.engine.properties.material import Material
from vibra.engine.mesher.element_setup import GMSH_TET4, GMSH_TET10, GMSH_HEX8, GMSH_HEX20

import logging
import numpy as np


class LoadProject:
    def __init__(self):
        super().__init__()

    def initialize(self):
        self.file = app().file
        self.model = app().old_project.model
        self.properties = app().old_project.model.properties

    def load(self):
        logging.info("Loading project... [25/100]")
        self.load_geometry_setup()

        logging.info("Loading project... [30/100]")
        self.load_geometry()

        logging.info("Loading project... [35/100]")
        self.load_geometry_data()

        logging.info("Loading project... [40/100]")
        self.load_mesh_setup()

        logging.info("Loading project... [45/100]")
        self.load_mesh_data()

        logging.info("Loading project... [52/100]")
        self.load_mesh_error_data()

        logging.info("Loading project... [55/100]")
        self.load_project_libraries()

        logging.info("Loading project... [60/100]")
        self.load_imported_table_data_from_file()

        logging.info("Loading project... [65/100]")
        self.load_model_properties()
    
        logging.info("Loading project... [70/100]")
        self.load_analysis_setup()

        logging.info("Loading project... [75/100]")
        self.load_analysis_results()

    def load_geometry_setup(self):
        length_unit, geometry_qf = self.file.read_geometry_setup_from_file()
        self.model.set_length_unit(length_unit=length_unit)
        self.model.set_geometry_quality_factor(geometry_qf=geometry_qf)

    def load_geometry(self):
        geometry_path = self.file.read_geometry_from_file()
        app().main_window.import_geometry_or_mesh(
                                                  geometry_path, 
                                                  update_render=False, 
                                                  ignore_workspaces=True
                                                  )

    def load_project_libraries(self):
        self.fluids_from_library = self.load_fluid_library()
        self.materials_from_library = self.load_material_library()

    def load_fluid_library(self):

        fluids_data = dict()
        fluid_library_data = app().file.read_fluid_library_from_file()
        if fluid_library_data is None:
            return

        for str_fluid_id, fluid_data in fluid_library_data.items():
            if not isinstance(fluid_data, dict):
                continue

            identifier = int(str_fluid_id)

            fluid = Fluid(  
                          name = fluid_data.get("name"),
                          fluid_density = fluid_data.get("fluid_density"),
                          speed_of_sound = fluid_data.get("speed_of_sound"),
                          color =  fluid_data.get("color"),
                          identifier = identifier,
                          isentropic_exponent = fluid_data.get("isentropic_exponent"),
                          thermal_conductivity = fluid_data.get("thermal_conductivity"),
                          specific_heat_Cp = fluid_data.get("specific_heat_Cp"),
                          dynamic_viscosity = fluid_data.get("dynamic_viscosity"),
                          temperature = fluid_data.get("temperature"),
                          pressure = fluid_data.get("pressure"),
                          molar_mass = fluid_data.get("molar_mass"),
                          key_mixture = fluid_data.get("key_mixture"),
                          molar_fractions = fluid_data.get("molar_fractions"),
                          )

            fluids_data[identifier] = fluid

        return fluids_data

    def load_material_library(self):

        materials_data = dict()
        material_library_data = app().file.read_material_library_from_file()
        if material_library_data is None:
            return

        for str_material_id, material_data in material_library_data.items():
            if not isinstance(material_data, dict):
                continue

            identifier = int(str_material_id)

            material = Material(
                                name = material_data.get("name"),
                                identifier = identifier, 
                                material_density = material_data.get("material_density"),
                                poisson_ratio = material_data.get("poisson_ratio"),
                                elasticity_modulus = material_data.get("elasticity_modulus"),
                                thermal_expansion_coefficient = material_data.get("thermal_expansion_coefficient"), 
                                color =  material_data.get("color"),
                                )

            materials_data[identifier] = material

        return materials_data

    def load_geometry_data(self):
        
        self.model.mesh.clear_geometry_data()

        geometry_data = self.file.read_geometry_data_from_file()
        if not geometry_data:
            # forces the project to reset, ensuring backward
            # compatibility with older versions of project files
            app().old_project.reset_solutions()
            self.file.remove_mesh_data_from_project_file()
            self.file.remove_results_data_from_project_file()
            return

        for key in ["points", "lines", "surfaces", "volumes"]:

            data = geometry_data.get(key)
            if data is None:
                continue

            self.model.mesh.geometry_information[key] = [int(value) for value in data]

        for key, data in geometry_data.items():
              
            if "length_from" in key:
                self.model.mesh.length_from_lines = {int(key) : value for key, value in data}

            elif "area_from" in key:
                self.model.mesh.area_from_surfaces = {int(key) : value for key, value in data}

            elif "volume_from" in key:
                self.model.mesh.volume_from_bodies = {int(key) : value for key, value in data}

            elif "surfaces_from_volume" in key:
                tag = int(key.split("_")[-1])
                _data = [int(_id) for _id in data]
                if "cache" in key:
                    self.model.mesh.cache_surfaces_from_volume[tag] = _data
                else:
                    self.model.mesh.surfaces_from_volume[tag] = _data

            elif "lines_from_surface" in key:
                tag = int(key.split("_")[-1])
                _data = [int(_id) for _id in data]
                if "cache" in key:
                    self.model.mesh.cache_lines_from_surface[tag] = _data
                else:
                    self.model.mesh.lines_from_surface[tag] = _data

            elif "points_from_line" in key:
                tag = int(key.split("_")[-1])
                _data = [int(_id) for _id in data]
                if "cache" in key:
                    self.model.mesh.cache_points_from_line[tag] = _data
                else:    
                    self.model.mesh.points_from_line[tag] = _data

        self.model.mesh.process_upwards_adjacencies_from_entities()
        app().main_window.update_geometry_information()

    def load_mesh_data_from_file(self, mesh_data: dict):

        self.model.mesh.clear_mesh_data()

        self.model.mesh.nodal_coordinates = mesh_data["nodal_coordinates"]
        self.model.mesh.lines_connectivity = mesh_data["lines_connectivity"]
        self.model.mesh.faces_connectivity = mesh_data["faces_connectivity"]
        self.model.mesh.solids_connectivity = mesh_data["solids_connectivity"]

        self.model.mesh.cache_nodal_coordinates = mesh_data.get("cache_nodal_coordinates")
        self.model.mesh.cache_lines_connectivity = mesh_data.get("cache_lines_connectivity")
        self.model.mesh.cache_faces_connectivity = mesh_data.get("cache_faces_connectivity")
        self.model.mesh.cache_solids_connectivity = mesh_data.get("cache_solids_connectivity")

        nodes_from_points = mesh_data.get("nodes_from_points")

        if isinstance(nodes_from_points, np.ndarray):
            self.model.mesh.nodes_from_points = {int(key) : int(value) for key, value in nodes_from_points}
            self.model.mesh.points_from_nodes = {value : key for key, value in self.model.mesh.nodes_from_points.items()}

        for key, data in mesh_data.items():
            
            # keep these lines for backwards compatibility
            if "nodes_from_points_" in key:
                tag = int(key.split("_")[-1])
                self.model.mesh.nodes_from_points[tag] = data

            elif "surfaces_from_volume" in key:
                tag = int(key.split("_")[-1])
                _data = [int(_id) for _id in data]
                if "cache" in key:
                    self.model.mesh.cache_surfaces_from_volume[tag] = _data
                else:
                    self.model.mesh.surfaces_from_volume[tag] = _data

            elif "lines_from_surface" in key:
                tag = int(key.split("_")[-1])
                _data = [int(_id) for _id in data]
                if "cache" in key:
                    self.model.mesh.cache_lines_from_surface[tag] = _data
                else:
                    self.model.mesh.lines_from_surface[tag] = _data

            elif "points_from_line" in key:
                tag = int(key.split("_")[-1])
                _data = [int(_id) for _id in data]
                if "cache" in key:
                    self.model.mesh.cache_points_from_line[tag] = _data
                else:    
                    self.model.mesh.points_from_line[tag] = _data

            elif "normals_surface" in key:
                tag = int(key.split("_")[-1])
                self.model.mesh.normals_surface[tag] = data

            elif "curvatures_surface" in key:
                tag = int(key.split("_")[-1])
                self.model.mesh.curvatures_surface[tag] = data

        self.model.mesh.process_upwards_adjacencies_from_entities()

        logging.info("Loading project... [50/100]")
        self.model.mesh.process_mesh_related_mappings("Loading")
        self.model.generated_mesh = True

    def load_mesh_setup(self):

        mesh_setup = self.file.read_mesh_setup_from_file()

        if "element_type" in mesh_setup.keys():
            if "shape_function" in mesh_setup.keys():

                element_type = mesh_setup.get("element_type", "").strip().lower()
                shape_function = mesh_setup.get("shape_function", "").strip().lower()
                
                if element_type == "tetrahedral" and shape_function == "linear":
                    solid_element = GMSH_TET4

                elif element_type == "tetrahedral" and shape_function == "quadratic":
                    solid_element = GMSH_TET10

                elif element_type == "hexahedral" and shape_function == "linear":
                    solid_element = GMSH_HEX8

                elif element_type == "hexahedral" and shape_function == "quadratic":
                    solid_element = GMSH_HEX20

                else:
                    raise NotImplementedError(f'Element type "{element_type}" not defined!')

                algorithm_3d = mesh_setup.get("algorithm_3d")
                if algorithm_3d is not None:
                    solid_element.algorithm_3d = algorithm_3d

                mesh_setup["ElementType"] = solid_element

                app().old_project.reset_solutions()
                app().old_project.set_mesh_setup(mesh_setup)

    def load_mesh_data(self):

        mesh_data = self.file.read_mesh_data_from_file()
        if not mesh_data:
            return

        self.load_mesh_data_from_file(mesh_data)

        geometry_path = self.file.read_geometry_from_file()
        if not self.model.check_path_for_geometry_file(geometry_path):
            self.model.mesh.update_element_type()

    def load_mesh_error_data(self):
        errors_data = self.file.read_errors_data_from_file()
        mesh_error = errors_data.get("mesh_error")
        if not isinstance(mesh_error, dict):
            return

        mesh = app().old_project.model.mesh
        if "collapsed_elements_data" in mesh_error.keys():
            collapsed_elements_data = mesh_error.get("collapsed_elements_data")
            mesh.collapsed_elements_data = collapsed_elements_data

            if isinstance(collapsed_elements_data, dict):
                mesh.collapsed_1d_elements = collapsed_elements_data.get("collpased_1d_elements", set())
                mesh.collapsed_2d_elements = collapsed_elements_data.get("collpased_2d_elements", set())
                mesh.collapsed_3d_elements = collapsed_elements_data.get("collpased_3d_elements", set())

        if "disconnected_nodes_data" in mesh_error.keys():
            mesh.disconnected_nodes_data = mesh_error.get("disconnected_nodes_data", dict())

    # def update_render(self):

    #     logging.info("Updating render... [20/100]")
    #     app().main_window.update_mesh_information()

    #     logging.info("Updating render... [90/100]")
    #     app().main_window.update_plots()

    def load_imported_table_data_from_file(self):

        imported_tables = app().file.read_imported_table_data_from_file()

        if "acoustic" in imported_tables.keys():
            app().old_project.model.properties.acoustic_imported_tables = imported_tables["acoustic"]

        if "structural" in imported_tables.keys():
            app().old_project.model.properties.structural_imported_tables = imported_tables["structural"]

    def load_model_properties(self):

        _properties = self.file.read_model_properties_from_file()

        for key, data in _properties.items():
            if isinstance(data, dict):
                for (property, id), prop_data in data.items():

                    if property == "fluid":
                        fluid_id = prop_data["fluid_id"]
                        if fluid_id not in self.fluids_from_library.keys():
                            continue
                        else:
                            prop_data = self.fluids_from_library[fluid_id]

                    elif property == "material":
                        material_id = prop_data["material_id"]
                        if material_id not in self.materials_from_library.keys():
                            continue
                        else:
                            prop_data = self.materials_from_library[material_id]

                    if key == "volume_properties":
                        self.properties._set_property(property, prop_data, volume=id)
                    
                    elif key == "group_properties":
                        self.properties._set_property(property, prop_data, group=id)

                    elif key == "surface_properties":
                        self.properties._set_property(property, prop_data, surface=id)

                    elif key == "line_properties":
                        self.properties._set_property(property, prop_data, line=id)

                    elif key == "point_properties":
                        self.properties._set_property(property, prop_data, point=id)

                    elif key == "element_properties":
                        self.properties._set_property(property, prop_data, element=id)

                    elif key == "nodal_properties":
                        self.properties._set_property(property, prop_data, node=id)

                    else:
                        self.properties._set_property(property, prop_data)

    def load_analysis_setup(self):
        analysis_setup = self.file.read_analysis_setup_from_file()
        app().old_project.model.old_set_analysis_setup(analysis_setup)
        app().old_project.create_solver()

    def load_thumbnail(self):
        thumbnail = self.file.read_thumbnail()
        if thumbnail is not None:
            app().old_project.thumbnail = thumbnail

    def load_analysis_results(self):

        project = app().old_project
        results_data = self.file.read_results_data_from_file()

        for key, data in results_data.items():
            data: dict

            if key == "modal_acoustic" and project.acoustic_modal_solver is not None:
                if np.iscomplexobj(data["natural_frequencies"]):
                    project.acoustic_modal_solver.complex_natural_frequencies = data.get("natural_frequencies", np.array([]))
                else:
                    project.acoustic_modal_solver.natural_frequencies = data.get("natural_frequencies", np.array([]))
                project.acoustic_modal_solver.solution = data.get("solution")

            elif key == "modal_structural" and project.structural_modal_solver is not None:
                project.structural_modal_solver.natural_frequencies = data.get("natural_frequencies", np.array([]))
                project.structural_modal_solver.displacement_dof = data.get("displacement_dof")
                if isinstance(data.get("displacement_dof"), np.ndarray):
                    project.structural_modal_solver.solution = data.get("solution")

            elif key == "harmonic_acoustic" and project.acoustic_harmonic_solver is not None and project.acoustic_harmonic_solver.project_file is None:
                project.acoustic_harmonic_solver.solution = data.get("solution")
                app().main_window.action_export_element_transfer_data.setDisabled(False)

            elif key == "harmonic_structural" and project.structural_harmonic_solver is not None and project.structural_harmonic_solver.project_file is None:
                project.structural_harmonic_solver.displacement_dof = data.get("displacement_dof")
                if isinstance(data.get("displacement_dof"), np.ndarray):
                    project.structural_harmonic_solver.solution = data.get("solution")

            else:
                continue

        logging.info("Loading project... [85/100]")

        acoustic_harmonic_solver = project.acoustic_harmonic_solver
        if acoustic_harmonic_solver is not None and acoustic_harmonic_solver.project_file is not None:
            self.file.handling_harmonic_solution_results("harmonic_acoustic")          
            acoustic_harmonic_solver.solution = acoustic_harmonic_solver.project_file.get_solution_loader()
            if acoustic_harmonic_solver.solution is None:
                return
            if acoustic_harmonic_solver.solution.has_partial_solutions():
                acoustic_harmonic_solver.solution = None
                project.can_resume_solution = True
        
        structural_harmonic_solver = project.structural_harmonic_solver
        if structural_harmonic_solver is not None and structural_harmonic_solver.project_file is not None:
            self.file.handling_harmonic_solution_results("harmonic_structural")
            structural_harmonic_solver.solution = structural_harmonic_solver.project_file.get_solution_loader()
            if structural_harmonic_solver.solution is None:
                return
            solution = structural_harmonic_solver.solution
            structural_harmonic_solver.displacement_dof = solution.get_extra_data("displacement_dof")
            if solution.has_partial_solutions():
                structural_harmonic_solver.solution = None
                project.can_resume_solution = True

        app().main_window.action_export_element_transfer_data.setDisabled(False)


def convert_two_columns_array_into_numeric_dictionary(input_data: np.ndarray, values_dtype: int | float=int):
    """ This method converts a two columns array into an 
        equivalent numeric dictionary. The elements of the 
        first column are the keys, and the elements of 
        second colum are the values.

        Parameters
        ----------
        input_data: np.ndarray
            the array of two columns to be converted 
            into a numeric dictionary

        values_dtype: int or float
            the values data type

        Return
        ------
        output_data: dict
            the output numeric dictionary
    """
    output_data = dict()
    if len(input_data[0, :]) == 2:       
        for k, v in input_data:
            output_data[int(k)] = values_dtype(v)

    return output_data