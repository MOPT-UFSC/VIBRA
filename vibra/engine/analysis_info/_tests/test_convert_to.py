import numpy as np
import pytest

from vibra.engine.analysis_info import (
    AnalysisMethod,
    HarmonicAnalysisSetup,
)


def test_convert_to_preserves_shared_fields():
    range_setup = HarmonicAnalysisSetup(
        f_min=10,
        f_max=20,
        f_step=2,
        analysis_method=AnalysisMethod.MODE_SUPERPOSITION,
        global_damping=(0.1, 0.2, 0.3),
        modes_number=50,
        sigma_factor=0.05,
    )

    list_setup = range_setup.convert_to(HarmonicAnalysisSetup, all_frequencies=range_setup.frequencies())

    assert list_setup.analysis_method == AnalysisMethod.MODE_SUPERPOSITION
    assert list_setup.global_damping == (0.1, 0.2, 0.3)
    assert list_setup.modes_number == 50
    assert list_setup.sigma_factor == 0.05
    assert list_setup.f_min == range_setup.f_min
    assert list_setup.f_max == range_setup.f_max
    assert list_setup.f_size == range_setup.f_size
    assert np.allclose(list_setup.frequencies(), range_setup.frequencies())


def test_convert_to_roundtrip_range_to_list_to_range():
    range_setup = HarmonicAnalysisSetup(
        f_min=10,
        f_max=20,
        f_step=2,
        analysis_method=AnalysisMethod.MODE_SUPERPOSITION,
        global_damping=(0.1, 0.2, 0.3),
        modes_number=50,
        sigma_factor=0.05,
    )

    list_setup = range_setup.convert_to(HarmonicAnalysisSetup, all_frequencies=range_setup.frequencies())

    range_back = list_setup.convert_to(
        HarmonicAnalysisSetup,
        f_min=list_setup.f_min,
        f_max=list_setup.f_max,
        f_step=2,
    )

    assert range_back.analysis_method == AnalysisMethod.MODE_SUPERPOSITION
    assert range_back.global_damping == (0.1, 0.2, 0.3)
    assert range_back.modes_number == 50
    assert range_back.sigma_factor == 0.05
    assert range_back.f_min == list_setup.f_min
    assert range_back.f_max == list_setup.f_max
    assert np.allclose(range_back.frequencies(), list_setup.frequencies())
