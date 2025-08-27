import gmsh
def local_mesh_refine(global_size: float | int, refinement_parameters: list):
    fields_list = [1]
    gmsh.model.mesh.field.add("Constant")
    gmsh.model.mesh.field.setNumbers(1, "SurfacesList", [])
    gmsh.model.mesh.field.setNumbers(1, "VolumesList", [])
    gmsh.model.mesh.field.setNumber(1, "VOut", global_size)

    for selection_type, local_size, selection_ids in refinement_parameters:
        threshold_type = gmsh.model.mesh.field.add("Constant")
        if selection_type == "lines":
            gmsh.model.mesh.field.setNumbers(
                threshold_type, "CurvesList", selection_ids
            )
        elif selection_type == "surfaces":
            gmsh.model.mesh.field.setNumbers(
                threshold_type, "SurfacesList", selection_ids
            )
        elif selection_type == "volumes":
            gmsh.model.mesh.field.setNumbers(
                threshold_type, "VolumesList", selection_ids
            )

        gmsh.model.mesh.field.setNumber(threshold_type, "VIn", local_size)
        fields_list.append(threshold_type)

    minimum_field = gmsh.model.mesh.field.add("Min")
    gmsh.model.mesh.field.setNumbers(minimum_field, "FieldsList", fields_list)
    gmsh.model.mesh.field.setAsBackgroundMesh(minimum_field)

gmsh.initialize()
gmsh.model.add("refino_area_linha")

occ = gmsh.model.occ
mesh = gmsh.model.mesh

box1 = occ.addBox(0, 0, 0, 1, 1, 1)
a = 0.02
box2 = occ.addBox(0, 0, 1-a, a, a, a)
occ.synchronize()
occ.cut([(3, box1)], [(3, box2)])
occ.synchronize()

mesh_size = 0.15


# gmsh.option.setNumber("Mesh.CharacteristicLengthMin", mesh_size)
# gmsh.option.setNumber("Mesh.CharacteristicLengthMax", mesh_size)

# gmsh.option.setNumber("Mesh.MeshSizeMax", mesh_size)

lines = [tags for dim, tags in gmsh.model.getEntities(1)]

# for line in lines:
#     start, end = gmsh.model.getValue

lines = [tags for dim, tags in gmsh.model.getEntities(1)]
refined_size = 0.002
small_lines = [12, 15, 18, 13, 10, 2, 3, 14, 9]

small_lines_dimTags = [(1, tag) for tag in small_lines]
print(small_lines_dimTags)


local_mesh_refine(mesh_size, [("lines", refined_size, small_lines)])

# thres = gmsh.model.mesh.field.add("Threshold")
# gmsh.model.mesh.field.setNumber(thres, "SizeMin", 0.05)  # malha fina perto da área pequena
# gmsh.model.mesh.field.setNumber(thres, "SizeMax", 0.5)   # malha grossa longe
# gmsh.model.mesh.field.setNumber(thres, "DistMin", 0.2)
# gmsh.model.mesh.field.setNumber(thres, "DistMax", 1.0)

# gmsh.model.mesh.field.setAsBackgroundMesh(thres)
gmsh.write("cubo_refiamento.step")
gmsh.model.mesh.generate(3)
gmsh.fltk.run()
gmsh.finalize()
