from dataclasses import dataclass
import numpy as np


@dataclass
class ImportedData:
    data: np.ndarray
    filename: str = str()
    extension: str = str()
    sheetname: str = str()
