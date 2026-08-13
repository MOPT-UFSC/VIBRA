from abc import ABC, abstractmethod
from pathlib import Path

from vibra.interface.user_input.data_handler.imported_data import ImportedData


class IOHandler(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def read(self, file_path: str | Path) -> ImportedData:
        pass

    def save(self):
        pass
