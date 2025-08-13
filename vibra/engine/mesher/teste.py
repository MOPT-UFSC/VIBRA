from geometry import Geometry

geometry = Geometry()
geometry.read_file("/home/guilherme/Área de Trabalho/VIBRA/data/examples/geometry_files/cubo_1m3.step")

print(geometry.curves_to_points[12])
# [4, 8]

print(geometry.surfaces_to_curves[5])
# [3, 7, 10, 12]