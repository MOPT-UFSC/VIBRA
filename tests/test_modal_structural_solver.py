from vibra.engine.mesher.mesh import Mesh
from vibra.engine.model import Model
from vibra.engine.assemblers.acoustic_assembler import AcousticAssembler
from vibra.engine.solvers.acoustic_modal_solver import AcousticModalSolver


def test_modal_structural():
    path = "data/examples/geometry_files/cilindro.step"
    mesh_setup = dict(
        minimum_element_size=30,
        maximum_element_size=30,
    )

    model = Model()
    model.set_geometry_path(path)
    model.set_mesh_setup(mesh_setup)
    model.process_mesh()

    modal_assembler = AcousticAssembler(model)
    modal_assembler.assemble_global_matrices()

    modal_solver = AcousticModalSolver(modal_assembler)
    modal_solver.solve()

    # Não sei o que seria legal de verificar aqui
    assert True 
