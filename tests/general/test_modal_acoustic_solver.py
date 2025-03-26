import pytest

from vibra.engine.assemblers.acoustic_assembler import AcousticAssembler
from vibra.engine.mesher.mesh import Mesh
from vibra.engine.model import Model
from vibra.engine.solvers.acoustic_modal_solver import AcousticModalSolver

@pytest.mark.skip
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

    modal_assembler = AcousticAssembler(model)
    modal_assembler.process_assemble()

    modal_solver = AcousticModalSolver(modal_assembler)
    modal_solver.solve()

    # Não sei o que seria legal de verificar aqui
    assert True


def process_external_model():
    
    coord_path = "data/examples/mesh/muffler/coord_muff.csv"
    connect_path = "data/examples/mesh/muffler/connect_muff.csv"
    
    mesh = Mesh()
    mesh.import_external_nodal_coordinates(coord_path)
    mesh.import_external_connectivity(connect_path)

    model = Model()
    model.generated_mesh = True

    modal_assembler = AcousticAssembler(model)
    modal_assembler.process_assemble()

    modal_solver = AcousticModalSolver(modal_assembler)
    natural_frequencies, modal_shape = modal_solver.solve()


if __name__ == "__main__":
    process_external_model()