from vibra.engine.mesher.mesh import Mesh
from vibra.engine.model import Model
from vibra.engine.assemblers.acoustic_modal_assembler import AcousticModalAssembler
from vibra.engine.solvers.modal_solver import ModalSolver


def test_modal_acoustic():
    path = "data/examples/geometry_files/cilindro.step"
    mesh_setup = dict(
        minimum_element_size=30,
        maximum_element_size=30,
    )

    model = Model()
    model.set_geometry_path(path)
    model.set_mesh_setup(mesh_setup)
    model.process_mesh()

    modal_assembler = AcousticModalAssembler(model)
    modal_assembler.assemble_global_matrices()

    modal_solver = ModalSolver(modal_assembler)
    modal_solver.solve()

    # Não sei o que seria legal de verificar aqui
    assert True 
