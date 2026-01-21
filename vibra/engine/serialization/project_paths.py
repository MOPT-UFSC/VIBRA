import shutil
from pathlib import Path


class ProjectPaths:
    def __init__(self, working_directory: Path | str):
        self.working_directory = Path(working_directory)
        if not self.working_directory.exists():
            self.working_directory.mkdir(parents=True)

        self.project_setup_filepath = self.working_directory / "project_setup.json"
        self.fluid_library_filepath = self.working_directory / "fluid_library.json"
        self.material_library_filepath = self.working_directory / "material_library.json"
        self.geometry_data_filepath = self.working_directory / "geometry_data.hdf5"
        self.model_properties_filepath = self.working_directory / "model_properties.json"
        self.mesh_data_filepath = self.working_directory / "mesh_data.hdf5"
        self.mesh_quality_data_filepath = self.working_directory / "mesh_quality_data.json"
        self.imported_table_data_filepath = self.working_directory / "imported_tables_data.hdf5"
        self.results_data_filepath = self.working_directory / "results_data.hdf5"
        self.thumbnail_filepath = self.working_directory / "thumbnail.png"
        self.harmonic_solution_filepath = self.working_directory / "harmonic_solution.hdf5"
        self.modal_solution_filepath = self.working_directory / "modal_solution.hdf5"
        self.geometry_folder = self.working_directory / "geometry_file"

    def clear_data(self):
        shutil.rmtree(self.working_directory, ignore_errors=True)
        self.working_directory.mkdir(parents=True)

    def is_empty(self):
        return not any(self.working_directory.iterdir())
