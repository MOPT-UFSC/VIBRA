from typing import List

from OCC.Core.BRep import BRep_Builder
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs, STEPControl_Reader
from OCC.Core.TopAbs import TopAbs_SOLID
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopoDS import topods, TopoDS_Compound

from PySide6.QtCore import QObject, Signal

from simple_cad.geometry.geometry_models import Imported, BaseGeometry


class GeometryCollection(QObject):
    on_geometries_change = Signal()

    def __init__(self):
        super().__init__()
        self._geometries: List[BaseGeometry] = []

    def __iter__(self):
        for geo in self._geometries:
            yield geo

    def geometryItemChanged(self):
        self.on_geometries_change.emit()

    def appendGeometry(self, geometry: BaseGeometry):
        geometry.on_geometry_change.connect(self.geometryItemChanged)
        geometry.name = self.getProperName(geometry.name)
        self._geometries.append(geometry)
        self.geometryItemChanged()

    def removeGeometry(self, geometry: BaseGeometry):
        self._geometries.remove(geometry)
        self.geometryItemChanged()

    def exportToStep(self, filename='modelo.step'):
        exportToStep(self._geometries, filename)

    def loadStep(self, filename: str, translation=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0)):
        import_reader = loadStep(filename)
        imported = Imported(import_reader, name='Imported', translation=translation, rotation=rotation)
        self.appendGeometry(imported)
        return imported

    def getProperName(self, name: str) -> str:
        current_names = self.getGeometryNames()
        geo_tag = 1
        while True:
            new_name = f"{name} <{geo_tag}>"
            if new_name not in current_names:
                return new_name
            geo_tag += 1

    def getGeometryNames(self) -> list[str]:
        return [geo.name for geo in self._geometries]

    def getGeometryByNameMapping(self) -> dict[str, BaseGeometry]:
        return { geo.name: geo for geo in self._geometries }

    def getGeometryByNames(self, names: list[str]) -> list[BaseGeometry]:
        geo_map = self.getGeometryByNameMapping()
        return [geo_map[name] for name in names]

    def exportSolidsToStep(self, solids: list, filename='selected_solids.step'):
        """Export selected solids to a STEP file."""
        return exportSolidsToStep(solids, filename)


def exportToStep(geometries: List[BaseGeometry], filename):
    step_writer = STEPControl_Writer()
    for geometry in geometries:
        step_writer.Transfer(geometry.GetShape(), STEPControl_AsIs)
    status = step_writer.Write(filename)
    if status == IFSelect_RetDone:
        print("STEP file saved successfully!")


def extractSolidsFromShape(shape):
    """Extract all individual solids from a shape."""
    solids = []
    explorer = TopExp_Explorer(shape, TopAbs_SOLID)
    while explorer.More():
        solid = topods.Solid(explorer.Current())
        solids.append(solid)
        explorer.Next()
    return solids


def exportSolidsToStep(solids: List, filename):
    """Export a list of TopoDS_Solid objects to a STEP file."""

    # Create a compound to hold all solids
    compound = TopoDS_Compound()
    builder = BRep_Builder()
    builder.MakeCompound(compound)

    for i, solid in enumerate(solids):
        print(f"Adding solid {i+1}/{len(solids)} to compound")
        builder.Add(compound, solid)

    # Export the compound
    step_writer = STEPControl_Writer()
    print(f"Transferring compound with {len(solids)} solid(s)...")
    transfer_status = step_writer.Transfer(compound, STEPControl_AsIs)
    print(f"  Transfer status: {transfer_status}")

    print(f"Writing to {filename}...")
    status = step_writer.Write(filename)

    if status == IFSelect_RetDone:
        print(f"STEP file saved successfully with {len(solids)} solid(s)!")
        return True
    else:
        print(f"STEP file write failed with status: {status}")
    return False


def loadStep(filename: str):
    step_reader = STEPControl_Reader()
    status = step_reader.ReadFile(filename)

    if status == IFSelect_RetDone:
        step_reader.TransferRoots()
        return step_reader
