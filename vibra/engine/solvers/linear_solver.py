from enum import Enum, auto
from pypardiso.pardiso_wrapper import PyPardisoSolver, Matrix_type
from scipy.sparse.linalg import LinearOperator
from scipy.sparse import triu


class SolverType(Enum):
    PARDISO = auto()
    MUMPS = auto()


class MumpsLinearOperator(LinearOperator):
    def __init__(self, ctx, A):
        ctx.set_matrix(A)
        ctx.factor()
        self.solve = ctx.solve
        LinearOperator.__init__(self, A.dtype, A.shape)

    def _matvec(self, x):
        return self.solve(x.astype(self.dtype))


class PardisoLinearOperator(LinearOperator):
    def __init__(self, ps, A):
        symmetric_matrices = [Matrix_type.CS, Matrix_type.RSS, Matrix_type.RSPD, Matrix_type.RSI, Matrix_type.CSS]
        if ps.mtype in symmetric_matrices:
            ps.factorize(triu(A, format='csr'))
        else:
            ps.factorize(A)
        self.factorized_A = ps.factorized_A
        self.solve = ps.solve
        LinearOperator.__init__(self, A.dtype, A.shape)

    def _matvec(self, x):
        return self.solve(self.factorized_A, x.astype(self.dtype))


class LinearSolver:
    def __init__(self, is_complex: bool, is_symmetric: bool, **kwargs):
        pass

    def solve(self, A, F):
        pass

    def clear_memory(self):
        pass

    def build_linear_operator(self, A) -> LinearOperator:
        pass


class PardisoLinearSolver(LinearSolver):
    def __init__(self, is_complex: bool, is_symmetric: bool, **kwargs):
        # Note: use mtype=3 for full symmetric complex matrix and mtype=6 for upper triangular complex matrix
        mtype = kwargs.get('mtype')
        if mtype is None:
            if is_complex:
                if is_symmetric:
                    mtype = Matrix_type.CS
                else:
                    mtype = Matrix_type.CNS
            else:
                if is_symmetric:
                    mtype = Matrix_type.RSI
                else:
                    mtype = Matrix_type.RNS

        phase = kwargs.get('phase', 13)
        size_limit_storage = kwargs.get('size_limit_storage', 5e7)
        self._solver = PyPardisoSolver(mtype, phase, size_limit_storage)

    def solve(self, A, F):
        return self._solver.solve(A, F)

    def clear_memory(self):
        self._solver.free_memory(everything=True)

    def build_linear_operator(self, A) -> LinearOperator:
        return PardisoLinearOperator(self._solver, A)


class MumpsLinearSolver(LinearSolver):
    def __init__(self, is_complex: bool, is_symmetric: bool, **kwargs):
        # local import of mumps for backward compatibility with the current build (without conda)
        from mumps import Context
        self.is_complex = is_complex
        self.is_symmetric = is_symmetric
        verbose = kwargs.get('verbose', False)
        self._solver = Context(verbose)

    def solve(self, A, F):
        self._solver.set_matrix(A, symmetric=self.is_symmetric)
        self._solver.factor()
        return self._solver.solve(F)

    def build_linear_operator(self, A) -> LinearOperator:
        return MumpsLinearOperator(self._solver, A)


def initialize_solver(solver_type: SolverType, is_complex: bool = False, is_symmetric: bool = True,
                      **kwargs) -> LinearSolver:
    if solver_type == SolverType.PARDISO:
        return PardisoLinearSolver(is_complex, is_symmetric, **kwargs)
    elif solver_type == SolverType.MUMPS:
        return MumpsLinearSolver(is_complex, is_symmetric, **kwargs)
