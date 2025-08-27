import gmsh
gmsh.initialize()

occ = gmsh.model.occ
mesh = gmsh.model.mesh
option = gmsh.option.setNumber
# gmsh.open("C:\\Users\\B00\\Downloads\\light1_fluid_heat_exchanger_interstage_1.STEP")






# mesh.generate(3)
gmsh.fltk.run()