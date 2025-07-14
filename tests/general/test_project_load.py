from vibra.project_files.project import Project
from shutil import copy


def test_loading_acoustic_modal_analysis():
    # This loading procedure is terrible
    # we need to simplify it as soon as possible

    project = Project()
    project.initialize_file_and_loader()

    copy("/home/andre/Documents/VIBRA/vibra/interface/data/examples/vibra_files/cilinder.vibra", project.file.path)

    project.reset_variables()
    project.reset_solutions()
    project.loader.initialize()
    project.loader.load()