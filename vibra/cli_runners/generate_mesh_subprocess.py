import logging
import sys
from pathlib import Path
from typing import Optional

from vibra.engine.mesher.mesh_setup import MeshSetup
from vibra.engine.project import Project

logging.basicConfig(
    level=logging.INFO,
    format="VIBRA_LOG|%(levelname)s|%(message)s",
    stream=sys.stdout,
)


def main(working_dir: Path):
    project = Project(working_dir)

    mesh_setup: Optional[MeshSetup] = project.project_reader.read_mesh_setup()
    geometry_path: Optional[Path] = project.project_reader.read_geometry_path()
    properties = project.project_reader.read_model_properties()

    if mesh_setup is None:
        raise FileNotFoundError(f"No mesh setup found in {project.project_paths.project_setup_filepath}")

    if geometry_path is None or not geometry_path.is_file():
        raise FileNotFoundError(f"No geometry file found from {project.project_paths.project_setup_filepath}")

    project.model.mesh_setup = mesh_setup
    project.model.geometry_path = geometry_path
    project.model.properties = properties

    project.generate_mesh(project.model.mesh_setup)

    if project.model.properties.is_the_surface_property_present_in_the_model("degrees_of_freedom_decoupling"):
        project.update_model_properties_file()


if __name__ == "__main__":
    import traceback

    import gmsh

    try:
        main()
    except Exception:
        logging.error("Generate mesh subprocess failed.")
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
    else:
        logging.info("Generate mesh subprocess complete")
    finally:
        if gmsh.isInitialized():
            gmsh.finalize()
