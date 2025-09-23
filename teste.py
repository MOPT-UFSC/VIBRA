import gmsh

gmsh.initialize()
gmsh.model.add("distancia")

occ = gmsh.model.occ

# Exemplo: duas linhas (uma reta e um arco só pra ter diferença)
p1 = occ.addPoint(-0.5, 0, 0)
p2 = occ.addPoint(1.5, 0, 0)
line1 = occ.addLine(p1, p2)

p3 = occ.addPoint(0, 1, 0)
p4 = occ.addPoint(1, 1, 0)
p5 = occ.addPoint(0.5, 1.5, 0)
arc = occ.addCircleArc(p3, p5, p4)

occ.synchronize()

# Função para amostrar pontos ao longo de uma curva
def sample_line(line_tag, npts=20):
    pts = []
    # parâmetros vão de 0 a 1
    for i in range(npts + 1):
        t = i / npts
        x, y, z = gmsh.model.getValue(1, line_tag, [t])
        pts.append((x, y, z))
    return pts

# Amostra pontos da linha 1
pts_line1 = sample_line(line1, npts=10)

# Calcula distância de cada ponto até a outra curva
distancias = []
occ.synchronize()
for pt in pts_line1:
    # d = occ.getDistance([(0, -1, pt)], [(1, arc)], False)
    pt_tag = occ.addPoint(*pt)
    d, x1, y1, z1, x2, y2, z2 = occ.getDistance(0, pt_tag, 1, arc)
    occ.remove([(0, pt_tag)])

    p1 = occ.addPoint(x1, y1, z1)
    p2 = occ.addPoint(x2, y2, z2)

    occ.addLine(p1, p2)
    

    
    distancias.append(d)

print("Distâncias da linha 1 até arco em cada ponto:")
occ.synchronize()
# print(distancias)
gmsh.fltk.run()
gmsh.finalize()
