import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from vibra.engine.mesher.visual_mesh import VisualMesh
from time import perf_counter


def show_faces():
    vm = VisualMesh()
    vm.load_file("./data/examples/geometry_files/cilindro.step")

    triangles = vm.coords[vm.triangles]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.add_collection(Poly3DCollection(triangles, edgecolor="k", linewidths=1, alpha=0.8))

    ax.set_xlim([-1000, 1000])
    ax.set_ylim([0, 2000])
    ax.set_zlim([-1000, 1000])

    plt.show()


def show_lines():
    vm = VisualMesh()
    vm.load_file("./data/examples/geometry_files/cilindro.step")

    triangles = vm.coords[vm.segments]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    ax.add_collection(Poly3DCollection(triangles, edgecolor="k", linewidths=1, alpha=0.8))

    ax.set_xlim([-1000, 1000])
    ax.set_ylim([0, 2000])
    ax.set_zlim([-1000, 1000])

    plt.show()


def measure_time():
    s = perf_counter()
    vm = VisualMesh()
    vm.load_file("./data/examples/geometry_files/heat_exchanger_reduced.step")
    e = perf_counter()
    print("Time: ", e - s)


show_faces()
show_lines()
measure_time()
