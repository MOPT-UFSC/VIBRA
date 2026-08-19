from dataclasses import dataclass
from pathlib import Path
import numpy as np


@dataclass
class ImportedDataInterface:
    path: Path = Path()

    def __post_init__(self):
        self.path = Path(self.path)
        self.filename = self.path.name
        self.extension = self.path.suffix

@dataclass
class TextData(ImportedDataInterface):
    data: np.array = None


@dataclass
class SimulationData(ImportedDataInterface):
    nodal_area: np.array = None
    nodal_coordinates: np.array = None


@dataclass
class SpreadsheetSheet:
    sheetname: str
    data: np.ndarray


@dataclass
class SpreadsheetData(ImportedDataInterface):
    sheets: list[SpreadsheetSheet] = None


ImportedData = TextData | SpreadsheetSheet | SimulationData