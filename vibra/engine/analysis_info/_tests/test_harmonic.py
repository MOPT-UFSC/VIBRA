import numpy as np
import pytest

from vibra.engine.analysis_info import HarmonicAnalysisSetup, HarmonicAnalysisSetupList, HarmonicAnalysisSetupRange


def test_abstract_class_initialization():
    with pytest.raises(TypeError):
        HarmonicAnalysisSetup()


def test_interval_configuration():
    setup = HarmonicAnalysisSetupRange(10, 18.2, 1.6)
    assert setup.f_min == 10
    assert setup.f_max == 18.2
    assert setup.f_step == 1.6
    assert setup.f_size == len(setup.frequencies()) == 6

    expected_frequencies = [10.0, 11.6, 13.2, 14.8, 16.4, 18.0]
    assert np.allclose(expected_frequencies, setup.frequencies())

    assert 18 in setup
    assert 0 not in setup

    for a, b in zip(expected_frequencies, setup):
        assert np.allclose(a, b)


def test_unmasked_frequency_configuration():
    expected_frequencies = [9, 18, 126, 127]
    setup = HarmonicAnalysisSetupList(expected_frequencies)
    assert setup.f_min == 9 == min(setup)
    assert setup.f_max == 127 == max(setup)
    assert setup.f_size == 4 == len(setup)
    assert np.allclose(expected_frequencies, setup.frequencies())

    assert 9 in setup
    assert 0 not in setup

    for a, b in zip(expected_frequencies, setup):
        assert np.allclose(a, b)


def test_masked_frequency_configuration():
    frequencies = [9, 18, 126, 127]
    mask = [0, 1, 1, 0]
    expected_frequencies = [18, 126]

    setup = HarmonicAnalysisSetupList(frequencies, mask)
    assert setup.f_min == 18 == min(setup)
    assert setup.f_max == 126 == max(setup)
    assert setup.f_size == 2 == len(setup)
    assert np.allclose(expected_frequencies, setup.frequencies())

    assert 18 in setup
    assert 9 not in setup

    for a, b in zip(expected_frequencies, setup):
        assert np.allclose(a, b)
