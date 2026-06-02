class SolverSubprocessError(RuntimeError):
    def __init__(
        self,
        returncode: int,
        stderr: str = "",
    ) -> None:
        self.returncode = returncode
        self.stderr = stderr.strip()

        message = f"Subprocess failed with returncode {returncode}"
        super().__init__(message)

    def __str__(self) -> str:
        if self.stderr:
            return self.stderr
        return super().__str__()
