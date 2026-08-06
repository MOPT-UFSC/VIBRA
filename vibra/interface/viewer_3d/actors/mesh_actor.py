import numpy as np
from molde import Color
from vtkmodules.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray
from vtkmodules.vtkCommonCore import vtkPoints, vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import (
    VTK_HEXAHEDRON,
    VTK_QUADRATIC_HEXAHEDRON,
    VTK_QUADRATIC_TETRA,
    VTK_TETRA,
    vtkCellArray,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkRenderingCore import vtkActor, vtkDataSetMapper

from vibra.engine.mesher.mesh_setup import ElementTopology
from vibra.engine.model import Model
from vibra.engine.properties import Fluid, Material
from vibra.utils.time_utils import function_timer


class MeshActor(vtkActor):
    def __init__(self, model: Model):
        self.model = model

        self.create_variables()
        self.last_mesh_id = 0

    def update(self):
        self.build_mesh()
        self.clear_colors()

    def create_variables(self):
        self.points = vtkPoints()

        self.colors = vtkUnsignedCharArray()
        self.colors.SetName("color")
        self.colors.SetNumberOfComponents(3)

        self.data = vtkUnstructuredGrid()
        self.data.SetPoints(self.points)
        self.data.GetCellData().SetScalars(self.colors)

        self.mapper = vtkDataSetMapper()
        self.mapper.SetInputData(self.data)
        self.SetMapper(self.mapper)

    @function_timer
    def build_mesh(self):
        if self.model is None:
            return

        if self.model.mesh is None:
            return

        mesh_id = id(self.model.mesh)
        if mesh_id == self.last_mesh_id:
            return
        self.last_mesh_id = mesh_id

        coords = self.model.mesh.nodal_coordinates
        self.points.SetData(numpy_to_vtk(coords[:, 1:]))

        match self.model.mesh.element_topology:
            case ElementTopology("tetrahedral", "linear"):
                cell_type = VTK_TETRA
                solids_connectivity = self.model.mesh.solids_connectivity

            case ElementTopology("tetrahedral", "quadratic"):
                cell_type = VTK_QUADRATIC_TETRA
                nodes_order = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 12)
                solids_connectivity = self.model.mesh.solids_connectivity[:, nodes_order]

            case ElementTopology("hexahedral", "linear"):
                cell_type = VTK_HEXAHEDRON
                solids_connectivity = self.model.mesh.solids_connectivity

            case ElementTopology("hexahedral", "quadratic"):
                cell_type = VTK_QUADRATIC_HEXAHEDRON
                nodes_order = (
                    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 
                    15, 17, 13, 20, 22, 23, 21, 14, 16, 18, 19
                )  # fmt: skip
                solids_connectivity = self.model.mesh.solids_connectivity[:, nodes_order]

            case unknown:
                raise NotImplementedError(f"Unknown topology {unknown}.")

        cell_connectivity = solids_connectivity[:, 4:]
        n_cells = len(cell_connectivity)
        helper = np.insert(cell_connectivity, 0, cell_connectivity.shape[1], axis=1)
        vtk_id_array = numpy_to_vtkIdTypeArray(helper.flatten())

        cells = vtkCellArray()
        cells.SetCells(n_cells, vtk_id_array)
        self.data.SetCells(cell_type, cells)
        self.colors.SetNumberOfTuples(n_cells)

        self.mapper.Modified()

    def clear_colors(self):
        if self.model is None:
            return

        for v in self.model.properties.volume_properties.values():
            if isinstance(v, Fluid | Material):
                self.set_color(Color.from_rgb(*v.color))
                return

        self.set_color(Color(255, 255, 255))

    def set_color(self, color: Color):
        rgb = color.to_rgb()
        for i in range(self.colors.GetNumberOfComponents()):
            self.colors.FillComponent(i, rgb[i])
        self.mapper.Modified()

    def paint_surfaces(self, surfaces: np.ndarray[int]):
        pass

    def paint_volumes(self, volumes: np.ndarray[int]):
        pass
