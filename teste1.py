import gmsh

gmsh.initialize()
occ = gmsh.model.occ

gmsh.option()
gmsh.option.setNumber("Mesh.QualityType", 0)






gmsh.fltk.run()