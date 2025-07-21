import numpy as np

from vibra.project_files.project import Project


def test_loading_acoustic_modal_analysis():
    project = Project()
    project.load_project("tests/general/acoustic_modal.vibra")
    project.run_analysis()

    expected_natural_frequencies = [
        85.86710557336141,
        171.85636214948076,
        258.09255638993875,
        344.7124407831859,
        404.81352711694717,
        404.8233840786405,
        414.0021704248314,
        414.00957786634365,
        431.7379704579161,
    ]

    non_trivial_frequencies = project.acoustic_modal_solver.natural_frequencies[1:]

    assert np.allclose(
        expected_natural_frequencies,
        non_trivial_frequencies,
    )
