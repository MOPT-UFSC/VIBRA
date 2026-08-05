from enum import Enum, auto
import logging
from pypardiso.pardiso_wrapper import PyPardisoSolver, Matrix_type
from scipy.sparse.linalg import LinearOperator
from scipy.sparse import triu, issparse
import numpy as np


class SolverType(Enum):
    PARDISO = auto()
    MUMPS = auto()
    MODAL_SUPERPOSITION = auto()


class MumpsLinearOperator(LinearOperator):
    def __init__(self, ctx, A, is_symmetric: bool):
        ctx.set_matrix(A, symmetric=is_symmetric)
        ctx.factor()
        self.solve = ctx.solve
        LinearOperator.__init__(self, A.dtype, A.shape)

    def _matvec(self, x):
        return self.solve(x.astype(self.dtype))


class PardisoLinearOperator(LinearOperator):
    def __init__(self, ps, A, is_symmetric: bool, est_operations: int | None = None):
        if is_symmetric:
            A = triu(A, format='csr')

        self.calc_counter = 0
        self.last_percentage = -1
        self.estimated_operations = est_operations

        ps.factorize(A)
        self.factorized_A = ps.factorized_A
        self.solve = ps.solve
        LinearOperator.__init__(self, A.dtype, A.shape)

    def _matvec(self, x):
        self.calc_counter += 1

        if self.estimated_operations is not None:
            percentage = min(99, 100 * self.calc_counter // self.estimated_operations)
            if percentage != self.last_percentage:
                logging.info(f"Solving the eigenproblem... [{percentage}/100]")
                self.last_percentage = percentage

        return self.solve(self.factorized_A, x.astype(self.dtype))


class LinearSolver:
    def __init__(self, **kwargs):
        self.is_symmetric = False
        self.linear_operator_class = LinearOperator
        self.is_symmetric_assumption: bool | None = None

    def solve(self, A, F):
        pass

    def clear_memory(self):
        pass

    def build_linear_operator(self, A, **kwargs) -> LinearOperator:
        solver = self.get_solver_instance(A)
        return self.linear_operator_class(solver, A, self.is_symmetric, **kwargs)

    def get_solver_instance(self, A, f=None):
        pass


class PardisoLinearSolver(LinearSolver):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Note: use mtype=3 for full symmetric complex matrix and mtype=6 for upper triangular complex matrix
        self.is_symmetric_assumption = kwargs.get('is_symmetric')
        self.mtype = kwargs.get('mtype')
        self.phase = kwargs.get('phase', 13)
        self.size_limit_storage = kwargs.get('size_limit_storage', 5e8)
        self._solver = None
        self.linear_operator_class = PardisoLinearOperator

    def solve(self, A, F):
        solver = self.get_solver_instance(A, F)
        if self.is_symmetric:
            # convert the symmetric matrix [A] into an upper triangular matrix to enhance the solver's
            # performance and reduce the amount of memory required to compute the solution
            A = triu(A, format="csr")
        return solver.solve(A, F)

    def clear_memory(self):
        if self._solver is not None:
            self._solver.free_memory(everything=True)

    def get_solver_instance(self, A, f=None):
        if self._solver:
            return self._solver
        if self.is_symmetric_assumption is not None:
            self.is_symmetric = self.is_symmetric_assumption
        else:
            self.is_symmetric = check_symmetry(A)
        is_complex = check_complex(A, f)
        if self.mtype is None:
            if self.is_symmetric:
                if is_complex:
                    self.mtype = Matrix_type.CS
                else:
                    self.mtype = Matrix_type.RSI
            else:
                if is_complex:
                    self.mtype = Matrix_type.CNS
                else:
                    self.mtype = Matrix_type.RNS
        print(f"Instantiating Pardiso Solver with matrix flags: is_symmetric: {self.is_symmetric}, is_complex: {is_complex}, mtype: {self.mtype}")
        self._solver = PyPardisoSolver(self.mtype, self.phase, self.size_limit_storage)
        return self._solver


class MumpsLinearSolver(LinearSolver):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.verbose = kwargs.get('verbose', False)
        self._solver = None
        self.linear_operator_class = MumpsLinearOperator

    def solve(self, A, F):
        solver = self.get_solver_instance(A, F)
        solver.set_matrix(A, symmetric=self.is_symmetric)
        solver.factor()
        return solver.solve(F)

    def get_solver_instance(self, A, f=None):
        if self._solver:
            return self._solver
        # local import of mumps for backward compatibility with the current build (without conda)
        from mumps import Context
        self.is_symmetric = check_symmetry(A)
        is_complex = check_complex(A, f)
        print(f"Instantiating MUMPS Solver with matrix flags: is_symmetric: {self.is_symmetric}, is_complex: {is_complex}")
        self._solver = Context(self.verbose)
        return self._solver
    
class ModalSuperpositionSolver(LinearSolver):
    def __init__(self, eigenvectors: np.ndarray, **kwargs):
        super().__init__(**kwargs)
        self.Phi = eigenvectors
        self.PhiH = eigenvectors.conj().T
        self.linear_operator_class = LinearOperator  # Not used

    def solve(self, A, F):
        Zr = np.matmul(self.PhiH, A.dot(self.Phi))
        fr = np.matmul(self.PhiH, F)
        ur = np.linalg.solve(Zr, fr)
        return np.matmul(self.Phi, ur)

    def clear_memory(self):
        pass  # Nothing to clear


def initialize_solver(solver_type: SolverType, **kwargs) -> LinearSolver:
    if solver_type == SolverType.PARDISO:
        return PardisoLinearSolver(**kwargs)
    elif solver_type == SolverType.MUMPS:
        return MumpsLinearSolver(**kwargs)
    elif solver_type == SolverType.MODAL_SUPERPOSITION:
        eigenvectors = kwargs.get("eigenvectors")
        if eigenvectors is None:
            raise ValueError("Eigenvectors must be provided for Modal Superposition Solver.")
        return ModalSuperpositionSolver(eigenvectors)
    else:
        raise ValueError(f"Unknown solver type: {solver_type}")


def check_symmetry(matrix, tol=1e-5) -> bool:
    if matrix.shape[0] != matrix.shape[1]:
        return False

    if issparse(matrix):
        diff = matrix - matrix.T
        if diff.nnz == 0:
            return True
        return np.all(np.abs(diff.data) < tol)
    else:
        return np.allclose(matrix, matrix.T, atol=tol)


def check_complex(A, f=None):
    is_A_complex = np.any(np.iscomplex(A.data))
    is_f_complex = np.any(np.iscomplex(f)) if f is not None else False
    is_complex = is_A_complex or is_f_complex

    return is_complex
