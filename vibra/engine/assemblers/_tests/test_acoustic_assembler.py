from vibra.engine.assemblers import matrix_helper
from vibra.engine.assemblers.acoustic_assembler import AcousticAssembler
from vibra.engine.model import Model
from scipy.sparse import csr_matrix
import numpy as np


def test_reordering_approach_for_frequency_dependent_acoustic_assembler(viscous_thermal_acoustic_model: Model):
    '''
    Asserting mass and stiffness matrix data using reordering with conventional csr_matrix constructor.
    '''

    assembler = AcousticAssembler(viscous_thermal_acoustic_model)

    assembler.assemble_global_matrices_and_excitations()
    # Enforce assembly with reordering
    reordering = matrix_helper.get_reordering_indices(assembler.ind_rows, assembler.ind_cols)
    factor_K, factor_M, _, _ = assembler.compute_global_matrices_factors(1)
    data_K = assembler.int3d_BtB * factor_K
    data_M = assembler.int3d_NtN * factor_M
    full_stiffness_with_reordering = matrix_helper.reorder_data(data_K, reordering)
    full_mass_with_reordering = matrix_helper.reorder_data(data_M, reordering)
    
    # Assembly matrix using conventional csr_matrix constructor
    full_stiffness = csr_matrix((data_K.flatten(), (assembler.ind_rows, assembler.ind_cols)), shape=(assembler.total_dofs, assembler.total_dofs))
    full_mass = csr_matrix((data_M.flatten(), (assembler.ind_rows, assembler.ind_cols)), shape=(assembler.total_dofs, assembler.total_dofs))

    assert np.allclose(full_stiffness_with_reordering.data, full_stiffness.data)
    assert np.allclose(full_mass_with_reordering.data, full_mass.data)
