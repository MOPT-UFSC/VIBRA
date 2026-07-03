from paraview_file import ParaviewFile

from vibra.external_mesh.external_mesh_data import ExternalMeshData

if __name__ == "__main__":

    data = ExternalMeshData()

    # filenames = ['file_solid285_tet4.cdb',
    #              'file_solid185_hex8.cdb',
    #              'file_solid187_tet10.cdb',
    #              'file_solid186_hex20.cdb']

    # filenames = ['ALLTYPES.txt']
    # filenames = ['various_bodies_and_meshes.cdb']
    filenames = ['suction_silencer_first_stage.dat']

    named_selections = ["input_face", "output_face"]

    for filename in filenames:

        data.reset()
        data.read_file(filename)
        data.set_named_selections(named_selections)

        data.get_data_from_file()

        data.export_nodal_coordinates()
        data.post_process_connectivities()
        data.export_connectivities()
        data.export_named_selection_nodes()
        data.export_named_selection_elements()

        mesh = ParaviewFile()
        mesh.set_nodal_coordinates(data.nodal_coordinates)

        for key, connect in data.solids_connectivities.items():
            body_id, element_type = key
            mesh.set_connectivity(connect)
            mesh.set_element_type(element_type)
            # mesh.reorder_connectivity()
            mesh.generate_vtu()