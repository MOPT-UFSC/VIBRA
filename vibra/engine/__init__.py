from enum import IntEnum


class AnalysisID(IntEnum):
    """
    Enumeration of analysis IDs.

    The functions are used to group similar analysis in a simple manner.
    Although it might not look obvious at first, the methods can be used 
    directly with integers as if they are static methods, just as shown 
    in the following example:

    ```
    >>> AnalysisID.is_modal(4)
    True
    >>> AnalysisID.is_structural(5)
    False
    >>> AnalysisID.features_structural(5)
    True
    ```
    """

    NO_ANALYSIS = -1
    STRUCTURAL_HARMONIC_DIRECT_METHOD = 0
    STRUCTURAL_HARMONIC_MODE_SUPERPOSITION = 1
    STRUCTURAL_MODAL = 2
    ACOUSTIC_HARMONIC = 3
    ACOUSTIC_MODAL = 4
    COUPLED_HARMONIC_DIRECT_METHOD = 5
    COUPLED_HARMONIC_MODE_SUPERPOSITION = 6
    STATIC_ANALYSIS = 7

    def is_modal(self):
        return self in [
            AnalysisID.ACOUSTIC_MODAL,
            AnalysisID.STRUCTURAL_MODAL,
        ]

    def is_harmonic(self):
        return self in [
            AnalysisID.STRUCTURAL_HARMONIC_DIRECT_METHOD,
            AnalysisID.STRUCTURAL_HARMONIC_MODE_SUPERPOSITION,
            AnalysisID.ACOUSTIC_HARMONIC,
            AnalysisID.COUPLED_HARMONIC_DIRECT_METHOD,
            AnalysisID.COUPLED_HARMONIC_MODE_SUPERPOSITION,
        ]

    def is_acoustic(self):
        return self in [
            AnalysisID.ACOUSTIC_HARMONIC,
            AnalysisID.ACOUSTIC_MODAL,
        ]

    def is_structural(self):
        return self in [
            AnalysisID.STRUCTURAL_HARMONIC_DIRECT_METHOD,
            AnalysisID.STRUCTURAL_HARMONIC_MODE_SUPERPOSITION,
            AnalysisID.STRUCTURAL_MODAL,
        ]

    def is_coupled(self):
        return self in [
            AnalysisID.COUPLED_HARMONIC_DIRECT_METHOD,
            AnalysisID.COUPLED_HARMONIC_MODE_SUPERPOSITION,
        ]

    def features_structural(self):
        return self.is_structural() or self.is_coupled()

    def features_acoustic(self):
        return self.is_acoustic() or self.is_coupled()

    def is_direct_method(self):
        return self in [
            AnalysisID.STRUCTURAL_HARMONIC_DIRECT_METHOD,
            AnalysisID.COUPLED_HARMONIC_DIRECT_METHOD,
        ]

    def is_mode_superposition(self):
        return self in [
            AnalysisID.STRUCTURAL_HARMONIC_MODE_SUPERPOSITION,
            AnalysisID.COUPLED_HARMONIC_MODE_SUPERPOSITION,
        ]
