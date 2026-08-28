import gmsh
import numpy as np


def initialize_gmsh_and_create_meshed_cube():

    # length dimension in millimeters
    length = 2000

    # base dimension in millimeters
    base = 200

    # height dimension in millimeters
    height = 300

    gmsh.initialize()
    cube = gmsh.model.occ.addBox(0, 0, 0, length, height, base)
    gmsh.model.occ.synchronize()

    lines = gmsh.model.getEntities(dim=1)
    lines_tags = [tag for dim, tag in lines]

    surfaces = gmsh.model.getEntities(dim=2)
    surface_tags = [tag for dim, tag in surfaces]

    num_nodes = 10
    for tag in lines_tags:
        gmsh.model.mesh.setTransfiniteCurve(tag, num_nodes)

    for tag in surface_tags:
        gmsh.model.mesh.setTransfiniteSurface(tag)
        gmsh.model.mesh.setRecombine(2, tag)

    gmsh.model.mesh.setTransfiniteVolume(cube)

    gmsh.model.mesh.setRecombine(3, cube)
    gmsh.option.setNumber("Mesh.ElementOrder", 2)
    gmsh.option.setNumber("Mesh.SecondOrderIncomplete", True)

    gmsh.model.mesh.generate(3)

    post_process_mesh()

    gmsh.fltk.run()
    gmsh.write("rectangular_cavity_hex20.nas")
    gmsh.finalize()


def get_connectivity_array(input_dict):
    """
    The returned value is an array where each line is a connectivity
    and the colums follow this order:

    Element index || Line/Face/Solid tag || Element type || Nodes per element || Connectivity
    """

    if not isinstance(input_dict, dict):
        raise TypeError("get_connectivity_data only accepts dicts as input.")

    max_cols = 0
    n_list = list()
    for data_0 in input_dict.values():
        for data_1 in data_0.values():
            if "indices" in data_1.keys():
                n_list.append(len(data_1["indices"]))
                array_nodes = data_1["array_element_nodes"]
                if max_cols < array_nodes.shape[1]:
                    max_cols = array_nodes.shape[1]

    n = int(np.sum(n_list))
    output_data = np.zeros((n, max_cols + 4), dtype=int)
    gmsh_elements = np.zeros(n, dtype=int)

    internal_indices = np.arange(n, dtype=int)
    output_data[:, 0] = internal_indices

    start, end, ind = 0, 0, 0
    for (entity_dim, entity_tag), e_data in input_dict.items():
        for etype_tag, data in e_data.items():
            end += n_list[ind]
            indices = data["indices"]
            connectivity = data["array_element_nodes"]

            rows = len(indices)
            cols = connectivity.shape[1]
            aux = np.ones(rows, dtype=int)

            output_data[start:end, 1] = aux * entity_tag
            output_data[start:end, 2] = aux * etype_tag
            output_data[start:end, 3] = aux * cols
            output_data[start:end, 4 : 4 + cols] = connectivity
            gmsh_elements[start:end] = indices

            start = end
            ind += 1

    map_elements = dict(zip(gmsh_elements, internal_indices))

    return output_data, map_elements


def post_process_mesh():

    indices, coords, _ = gmsh.model.mesh.getNodes(includeBoundary=True)
    total_nodes = int(np.max(indices))

    unit_length_factor = 1e-3
    nodal_coordinates = np.zeros((total_nodes, 4))
    nodal_coordinates[indices - 1, 1:] = coords.reshape(-1, 3) * unit_length_factor
    nodal_coordinates[indices - 1, :1] = indices.reshape(-1, 1) - 1

    connectivity_dim1 = dict()
    connectivity_dim2 = dict()
    connectivity_dim3 = dict()

    for dim, tag in gmsh.model.getEntities():
        elements_data = dict()
        element_types, element_indices, element_nodes = gmsh.model.mesh.getElements(dim, tag)

        if not element_indices:
            continue

        for i, element_type in enumerate(element_types):
            _, _, _, nodes_per_element, _, _ = gmsh.model.mesh.getElementProperties(
                element_type
            )

            array_element_nodes = np.array(element_nodes[i]).reshape(
                -1, nodes_per_element
            )
            # array_element_nodes -= 1

            elements_data[element_type] = {
                "indices": element_indices[i],
                "array_element_nodes": array_element_nodes,
            }

        if dim == 0:  # Points
            node_id = element_nodes[0][0] - 1

        elif dim == 1:  # Lines
            connectivity_dim1[dim, tag] = elements_data

        elif dim == 2:  # Surfaces
            connectivity_dim2[dim, tag] = elements_data

        elif dim == 3:  # Solids
            connectivity_dim3[dim, tag] = elements_data

    lines_connectivity, map_line_elements = get_connectivity_array(connectivity_dim1)
    faces_connectivity, map_face_elements = get_connectivity_array(connectivity_dim2)
    solids_connectivity, map_solid_elements = get_connectivity_array(connectivity_dim3)

    print(faces_connectivity)
    print(solids_connectivity)

    # indices = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 11, 13, 9, 10, 12, 14, 15, 16, 18, 19, 17], dtype=int)
    indices = np.array([4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 17, 13, 20, 22, 23, 21, 14, 16, 18, 19], dtype=int)

    print(solids_connectivity[:, indices])


if __name__ == "__main__":

    initialize_gmsh_and_create_meshed_cube()