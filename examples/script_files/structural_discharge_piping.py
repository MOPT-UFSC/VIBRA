
from vibra.engine.project import Project
from vibra.utils.interface_utils import SectionPlane, VisualizationFilter, preview_cache


@preview_cache
def setup() -> Project:
    project = Project().load_project("vibra/interface/data/examples/vibra_files/structural_discharge_system.vibra")
    return project


project = setup()

section_plane = SectionPlane(origin=(0, 0, 0), normal=(0, 0, -1))
visualization_filter = VisualizationFilter(points=False, lines=True, faces=True)
