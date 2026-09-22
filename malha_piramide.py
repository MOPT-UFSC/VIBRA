import gmsh
import os
import sys


def create_pyramid_element(element_order: int):

    gmsh.initialize()
    gmsh.option.setNumber("General.Verbosity", 0)

    occ = gmsh.model.occ
    msh = gmsh.model.mesh

    p1 = occ.addPoint(0, 0, 0)
    p2 = occ.addPoint(1, 0, 0)
    p3 = occ.addPoint(1, 1, 0)
    p4 = occ.addPoint(0, 1, 0)
    p5 = occ.addPoint(0.5, 0.5, 1)

    l1 = occ.addLine(p1, p2)
    l2 = occ.addLine(p2, p3)
    l3 = occ.addLine(p3, p4)
    l4 = occ.addLine(p4, p1)
    l5 = occ.addLine(p1, p5)
    l6 = occ.addLine(p2, p5)
    l7 = occ.addLine(p3, p5)
    l8 = occ.addLine(p4, p5)

    cl_base = occ.addCurveLoop([l1, l2, l3, l4])
    s_base = occ.addPlaneSurface([cl_base])

    cl1 = occ.addCurveLoop([l1, l6, -l5])
    s1 = occ.addPlaneSurface([cl1])
    cl2 = occ.addCurveLoop([l2, l7, -l6])
    s2 = occ.addPlaneSurface([cl2])
    cl3 = occ.addCurveLoop([l3, l8, -l7])
    s3 = occ.addPlaneSurface([cl3])
    cl4 = occ.addCurveLoop([l4, l5, -l8])
    s4 = occ.addPlaneSurface([cl4])

    sl = occ.addSurfaceLoop([s_base, s1, s2, s3, s4])
    vol = occ.addVolume([sl])

    occ.synchronize()

    for l in [l1, l2, l3, l4, l5, l6, l7, l8]:
        msh.setTransfiniteCurve(l, 2)

    gmsh.option.setNumber("Mesh.Algorithm3D", 1)  # Delaunay
    gmsh.option.setNumber("Mesh.ElementOrder", 1)
    gmsh.option.setNumber("Mesh.Nodes", 1)
    gmsh.option.setNumber("Mesh.NodeLabels", 1)
    gmsh.option.setNumber("Mesh.SecondOrderIncomplete", 1)

    # gmsh.option.setNumber("Mesh.VolumeLabels", 1)

    msh.generate(1)

    corner_node_tags = msh.getNodes(3, vol, True)[0]
    msh.addElementsByType(vol, 7, [], corner_node_tags)

    msh.setOrder(element_order)

    print("Elementos por dimensao:")
    for dim in range(4):
        types, tags, _ = msh.getElements(dim)
        for t, tt in zip(types, tags):
            name, d, order, num_nodes, _, _ = msh.getElementProperties(int(t))
            print(f"  dim {dim}: {len(tt)}x {name} (tipo {int(t)}, ordem {order}, {num_nodes} nos)")

    element_types, element_indices, element_nodes = msh.getElements(3, vol)
    tipo = int(element_types[0])
    tag = int(element_indices[0][0])
    name, dim, order, num_nodes, _, _ = msh.getElementProperties(tipo)
    print(f"\nPiramide: {name} (tipo {tipo}), ordem {order}, {num_nodes} nos")
    print("Connectivity:", [int(x) for x in element_nodes[0]])

    if element_order == 1:
        reord_indices = [0, 1, 2, 3, 4]
    elif element_order == 2:
        reord_indices = [0, 1, 2, 3, 4, 5, 8, 10, 6, 7, 9, 11, 12]
    else:
        return

    print(f"Ordered connectivity: {element_nodes[0][reord_indices]}")

    jac, det, _ = msh.getJacobian(tag, [0.25, 0.25, 0.25])
    print("det(J):", det)

    gmsh.fltk.run()
    gmsh.write("piramide_second_order.msh")
    gmsh.finalize()

if __name__ == "__main__":

    create_pyramid_element(2)