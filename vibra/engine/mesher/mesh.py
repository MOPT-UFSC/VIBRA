
from vibra.engine.mesher.element_type import *
from vibra.engine.mesher.geometry_setup import GeometrySetup
from vibra.engine.mesher.reordering import Reordering
from vibra.utils.progress_status import ProgressStatus

from vibra.interface.loading_bar import load_function
from vibra.interface.general.print_message_input import PrintMessageInput

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter
from vtkmodules.vtkCommonDataModel import (
    vtkUnstructuredGrid,
    VTK_TETRA,
    VTK_HEXAHEDRON,
    VTK_QUADRATIC_TETRA,
    VTK_QUADRATIC_HEXAHEDRON
)

import logging
import os
import gmsh
import sys

from pathlib import Path
from tempfile import NamedTemporaryFile
from time import time

import numpy as np
from collections import defaultdict


class Mesh:
    def __init__(self):
        self.geometry_setup = None
        self.mesh_setup = None
        self.reset_variables()

    def reset_variables(self):

        # self.dimension = 0
        self.reordering = None
        self.element_type = DEFAULT_ELEMENT_TYPE
        self.nodal_coordinates = np.array([])
        self.lines_connectivity = np.array([])
        self.faces_connectivity = np.array([])
        self.solids_connectivity = np.array([])

        self.geometry_information = defaultdict(list)

        self.nodes_from_points = dict()
        self.nodes_from_lines = dict()
        self.nodes_from_surfaces = dict()
        self.nodes_from_volumes = dict()

        self.gmsh_elements_from_lines = dict()
        self.gmsh_elements_from_surfaces = dict()
        self.gmsh_elements_from_volumes = dict()

        self.elements_from_line = dict()
        self.elements_from_surface = dict()
        self.elements_from_volume = dict()

        self.line_from_element = dict()
        self.surface_from_element = dict()
        self.volume_from_element = dict()

        self.surfaces_from_volumes = dict()
        self.connectivity_from_surfaces = dict()
        self.nodes_from_face_element = dict()
        self.nodes_from_solid_element = dict()
        self.solid_elements_center = dict()

        self.nodes_out_of_face_element = dict()

        self.surfaces_areas = dict()
        self.bodies_volumes = dict()
        self.surface_area_from_element_integration = dict()

        self.nodal_area = defaultdict(list)
        self.volume_from_surface = defaultdict(list)
        self.face_elements_connected_to_nodes = defaultdict(list)


    @classmethod
    def from_cad(
        cls,
        path: str,
        *,
        minimum_element_size: float = 30.0,
        maximum_element_size: float = 30.0,
        element_type: ElementType = DEFAULT_ELEMENT_TYPE,
        geometry_tolerance: float = 1e-8,
        size_factor: float = 0.5,
        dimension: int = 3,
        threads: int = 1,
        gmsh_gui: bool = False,
        mesh_refinement_parameters = None, 
        mesh_connection = True,
    ):
        """
        Custom constructor so you can create a mesh with this sintax:
        mesh = Mesh.from_cad(...)

        I am not puting it in the default constructor because maybe
        we need to create a mesh from data that is not a CAD.

        Then you can create other constructor like this and avoid a
        lot of confusing if statements in the __init__ method.
        """

        obj = Mesh()
        obj.load_cad(
                    path,
                    minimum_element_size = minimum_element_size,
                    maximum_element_size = maximum_element_size,
                    element_type = element_type,
                    geometry_tolerance = geometry_tolerance,
                    size_factor = size_factor,
                    dimension = dimension,
                    threads = threads,
                    gmsh_gui = gmsh_gui,
                    mesh_refinement_parameters = mesh_refinement_parameters,
                    mesh_connection = mesh_connection,
                    )

        return obj

    def load_cad(
                    self,
                    path: (str | Path),
                    *,
                    minimum_element_size: float = 30.0,
                    maximum_element_size: float = 30.0,
                    element_type: ElementType = DEFAULT_ELEMENT_TYPE,
                    geometry_tolerance: float = 1e-8,
                    size_factor: float = 0.50,
                    dimension: int = 3,
                    threads: int = 4,
                    gmsh_gui: bool = False,
                    mesh_refinement_parameters = None,
                    mesh_connection = True,
                ):

        self.mesh_setup = dict(
                                minimum_element_size = minimum_element_size,
                                maximum_element_size = maximum_element_size,
                                element_type = element_type,
                                geometry_tolerance = geometry_tolerance,
                                size_factor = size_factor,
                                dimension = dimension,
                                threads = threads,
                                mesh_refinement_parameters = mesh_refinement_parameters,
                                mesh_connection = mesh_connection
                                )

        self.mesh_connection = mesh_connection

        gmsh.initialize("", False)

        logging.info("Configuring mesh..." + ProgressStatus(5, 100))
        self._configure_mesh(   element_type,
                                minimum_element_size,
                                maximum_element_size,
                                geometry_tolerance,
                                size_factor,
                                threads,
                                mesh_refinement_parameters,
                            )

        logging.info("Loading geometry..." + ProgressStatus(10, 100))

        gmsh.open(path)

        # if isinstance(path, str):
        #     paths = [paths]

        # # t0 = time()
        # for path in paths:
        #     gmsh.merge(str(path))
        #     # gmsh.open(str(path))

        gmsh.model.occ.synchronize()
        # self.get_geometry_info()

        # self.dimension = min(dimension, gmsh.model.getDimension())
        self.element_type = element_type

        if self.mesh_connection:
            self._merge_nodes_from_adjacent_volumes()

        try:

            logging.info("Generating mesh..." + ProgressStatus(25, 100))
            # gmsh.model.mesh.generate(dim=element_type.dimensions)
            gmsh.model.mesh.generate(dim=dimension)
            logging.info("Generating mesh..." + ProgressStatus(60, 100))
            self.get_geometry_info()

        except:
            gmsh.finalize()

        gmsh.model.mesh.removeDuplicateNodes()

        logging.info("Post-processing mesh..." + ProgressStatus(70, 100))
        self._process_mesh()

        if gmsh_gui:
            if "-nopopup" not in sys.argv:
                gmsh.fltk.run()

        gmsh.finalize()
        # dt = time() - t0
        # print(f"Elapsed time: {dt}")

        logging.info(   f"Mesh generated with {len(self.nodal_coordinates)} nodes"
                        f", {len(self.lines_connectivity)} dim 1"
                        f", {len(self.faces_connectivity)} dim 2"
                        f"and {len(self.solids_connectivity)} dim 3 elements"   )

    def _merge_nodes_from_adjacent_volumes(self):
        """ This method merges all nodes from adjacent volumes.
        """
        volumes_list = gmsh.model.getEntities(3)
        gmsh.model.occ.fragment(volumes_list, volumes_list)
        gmsh.model.occ.synchronize() 

    def import_nodes_coordinates(self, filename):
        header = "Node index || Coordinate x [m] || Coordinate y [m] || Coordinate z [m]"
        return np.loadtxt(
            filename,
            delimiter=";",
            header=header,
            fmt=["%i", "%.16f", "%.16f", "%.16f"],
        )

    def import_faces_connectivity(self, filename):
        header = "Index || Element ID || Face ID || Element type ID || Connected Node IDs"
        return np.loadtxt(filename, delimiter=";", header=header, fmt="%i")

    def import_solids_connectivity(self, filename):
        header = "Index || Solid ID || Element type ID || Element ID || Connected Node IDs"
        return np.loadtxt(filename, delimiter=";", header=header, fmt="%i")
    
    def import_external_nodal_coordinates(self, data, index_zero=True):
        """
        """
        if isinstance(data, list):
            data = np.array(data)

        rows, cols = data.shape

        indexes = data[:,0]
        if index_zero:
            indexes -= 1

        self.nodal_coordinates = np.zeros((rows, cols), dtype=float)
        self.nodal_coordinates[:,0] = indexes
        self.nodal_coordinates[:,1:] = data[:,1:]

    def import_external_connectivity(self, connectivity, index_zero=True, etype_tag=1):
        """
        """
        self.elements_from_volume.clear()

        data = list()
        for key, connect_data in connectivity.items():

            self.elements_from_volume[key[0]] = connect_data[:, 0] - 1

            for nodes in connect_data:
                data.append(nodes)

        data = np.array(data, dtype=int)
        rows, cols = data.shape

        indexes = data[:, 0]
        volumes = data[:, 1]
        nodes_per_element = data[:, 2]
        connect = data[:, 3:]

        if index_zero:
            connect -= 1
            indexes -= 1    

        aux = np.ones(rows)
        self.solids_connectivity = np.zeros((rows, cols+1), dtype=int)
        self.solids_connectivity[:, 0] = indexes
        self.solids_connectivity[:, 1] = volumes
        self.solids_connectivity[:, 2] = aux*etype_tag
        self.solids_connectivity[:, 3] = nodes_per_element
        self.solids_connectivity[:, 4:] = connect

    def export_nodal_coordinates(self, filename):
        fmt = ["%i", "%.16f", "%.16f", "%.16f"]
        header = "Node index || Coordinate x [m] || Coordinate y [m] || Coordinate z [m]"
        np.savetxt(filename, self.nodal_coordinates, delimiter=";", header=header, fmt=fmt)

    def export_face_elements_connectivity(self, filename):
        header = "Index || Element ID || Face ID || Element type ID || Connected Node IDs"
        np.savetxt(filename, self.faces_connectivity, delimiter=";", header=header, fmt="%i")

    def export_solid_elements_connectivity(self, filename):
        header = "Index || Solid ID || Element type ID || Element ID || Connected Node IDs"
        np.savetxt(filename, self.solids_connectivity, delimiter=";", header=header, fmt="%i")

    def export_vtu_file(self, filename):
        """ This methods exports vtu file. """
        points = vtkPoints()
        vtk_dataset = vtkUnstructuredGrid()
        for id, coords in enumerate(self.nodal_coordinates[:,1:]):
            points.InsertPoint(id, list(coords))
            vtk_dataset.SetPoints(points)
        #
        NODES_PER_ELEMENT = len(self.solids_connectivity[0, 4:])
        if NODES_PER_ELEMENT == 4:
            vtk_cell = VTK_TETRA
        elif NODES_PER_ELEMENT == 10:
            vtk_cell = VTK_QUADRATIC_TETRA
        elif NODES_PER_ELEMENT == 8:
            vtk_cell = VTK_HEXAHEDRON
        elif NODES_PER_ELEMENT == 20:
            vtk_cell = VTK_QUADRATIC_HEXAHEDRON
        else:
            raise TypeError("Unsupported element type.")

        n_nodes, nf_elem, ns_elem = self.get_mesh_info()
        vtk_dataset.Allocate(ns_elem)
        for id, connect in enumerate(self.solids_connectivity[:, 4:]):
            vtk_dataset.InsertNextCell(vtk_cell, NODES_PER_ELEMENT, list(connect))

        # unod1 = np.zeros((nnode), dtype=complex)
        # for i in range(nnode):
        #     unod1[i] = P[i, modo1]
                            
        # array1 = vtkDoubleArray()
        # array1.SetNumberOfComponents(1)
        # array1.SetNumberOfTuples(nnode)
        # array1.SetName('Pressure Real')

        # for id in range(nnode):
        #     values1 = [np.real(unod1[id])]
        #     array1.SetTuple(id, values1)
        #     vtk_dataset.GetPointData().AddArray(array1)
            
        writer = vtkXMLUnstructuredGridWriter()
        writer.SetFileName(filename)
        writer.SetInputData(vtk_dataset)
        writer.Write()

    def local_mesh_refine(self, lc_geral, mesh_refinement_parameters):

        fields_list = [1]

        gmsh.model.mesh.field.add("Constant")
        gmsh.model.mesh.field.setNumbers(1, "SurfacesList", [])
        gmsh.model.mesh.field.setNumber(1, "VOut", lc_geral)       

        for size, faces in mesh_refinement_parameters:
            threshold_type = gmsh.model.mesh.field.add("Constant")
            gmsh.model.mesh.field.setNumbers(threshold_type, "SurfacesList", faces)
            gmsh.model.mesh.field.setNumber(threshold_type, "VIn", size)
            fields_list.append(threshold_type)

        minimum_field = gmsh.model.mesh.field.add("Min")
        gmsh.model.mesh.field.setNumbers(minimum_field, "FieldsList", fields_list)
        gmsh.model.mesh.field.setAsBackgroundMesh(minimum_field)

    def _configure_mesh(
                        self,
                        element_type,
                        minimum_element_size,
                        maximum_element_size,
                        tolerance,
                        size_factor,
                        threads,
                        mesh_refinement_parameters=None
                        ):

        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.option.setNumber("General.Verbosity", 0)
        gmsh.option.setNumber("General.NumThreads", threads)
        gmsh.option.setNumber("Geometry.Tolerance", tolerance)

        if size_factor != 0:
            gmsh.option.setNumber("Mesh.MeshSizeFactor", size_factor)

        elif mesh_refinement_parameters:
            self.local_mesh_refine(minimum_element_size, mesh_refinement_parameters)

        else:
            gmsh.option.setNumber("Mesh.MeshSizeMin", minimum_element_size)
            gmsh.option.setNumber("Mesh.MeshSizeMax", maximum_element_size)

        gmsh.option.setNumber("Mesh.Algorithm", element_type.algorithm_2d)
        gmsh.option.setNumber("Mesh.Algorithm3D", element_type.algorithm_3d)
        gmsh.option.setNumber("Mesh.RecombinationAlgorithm", element_type.recombination_algorithm)
        gmsh.option.setNumber("Mesh.SubdivisionAlgorithm", element_type.subdivision_algorithm)
        gmsh.option.setNumber("Mesh.RecombineAll", element_type.recombine_all)
        gmsh.option.setNumber("Mesh.ElementOrder", element_type.element_order)
        gmsh.option.setNumber("Mesh.SecondOrderIncomplete", element_type.second_order_incomplete)


    def _process_mesh(self):
        """
        Transform gmsh data in a more manageable format (aka nodal coords and connectivity).
        """
        indexes, coords, _ = gmsh.model.mesh.getNodes(includeBoundary=True)
        total_nodes = int(np.max(indexes))
        self.nodal_coordinates = np.zeros((total_nodes, 4))
        self.nodal_coordinates[indexes - 1, 1:] = coords.reshape(-1, 3) / 1000
        self.nodal_coordinates[indexes - 1, :1] = indexes.reshape(-1, 1) - 1

        connectivity_dim1 = dict()
        connectivity_dim2 = dict()
        connectivity_dim3 = dict()

        self.nodes_from_points.clear()
        self.nodes_from_lines.clear()
        self.nodes_from_surfaces.clear()
        self.nodes_from_volumes.clear()

        self.gmsh_elements_from_lines.clear()
        self.gmsh_elements_from_surfaces.clear()
        self.gmsh_elements_from_volumes.clear()

        self.connectivity_from_surfaces.clear()

        self.surfaces_from_volumes.clear()
        self.volume_from_surface.clear()
        self.solid_elements_center.clear()

        for dim, tag in gmsh.model.getEntities():

            if dim == 3:
                _, downwards = gmsh.model.getAdjacencies(dim, tag)
                self.surfaces_from_volumes[tag] = list(downwards)
                for surf_id in list(downwards):
                    self.volume_from_surface[surf_id].append(tag)

            elements_data = dict()
            element_types, element_indexes, element_nodes = gmsh.model.mesh.getElements(dim, tag)

            if not element_indexes:
                continue

            for i, element_type in enumerate(element_types):
                _, _, _, nodes_per_element, _, _ = gmsh.model.mesh.getElementProperties(element_type)

                array_element_nodes = np.array(element_nodes[i]).reshape(-1, nodes_per_element)
                array_element_nodes -= 1  # index connectivity from 0

                elements_data[element_type] = { 
                                                "indexes" : element_indexes[i],
                                                "array_element_nodes" : array_element_nodes
                                              }

            if dim == 0:  # Points
                self.nodes_from_points[tag] = int(element_nodes[0]) - 1

            elif dim == 1:  # Lines
                connectivity_dim1[dim, tag] = elements_data
                self.nodes_from_lines[tag] = np.array([*set(element_nodes[0])], dtype=int) - 1
                self.gmsh_elements_from_lines[tag] = np.array([*set(element_indexes[0])], dtype=int)

            elif dim == 2:  # Surfaces
                connectivity_dim2[dim, tag] = elements_data
                self.nodes_from_surfaces[tag] = np.array([*set(element_nodes[0])], dtype=int) - 1
                self.connectivity_from_surfaces[tag] = array_element_nodes
                self.gmsh_elements_from_surfaces[tag] = np.array([*set(element_indexes[0])], dtype=int)

            elif dim == 3:  # Solids
                connectivity_dim3[dim, tag] = elements_data
                self.nodes_from_volumes[tag] = np.array([*set(element_nodes[0])], dtype=int) - 1
                self.gmsh_elements_from_volumes[tag] = np.array([*set(element_indexes[0])], dtype=int)

        logging.info("Post-processing mesh..." + ProgressStatus(80, 100))

        self.lines_connectivity, self.map_line_elements = self._get_connectivity_array(connectivity_dim1)
        self.faces_connectivity, self.map_face_elements = self._get_connectivity_array(connectivity_dim2)
        self.solids_connectivity, self.map_solid_elements = self._get_connectivity_array(connectivity_dim3)

        # np.savetxt("nodal_coordinates.dat", self.nodal_coordinates, delimiter=",", fmt=["%i", "%.16f", "%.16f", "%.16f"])
        # np.savetxt("faces_connectivity.dat", self.faces_connectivity, delimiter=",", fmt="%i")
        # np.savetxt("solids_connectivity.dat", self.solids_connectivity, delimiter=",", fmt="%i")

        # # internal check for solid connectivity
        # aux_zeros = np.zeros(len(self.solids_connectivity[0,4:]))
        # for i, values in enumerate(self.solids_connectivity[:,4:]):
        #     if (aux_zeros == values).all():
        #         print(f"The solid element #{i} doesn't have valid connectivity")

        self._maps_lines_by_elements()
        self._maps_surfaces_by_elements()
        self._maps_volumes_by_elements()


    def _maps_lines_by_elements(self):
        self.line_from_element.clear()
        self.elements_from_line.clear()
        for tag, gmsh_indexes in self.gmsh_elements_from_lines.items():

            n = len(gmsh_indexes)
            internal_indexes = np.zeros(n, dtype=int)

            for i, gmsh_index in enumerate(gmsh_indexes):
                index = self.map_line_elements[gmsh_index]
                internal_indexes[i] = index
                self.line_from_element[index] = tag

            self.elements_from_line[tag] = internal_indexes


    def _maps_surfaces_by_elements(self):
        self.surface_from_element.clear()
        self.elements_from_surface.clear()
        for tag, gmsh_indexes in self.gmsh_elements_from_surfaces.items():

            n = len(gmsh_indexes)
            internal_indexes = np.zeros(n, dtype=int)

            for i, gmsh_index in enumerate(gmsh_indexes):
                index = self.map_face_elements[gmsh_index]
                internal_indexes[i] = index
                self.surface_from_element[index] = tag

            self.elements_from_surface[tag] = internal_indexes


    def _maps_volumes_by_elements(self):
        self.volume_from_element.clear()
        self.elements_from_volume.clear()
        for tag, gmsh_indexes in self.gmsh_elements_from_volumes.items():

            n = len(gmsh_indexes)
            internal_indexes = np.zeros(n, dtype=int)

            for i, gmsh_index in enumerate(gmsh_indexes):
                index = self.map_solid_elements[gmsh_index]
                internal_indexes[i] = index
                self.volume_from_element[index] = tag

            self.elements_from_volume[tag] = internal_indexes


    def _process_face_elements_connected_to_nodes(self, selected_ids : int | list):

        self.nodes_from_face_element.clear()
        self.face_elements_connected_to_nodes.clear()
        self.surface_area_from_element_integration.clear()

        if isinstance(selected_ids, int):
            selected_ids = [selected_ids]

        for tag in selected_ids:
            connect_data = self.connectivity_from_surfaces[tag]
           
            area = 0.
            for element_nodes in connect_data:
                area += self.process_triangular_area_by_nodal_coordinates(element_nodes)

            self.surface_area_from_element_integration[tag] = area

            flat_data = connect_data.flatten()
            face_nodes = np.array([*set(flat_data)], dtype=int)
            for node in face_nodes:

                aux = 0
                for col in range(connect_data.shape[1]):
                    aux += connect_data[:, col] == node

                mask = aux == 1
                self.face_elements_connected_to_nodes[node].append(connect_data[mask, :])

        # import json
        # with open("areas_data.json", "r") as file:
        #     areas_data = json.load(file)


    def _process_solid_elements_connected_to_nodes(self):
        # t0 = time()

        self.nodes_from_solid_element.clear()
        for el, connected_nodes in enumerate(self.solids_connectivity[:, 4:]):
            self.nodes_from_solid_element[el] = connected_nodes

        # dt = time() - t0
        # print(f"Elapsed '_process_solid_elements_connected_to_nodes': {dt} s")


    def get_face_elements_connected_to_nodes(self, node_ids, surface_id=None):

        face_elements_connected_to_nodes = dict()

        Nel = len(node_ids)
        for i, node_id in enumerate(node_ids):
            # t0 = time()
            if surface_id is None:
                mask = np.sum(self.faces_connectivity[:, 4:] == node_id, axis=1) == 1
                face_elements_connected_to_nodes[node_id, surface_id] = self.faces_connectivity[:, 0][mask]
            else:
                connect_from_surface = self.connectivity_from_surfaces[surface_id]
                mask = np.sum(connect_from_surface == node_id, axis=1) == 1
                face_elements_connected_to_nodes[node_id, surface_id] = connect_from_surface[mask, :]

            # dt = time() - t0
            # print(f"Loop time: {dt} s")
            text = f"Obtaining face elements connected to nodes... \nSurface [{surface_id}]"
            logging.info(text + ProgressStatus(int(100 * i / Nel), 100))

        return face_elements_connected_to_nodes


    def get_solid_elements_connected_to_nodes(self, node_ids):

        # t0 = time()

        solid_elements_connected_to_nodes = dict()

        mask_0 = np.sum(np.isin(self.solids_connectivity[:, 4:], node_ids), axis=1) >= 1
        filtered_data = self.solids_connectivity[mask_0, :]

        Nel = len(node_ids)
        for i, node_id in enumerate(node_ids):
            # mask = np.sum(self.solids_connectivity[:, 4:] == node_id, axis=1) == 1
            # solid_elements_connected_to_nodes[node_id] = self.solids_connectivity[:, 0][mask]
            mask = np.sum(filtered_data[:, 4:] == node_id, axis=1) == 1
            solid_elements_connected_to_nodes[node_id] = filtered_data[:, 0][mask]

            logging.info("Obtaining solid elements connected to nodes..." + ProgressStatus(int(100 * i / Nel), 100))

        # dt = time() - t0
        # print(f"Loop time: {dt} s")

        return solid_elements_connected_to_nodes


    def _process_nodal_areas(self, node=None):
        self.nodal_area.clear()
        for node, data in self.face_elements_connected_to_nodes.items():
            for element_nodes in data[0]:
                area = self.process_triangular_area_by_nodal_coordinates(element_nodes)
                if area is not None:
                    self.nodal_area[node].append(area)


    def process_triangular_area_by_nodal_coordinates(self, nodes):
        area = None
        if len(nodes) == 3:

            coord_A = self.nodal_coordinates[nodes[0], 1:]
            coord_B = self.nodal_coordinates[nodes[1], 1:]
            coord_C = self.nodal_coordinates[nodes[2], 1:]

            AB = coord_B - coord_A
            BC = coord_C - coord_B
            area = np.linalg.norm(np.cross(AB, BC)) / 2

        return area


    def get_mesh_info(self):
        n_nodes = self.nodal_coordinates.shape[0]
        n_face_elements = self.faces_connectivity.shape[0]
        n_solid_elements = self.solids_connectivity.shape[0]
        return n_nodes, n_face_elements, n_solid_elements


    def get_geometry_info(self):
        self.geometry_information.clear()
        labels = ["points", "curves", "surfaces", "volumes"]
        for dim, tag in gmsh.model.getEntities():
            label = labels[dim]
            self.geometry_information[label].append(tag)


    def get_model_areas(self, path):
        """This method returns returns the all surface area processed using
        gmsh internal functions.

        """

        self.surfaces_areas.clear()
        self.bodies_volumes.clear()

        # The adoption of quadratic elements ensures better results for area calculations.
        element_type = TETRAHEDRON_10

        gmsh.initialize("", False)
        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.option.setNumber("General.Verbosity", 0)
        gmsh.option.setNumber("General.NumThreads", 4)
        gmsh.merge(str(path))
        # gmsh.open(str(path))

        if self.mesh_connection:
            self._merge_nodes_from_adjacent_volumes()

        gmsh.option.setNumber("Geometry.Tolerance", 1e-6)
        gmsh.option.setNumber("Mesh.MeshSizeFactor", 0.1)
        gmsh.option.setNumber("Mesh.Algorithm", element_type.algorithm_2d)
        gmsh.option.setNumber("Mesh.Algorithm3D", element_type.algorithm_3d)
        gmsh.option.setNumber("Mesh.RecombinationAlgorithm", element_type.recombination_algorithm)
        gmsh.option.setNumber("Mesh.SubdivisionAlgorithm", element_type.subdivision_algorithm)
        gmsh.option.setNumber("Mesh.RecombineAll", element_type.recombine_all)

        gmsh.option.setNumber("Mesh.ElementOrder", element_type.element_order)
        gmsh.option.setNumber("Mesh.SecondOrderIncomplete", element_type.second_order_incomplete)

        gmsh.model.mesh.generate(dim=2)

        for dim, tag in gmsh.model.getEntities():

            if dim == 2:  # Surfaces

                p = gmsh.model.addPhysicalGroup(2, [tag])
                gmsh.plugin.setNumber("MeshVolume", "Dimension", 2)
                gmsh.plugin.setNumber("MeshVolume", "PhysicalGroup", p)
                gmsh.plugin.run("MeshVolume")

                views = gmsh.view.getTags()
                _, _, data = gmsh.view.getListData(views[-1])

                self.surfaces_areas[tag] = data[-1][-1] / (1e6)
                # if tag in [32, 36]:
                #     print(tag, data[-1][-1] / (1e6))

            # maybe it is going to be necessary evaluate the bodies volumes too
            # elif dim == 3:  # Solids

            #     p = gmsh.model.addPhysicalGroup(3, [tag])
            #     gmsh.plugin.setNumber("MeshVolume", "Dimension", 3)
            #     gmsh.plugin.setNumber("MeshVolume", "PhysicalGroup", p)
            #     gmsh.plugin.run("MeshVolume")
            #     views = gmsh.view.getTags()
            #     _, _, data = gmsh.view.getListData(views[-1])

            #     self.bodies_volumes[tag] = data[-1][-1]

        gmsh.finalize()


    def _get_connectivity_array(self, input_dict):
        """
        The returned value is an array where each line is a connectivity
        and the collums follow this order:

        Index || Element index || Solid ID || Element type ID || Node IDS
        """

        if not isinstance(input_dict, dict):
            raise TypeError("get_connectivity_data only accepts dicts as input.")

        max_cols = 0
        n_list = []
        for data_0 in input_dict.values():
            for data_1 in data_0.values():
                if "indexes" in data_1.keys():
                    n_list.append(len(data_1["indexes"]))
                    array_nodes = data_1["array_element_nodes"]
                    if max_cols < array_nodes.shape[1]:
                        max_cols = array_nodes.shape[1]

        n = int(np.sum(n_list))
        output_data = np.zeros((n, max_cols + 4), dtype=int)
        gmsh_elements = np.zeros(n, dtype=int)

        internal_indexes = np.arange(n, dtype=int)
        output_data[:, 0] = internal_indexes 

        start, end, ind = 0, 0, 0
        for (entity_dim, entity_tag), e_data in input_dict.items():

            for etype_tag, data in e_data.items():

                end += n_list[ind]
                indexes = data["indexes"]
                nodes = data["array_element_nodes"]

                rows = len(indexes)
                cols = nodes.shape[1]
                aux = np.ones(rows, dtype=int)

                output_data[start:end, 1] = aux * entity_tag
                output_data[start:end, 2] = aux * etype_tag
                output_data[start:end, 3] = aux * cols
                output_data[start:end, 4 : 4 + cols] = nodes
                gmsh_elements[start:end] = indexes

                start = end
                ind += 1

        map_elements = dict(zip(gmsh_elements, internal_indexes))

        return output_data, map_elements


    def get_array_based_elements_mapping(self, entity="lines"):

        if entity == "lines":
            keys = list(self.map_line_elements.keys())
            values = list(self.map_line_elements.values())
        elif entity == "faces":
            keys = list(self.map_face_elements.keys())
            values = list(self.map_face_elements.values())
        elif entity == "solids":
            keys = list(self.map_solid_elements.keys())
            values = list(self.map_solid_elements.values())
        else:
            return None

        return np.array([keys, values], dtype=int).T


    def _process_element_average_coordinates(self, element_ids):
        """ This method evaluates the element average center coordinates. """

        solid_elements_center = dict()

        for i, element_id in enumerate(element_ids):
            nodes = self.nodes_from_solid_element[element_id]
            solid_elements_center[element_id] = np.average(self.nodal_coordinates[nodes, 1:], axis=0)

        return solid_elements_center

    def get_average_nodal_coordinates(self, surface_ids: list, averaged=False):

        nodal_coordinates = self.nodal_coordinates
        stop, surface_ids = self.check_input_surface_id(surface_ids)

        if stop:
            return list()

        rows = list()
        for surface_id in surface_ids:
            if averaged:
                for row in self.nodes_from_surfaces[surface_id]:
                    rows.append(row)
            else:
                _nodes = list(self.nodes_from_surfaces[surface_id])
                rows.append(_nodes)

        center_coords = list()
        if rows:
            if averaged:
                avg_coords = np.average(nodal_coordinates[rows, 1:], axis=0)   
                center_coords.append(avg_coords)
            else:
                for row in rows:
                    avg_coords = np.average(nodal_coordinates[row, 1:], axis=0)
                    center_coords.append(avg_coords)

        return center_coords


    def get_elements_and_nodes_from_sphere(self, surface_ids, selection_radius, averaged=False, filter_type=0, export_data=False):

        list_center_coords = self.get_average_nodal_coordinates(surface_ids, averaged=averaged)
        if len(list_center_coords) == 0:
            return list(), list()

        selected_elements = list()
        nodes_inside_sphere = list()
        node_indexes = self.nodal_coordinates[:,0]
        nodal_coordinates = self.nodal_coordinates[:,1:]

        for center_coords in list_center_coords:
            
            if filter_type == 0: # filters the elements inside sphere based on elements coordinates center

                filter_radius = 1.1 * selection_radius
                _, filtered_elements = self.get_nodes_inside_sphere_and_its_elements_connected(center_coords, filter_radius)

                if filtered_elements:
                    filtered_solid_elements = self._process_element_average_coordinates(filtered_elements)
                    element_indexes = np.array(list(filtered_solid_elements.keys()), dtype=int)
                    elements_center_coordinates = np.array(list(filtered_solid_elements.values()), dtype=float)
                else:
                    return

                diff_nodes = np.linalg.norm(nodal_coordinates - center_coords, axis=1)
                diff_elem = np.linalg.norm(elements_center_coordinates - center_coords, axis=1) 

                mask_nodes = diff_nodes <= selection_radius
                mask_elem = diff_elem <= selection_radius

                if sum(mask_nodes):
                    for node_id in node_indexes[mask_nodes]:
                        if node_id not in nodes_inside_sphere:
                            nodes_inside_sphere.append(node_id)
            
                if sum(mask_elem):
                    for element_id in element_indexes[mask_elem]:
                        if element_id not in selected_elements:
                            selected_elements.append(element_id)

            else: # filters the elements inside sphere based on nodal coordinates

                diff_nodes = np.linalg.norm(nodal_coordinates - center_coords, axis=1) 
                mask_nodes = diff_nodes <= selection_radius

                if sum(mask_nodes):

                    nodes_inside_sphere = node_indexes[mask_nodes]
                    selection_data = self.get_solid_elements_connected_to_nodes(nodes_inside_sphere)
                    for _node, element_ids in selection_data.items():
                        for element_id in element_ids:
                            if element_id not in selected_elements:
                                selected_elements.append(element_id)

        self.nodes_inside_sphere = nodes_inside_sphere
        self.selected_elements = selected_elements

        if export_data:
            # list_nodes = np.array(nodes_inside_sphere, dtype=int).reshape(-1,1)
            # list_elements = np.array(selected_elements, dtype=int).reshape(-1,1)
            list_nodes = np.array(nodes_inside_sphere).reshape(-1,1)
            list_elements = np.array(selected_elements).reshape(-1,1)
            connectivity = self.solids_connectivity[:, 4:]
            rows = len(list_elements)
            cols = connectivity.shape[1]
            data_elem = np.zeros((rows, cols+1), dtype=int)
            data_elem[:, 0] = selected_elements
            data_elem[:, 1:] = connectivity[selected_elements, :]

            np.savetxt("nodes_inside_sphere.dat", list_nodes, delimiter=";", fmt='%i')
            np.savetxt("selected_elements.dat", list_elements, delimiter=";", fmt='%i')
            np.savetxt("selected_elements_data.dat", data_elem, delimiter=";", fmt="%i")
            print(f"Number of nodes: {len(nodes_inside_sphere)}")
            print(f"Number of elements: {len(selected_elements)}")

        return selected_elements, nodes_inside_sphere


    def get_nodes_inside_sphere_and_its_elements_connected(self, center_coords, selection_radius):

        node_indexes = self.nodal_coordinates[:,0]
        nodal_coordinates = self.nodal_coordinates[:,1:]

        diff_nodes = np.linalg.norm(nodal_coordinates - center_coords, axis=1)
        mask_nodes = diff_nodes <= selection_radius
        nodes_inside_sphere = node_indexes[mask_nodes]

        selection_data = self.get_solid_elements_connected_to_nodes(nodes_inside_sphere)

        _selected_elements = list()
        for _node, element_ids in selection_data.items():
            _selected_elements.extend(element_ids)

        selected_elements = np.array([*set(_selected_elements)], dtype=int)

        return nodes_inside_sphere, list(selected_elements)


    def check_selected_ids(self, selected_ids, selection = "nodes", single_id = False):

        try:

            message = ""
            if isinstance(selected_ids, str):
                tokens = selected_ids.strip().split(",")
                try:
                    tokens.remove("")
                except:
                    pass
                list_ids = list(map(int, tokens))

            elif isinstance(selected_ids, list):
                list_ids = selected_ids

            elif isinstance(selected_ids, (tuple, np.ndarray)):
                list_ids = list(selected_ids)

            all_ids = list()
            if selection == "nodes":
                all_ids = list(self.nodal_coordinates[:, 0])

            elif selection == "face_elements":
                all_ids = list(self.faces_connectivity[:, 0])

            elif selection == "solid_elements":
                all_ids = list(self.solids_connectivity[:, 0])

            elif selection == "lines":
                if "curves" in self.geometry_information.keys():
                    all_ids = self.geometry_information["curves"]

            elif selection == "surfaces":
                if selection in self.geometry_information.keys():
                    all_ids = self.geometry_information["surfaces"]

            elif selection == "volumes":
                if selection in self.geometry_information.keys():
                    all_ids = self.geometry_information["volumes"]

            else:
                return

            _size = len(all_ids)

            if len(list_ids) == 0:
                message = "An empty input field for the Selection ID has been detected. Please, enter a valid Selection ID to proceed."

            elif len(list_ids) >= 1:
                if single_id and len(list_ids) > 1:
                    message = "Multiple Selected IDs"
                else:
                    try:
                        for _id in list_ids:
                            if _id not in all_ids:
                                message = "Dear user, you have typed an invalid entry at the Selected ID input field. "
                                message += f"The input value(s) must be integer(s) number(s) N such that N <= {_size}."
                                break
                    except Exception as error_log:
                        message = "Dear user, you have typed an invalid entry at the Selected ID input field. "
                        message += f"The input value(s) must be integer(s) number(s) N such that N <= {_size}."
                        message += f"\n\n{str(error_log)}"

        except Exception as log_error:
            message = "Wrong input for the Selected ID's. "
            message += f"\n\n{str(log_error)}"

        if message != "":
            window_title = "Error"
            title = "Invalid entry to the Selection ID"
            PrintMessageInput([window_title, title, message])
            return True, list()

        if single_id:
            return False, list_ids[0]
        else:
            return False, list_ids


    def check_input_line_id(self, selected_ids, single_id=False):
        try:
            message = ""
            if isinstance(selected_ids, str):
                tokens = selected_ids.strip().split(",")
                try:
                    tokens.remove("")
                except:
                    pass
                list_ids = list(map(int, tokens))

            elif isinstance(selected_ids, list):
                list_ids = selected_ids

            elif isinstance(selected_ids, (tuple, np.ndarray)):
                list_ids = list(selected_ids)

            line_ids = self.nodes_from_lines.keys()
            _size = len(line_ids)

            if len(list_ids) == 0:
                message = "An empty input field for the Selected ID has been detected. Please, enter a valid Selected ID to proceed."

            elif len(list_ids) >= 1:
                if single_id and len(list_ids) > 1:
                    message = "Multiple Selected IDs"
                else:
                    try:
                        for _id in list_ids:
                            if _id not in line_ids:
                                message = "Dear user, you have typed an invalid entry at the Selected ID input field. "
                                message += f"The input value(s) must be integer(s) number(s) N such that N <= {_size}."
                                break
                    except Exception as error_log:
                        message = "Dear user, you have typed an invalid entry at the Selected ID input field. "
                        message += f"The input value(s) must be integer(s) number(s) N such that N <= {_size}."
                        message += f"\n\n{str(error_log)}"

        except Exception as log_error:
            message = "Wrong input for the Selected ID's. "
            message += f"\n\n{str(log_error)}"

        if message != "":
            window_title = "Error"
            title = "Invalid entry to the Selected ID"
            PrintMessageInput([window_title, title, message])
            return True, list()

        if single_id:
            return False, list_ids[0]
        else:
            return False, list_ids


    def check_input_surface_id(self, selected_ids, single_id=False):
        try:
            message = ""
            if isinstance(selected_ids, str):
                tokens = selected_ids.strip().split(",")
                try:
                    tokens.remove("")
                except:
                    pass
                list_ids = list(map(int, tokens))

            elif isinstance(selected_ids, list):
                list_ids = selected_ids

            elif isinstance(selected_ids, (tuple, np.ndarray)):
                list_ids = list(selected_ids)

            surface_ids = self.nodes_from_surfaces.keys()
            _size = len(surface_ids)

            if len(list_ids) == 0:
                message = "An empty input field for the Surface ID has been detected. Please, enter a valid Surface ID to proceed."

            elif len(list_ids) >= 1:
                if single_id and len(list_ids) > 1:
                    message = "Multiple Selected IDs"
                else:
                    try:
                        for _id in list_ids:
                            if _id not in surface_ids:
                                message = "Dear user, you have typed an invalid entry at the Selected ID input field. "
                                message += f"The input value(s) must be integer(s) number(s) N such that N <= {_size}."
                                break
                    except Exception as error_log:
                        message = "Dear user, you have typed an invalid entry at the Selected ID input field. "
                        message += f"The input value(s) must be integer(s) number(s) N such that N <= {_size}."
                        message += f"\n\n{str(error_log)}"

        except Exception as log_error:
            message = "Wrong input for the Selected ID's. "
            message += f"\n\n{str(log_error)}"

        if message != "":
            window_title = "Error"
            title = "Invalid entry to the Surface ID"
            PrintMessageInput([window_title, title, message])
            return True, list()

        if single_id:
            return False, list_ids[0]
        else:
            return False, list_ids


    def check_input_volume_id(self, selected_ids, single_id=False):
        try:

            message = ""
            if isinstance(selected_ids, str):
                tokens = selected_ids.strip().split(",")
                try:
                    tokens.remove("")
                except:
                    pass
                list_ids = list(map(int, tokens))

            elif isinstance(selected_ids, list):
                list_ids = selected_ids

            elif isinstance(selected_ids, (tuple, np.ndarray)):
                list_ids = list(selected_ids)

            volume_ids = self.nodes_from_volumes.keys()
            _size = len(volume_ids)

            if len(list_ids) == 0:
                message = "An empty input field for the Volume ID has been detected. Please, enter a valid Volume ID to proceed."

            elif len(list_ids) >= 1:
                if single_id and len(list_ids) > 1:
                    message = "Multiple Selected IDs"
                else:
                    try:
                        for _id in list_ids:
                            if _id not in volume_ids:
                                message = "Dear user, you have typed an invalid entry at the Selected ID input field. "
                                message += f"The input value(s) must be integer(s) number(s) N such that N <= {_size}."
                                break
                    except Exception as error_log:
                        message = "Dear user, you have typed an invalid entry at the Selected ID input field. "
                        message += f"The input value(s) must be integer(s) number(s) N such that N <= {_size}."
                        message += f"\n\n{str(error_log)}"

        except Exception as log_error:
            message = "Wrong input for the Selected ID's. "
            message += f"\n\n{str(log_error)}"

        if message != "":
            window_title = "Error"
            title = "Invalid entry to the Volume ID"
            PrintMessageInput([window_title, title, message])
            return True, list()

        if single_id:
            return False, list_ids[0]
        else:
            return False, list_ids


    def _process_nodes_reordering(self, print_log=False):
        return
        """ This method processes the nodes reordering to reduce the global matrices 
            bandwidth and improve the solution performance.
        """
        # print(f"Nodal coordinates: {self.nodal_coordinates.shape}")
        # print(f"Connectivity: {self.solids_connectivity.shape}")
        # np.savetxt("nodal_coordinates.dat", self.nodal_coordinates, delimiter=",", fmt=["%i", "%.16f", "%.16f", "%.16f"])
        # np.savetxt("faces_connectivity.dat", self.faces_connectivity, delimiter=",", fmt='%i')
        # np.savetxt("solids_connectivity.dat", self.solids_connectivity, delimiter=",", fmt='%i')

        t0 = time()
        self.reordering = Reordering(self)
        if print_log:
            dt = time()  - t0
            print(f"Time to process - reordering (1/4): {dt}")
        logging.info("Reordering nodes (1/4)..." + ProgressStatus(20, 100))

        t0 = time()
        self.reordering._process_reordering()
        if print_log:
            dt = time()  - t0
            print(f"Time to process - reordering (2/4): {dt}")
        logging.info("Reordering nodes (2/4)..." + ProgressStatus(60, 100))

        t0 = time()
        self.lines_connectivity = self.reordering.get_new_connectivity(self.lines_connectivity)
        self.faces_connectivity = self.reordering.get_new_connectivity(self.faces_connectivity)
        self.solids_connectivity = self.reordering.get_new_connectivity(self.solids_connectivity)
        if print_log:
            dt = time()  - t0
            print(f"Time to process - reordering (3/4): {dt}")
        logging.info("Reordering nodes (3/4)..." + ProgressStatus(80, 100))

        t0 = time()
        self.nodal_coordinates = self.reordering.get_new_nodal_coordinates()        
        self.nodes_from_lines = self.reordering.updates_nodes_from(self.nodes_from_lines)
        self.nodes_from_surfaces = self.reordering.updates_nodes_from(self.nodes_from_surfaces)
        self.nodes_from_volumes = self.reordering.updates_nodes_from(self.nodes_from_volumes)
        self.connectivity_from_surfaces = self.reordering.updates_nodes_from(self.connectivity_from_surfaces)
        if print_log:
            dt = time()  - t0
            print(f"Time to process - reordering (4/4): {dt}")
        logging.info("Reordering nodes (4/4)..." + ProgressStatus(100, 100))
        
        t0 = time()
        self._process_solid_elements_connected_to_nodes()
        if print_log:
            dt = time()  - t0
            print(f"Time to post-process - reordering (1/2): {dt}")
        
        t0 = time()
        self._process_element_average_coordinates()
        if print_log:    
            dt = time()  - t0
            print(f"Time to post-process - reordering (2/2): {dt}")
         
        # print(f"Nodal coordinates (after): {self.nodal_coordinates.shape}")
        # print(f"Connectivity (after): {self.solids_connectivity.shape}")
        # np.savetxt("nodal_coordinates_reordered.dat", self.nodal_coordinates, delimiter=",", fmt=["%i", "%.16f", "%.16f", "%.16f"])
        # np.savetxt("faces_connectivity_reordered.dat", self.faces_connectivity, delimiter=",", fmt='%i')
        # np.savetxt("solids_connectivity_reordered.dat", self.solids_connectivity, delimiter=",", fmt='%i')


if __name__ == "__main__":
    # path = "C:\\Repositorios\\VibraEngine\\examples\\geometry_files\\Paralelepipedo.STEP"
    # path = "C:\\Repositorios\\VibraEngine\\examples\\geometry_files\\Tetraedro.STEP"
    # path = "C:\\Repositorios\\VibraEngine\\examples\\geometry_files\\Cubo_1m3.STEP"
    # path = "C:\\Repositorios\\VibraEngine\\examples\\geometry_files\\Cilindro.STEP"
    # path = "C:\\Repositorios\\VibraEngine\\examples\\script_files\\script_hex_elements.txt"

    path = "data/geometries/vessel.step"

    if not os.path.exists(path):
        raise FileNotFoundError

    mesh = Mesh()
    mesh.load_cad(path, 100, element_type=TETRAHEDRON_4)
