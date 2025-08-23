from vibra.engine.assemblers import matrix_helper
from vibra.engine.assemblers.acoustic_assembler import AcousticAssembler
from vibra.engine.model import Model
from scipy.sparse import csr_matrix


def test_acoustic_stacked_assembler(acoustic_model: Model):
    '''
    Asserting that stacked K and M matrices are computed in the same way as the reference one.
    '''

    assembler = AcousticAssembler(acoustic_model)
    assembler.define_acoustic_elements()

    element_3D = assembler.element_3d
    element_3D.reorder_connect()

    int3d_BtB, int3d_NtN = element_3D.stacked_elementary_matrices_NtN_BtB()

    assembler.gather_data_to_assemble_global_matrices_reference()

    rel_error_K = (int3d_BtB - assembler.int3d_BtB.astype(float)) / assembler.int3d_BtB.astype(float)
    rel_error_M = (int3d_NtN - assembler.int3d_NtN.astype(float)) / assembler.int3d_NtN.astype(float)

    max_error_K = max(abs(rel_error_K.flatten()))
    max_error_M = max(abs(rel_error_M.flatten()))

    assert max_error_M == 0
    assert max_error_K == 0


def test_reordering_approach_for_frequency_dependent_acoustic_assembler(viscous_thermal_acoustic_model: Model):
    '''
    Asserting mass and stiffness matrix data using reordering with conventional csr_matrix constructor.
    '''

    assembler = AcousticAssembler(viscous_thermal_acoustic_model)

    assembler.process_assemble()
    # Enforce assembly with reordering
    reordering = matrix_helper.get_reordering_indexes(assembler.ind_rows, assembler.ind_cols)
    factor_K, factor_M = assembler.compute_global_matrices_factors(1)
    data_K = assembler.int3d_BtB * factor_K
    data_M = assembler.int3d_NtN * factor_M
    full_stiffness_with_reordering = matrix_helper.reorder_data(data_K, reordering)
    full_mass_with_reordering = matrix_helper.reorder_data(data_M, reordering)
    
    # Assembly matrix using conventional csr_matrix constructor
    full_stiffness = csr_matrix((data_K.flatten(), (assembler.ind_rows, assembler.ind_cols)), shape=(assembler.total_dofs, assembler.total_dofs))
    full_mass = csr_matrix((data_M.flatten(), (assembler.ind_rows, assembler.ind_cols)), shape=(assembler.total_dofs, assembler.total_dofs))

    rel_error_stiffness = (full_stiffness_with_reordering.data - full_stiffness.data) / full_stiffness.data
    rel_error_mass = (full_mass_with_reordering.data - full_mass.data) / full_mass.data

    max_error_stiffness = max(abs(rel_error_stiffness.flatten()))
    max_error_mass = max(abs(rel_error_mass.flatten()))

    assert max_error_mass < 1e-15
    assert max_error_stiffness < 1e-12
