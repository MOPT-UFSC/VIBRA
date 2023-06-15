from dataclasses import dataclass
import numpy as np


@dataclass
class ProgressStatus:
    step: int
    max_steps: int
    message: str = ""

    def __str__(self):
        return f"{self.message} {self.step}/{self.max_steps}"

    def __radd__(self, lhs):
        self.message = str(lhs)
        return self
