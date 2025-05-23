import gmsh
import numpy as np
from itertools import permutations
from scipy.spatial import KDTree
from scipy.optimize import linear_sum_assignment

class PeriodicMesh():
    """
    This class can be used to set the same number of nodes to two similar faces. However there are some
    prerequisites:
    - The faces must be similar in a sense that they are basically the same, just scaled, translated
    and/or rotated.
    - The faces must have the same number of nodes to use the gmsh method (as of now).
    """
    def __init__(self):
        occ = gmsh.model.occ
        mesh = gmsh.model.mesh
        gmsh.initialize()
        gmsh.option.setNumber("General.Terminal", 0)

        
    def create_basic_boxes(self):
        """
        This metod in only used for testing.
        """
        occ.addBox(0, 0, 0, 1, .5, .5)
        occ.addBox(1.2, 0, 0, 3, 1.5, 1.5)
        gmsh.model.occ.synchronize()
        gmsh.option.setNumber("Mesh.MeshSizeFactor", 0.11)

        surf_orig = 2
        surf_dest = 7
        return surf_orig, surf_dest

    def match_different_point_counts(self, pts_orig, pts_dest):
        """
        Matches points when the surfaces have different numbers of vertices. Only used for testing
        the capabilities of the gmsh metod. Maybe this can be used in the future if gmsh implements
        support for making period meshes for points not literally embedded in the surface.
        """
        src = np.array(pts_orig)
        dst = np.array(pts_dest)
        
        # Cas 1: Same number of nodes - uses existing method.
        if len(src) == len(dst):
            return self.correct_points_order(src, dst)
        
        # Caso 2: More points in the destination - selects the closest ones.
        if len(src) < len(dst):
            tree = KDTree(dst)
            _, indices = tree.query(src)
            matched_dst = dst[np.sort(indices)]
            return matched_dst
        
        # Case 3: More points in the origin - uses optimal correspondance
        cost_matrix = np.zeros((len(src), len(dst)))
        for i, s in enumerate(src):
            for j, t in enumerate(dst):
                cost_matrix[i,j] = np.linalg.norm(s - t)
        
        row_ind, col_ind = linear_sum_assignment(cost_matrix)
        matched_dst = dst[col_ind[np.argsort(row_ind)]]
        
        return matched_dst

    def get_points(self, surface_tag):
        points = set()
        edges = gmsh.model.getBoundary([(2, surface_tag)])
        for edge in edges:
            edge_points = gmsh.model.getBoundary([edge])
            points.update(p[1] for p in edge_points)
        points = list(points)
        print(f"surf {surface_tag} tem os pontos {points}")
        points_coords = [gmsh.model.getValue(0, point, [0, 0, 0]) for point in points]
        return np.array(points_coords)

    def correct_points_order(self, pts_orig, pts_dest):
        A = np.array(pts_orig)
        B = np.array(pts_dest)
        
        if self.is_correct_order(A, B):
            return B
        
        # Tests all the possible permutations
        for perm in permutations(B):
            if self.is_correct_order(A, perm):
                print("Points order automatically corrected.")
                return np.array(perm)
        
        print("It was not possible to obtain points correspondace between the two surfaces.")
        return B  

    def is_correct_order(self, pts_orig, pts_dest):
        vec_orig = pts_orig[1:] - pts_orig[0]
        vec_dest = pts_dest[1:] - pts_dest[0]
        
        scale_x = np.linalg.norm(vec_dest[0]) / np.linalg.norm(vec_orig[0])
        scale_y = np.linalg.norm(vec_dest[1]) / np.linalg.norm(vec_orig[1])
        
        # Verifies consistency, 10% tolerance
        return np.isclose(scale_x, scale_y, rtol=0.1)

    def define_scaled_mesh(self, surf_orig, surf_dest):
        pts_orig = self.get_points(surf_orig)
        pts_dest = self.correct_points_order(pts_orig, self.get_points(surf_dest))
        # tmp = list(get_points(surf_dest))
        # tmp.append(gmsh.model.getValue(0, 13, []))
        # print(tmp)
        # pts_dest = correct_points_order(pts_orig, tmp)
        # print(pts_dest)

        # print(50*"=")
        # print(pts_orig)
        # print(pts_dest)
        # print("diferenca", 50*"=")
        # print(np.round(pts_dest - pts_orig, 2))
            
        # Verificação da ordem dos pontos
        dists_orig = np.linalg.norm(pts_orig[1:] - pts_orig[0], axis=1)
        dists_dest = np.linalg.norm(pts_dest[1:] - pts_dest[0], axis=1)
        print(f"{dists_orig=}")
        print(f"{dists_dest=}")
        scales = dists_dest / dists_orig

        if not np.allclose(scales, scales[0], rtol=0.1):
            print("Erro: Pontos inconsistentes ou geometria inválida para a operação de peridiocidade.")
            gmsh.finalize()
            return
        
        scale = np.mean(scales)
        translation = np.mean(pts_dest, axis=0) - scale * np.mean(pts_orig, axis=0)

        affine = np.eye(4)
        affine[:3, :3] *= scale
        affine[:3, 3] = translation

        print(affine)
        gmsh.model.mesh.setPeriodic(0, [2, 1, 3], [11, 12, 10], affine.flatten().tolist())

        gmsh.model.mesh.setPeriodic(2, [surf_dest], [surf_orig], affine.flatten().tolist())
        mesh.generate(2)

        nodes1, coords1, _ = gmsh.model.mesh.getNodes(dim=2, tag=surf_orig)
        count1 = len(nodes1)

        nodes2, coords2, _ = gmsh.model.mesh.getNodes(dim=2, tag=surf_dest)
        count2 = len(nodes2)

        print(f"nós em surf_orig: {count1}")
        print(f"nós em surf_dest: {count2}")

        gmsh.fltk.run()

    def generate_standard_mesh():
        """
        This method is only used for testing.
        """
        mesh.generate(2)
        # gmsh.option.setNumber("Geometry.Surfaces", 1)
        # gmsh.option.setNumber("Geometry.SurfaceType", 2)
        # gmsh.option.setNumber("Geometry.LabelType", 1)
        # gmsh.option.setNumber("Geometry.PointLabels", 1)
        # gmsh.option.setNumber("Geometry.PointType", 1)
        # gmsh.option.setNumber("Geometry.PointSize", 9)
        # gmsh.option.setNumber("Geometry.CurveType", 1)
        # gmsh.option.setNumber("Geometry.NumSubEdges", 50)

        # Teste da quantidade de nós
        nodes1, coords1, _ = gmsh.model.mesh.getNodes(dim=2, tag=surf_orig)
        count1 = len(nodes1)

        # mesma coisa para surf2
        nodes2, coords2, _ = gmsh.model.mesh.getNodes(dim=2, tag=surf_dest)
        count2 = len(nodes2)

        print(f"nós em surf_orig: {count1}")
        print(f"nós em surf_dest: {count2}")

        gmsh.fltk.run()

    # surf_orig, surf_dest = create_basic_boxes()
    # # # surf_orig, surf_dest = create_complex_curved_structure()
    # # gmsh.option.setNumber("Mesh.SurfaceFaces", 1)
    # # gmsh.option.setNumber("Mesh.MeshSizeFactor", .1)
    # # # mesh.generate(2)
    # # gmsh.fltk.run()
    # # surf_orig = 5
    # # surf_dest = 7
    # define_scaled_mesh(surf_orig, surf_dest)


