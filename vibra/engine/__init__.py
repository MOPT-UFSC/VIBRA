from enum import IntEnum


class AnalysisID(IntEnum):
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
            self.ACOUSTIC_MODAL,
            self.STRUCTURAL_MODAL,
        ]

    def is_harmonic(self):
        return self in [
            self.STRUCTURAL_HARMONIC_DIRECT_METHOD,
            self.STRUCTURAL_HARMONIC_MODE_SUPERPOSITION,
            self.ACOUSTIC_HARMONIC,
            self.COUPLED_HARMONIC_DIRECT_METHOD,
            self.COUPLED_HARMONIC_MODE_SUPERPOSITION,
        ]

    def is_acoustic(self):
        return self in [self.ACOUSTIC_HARMONIC, self.ACOUSTIC_MODAL]

    def is_structural(self):
        return self in [
            self.STRUCTURAL_HARMONIC_DIRECT_METHOD,
            self.STRUCTURAL_HARMONIC_MODE_SUPERPOSITION,
            self.STRUCTURAL_MODAL,
        ]

    def is_coupled(self):
        return self in [
            self.COUPLED_HARMONIC_DIRECT_METHOD,
            self.COUPLED_HARMONIC_MODE_SUPERPOSITION,
        ]

    def is_direct_method(self):
        return self in [
            self.STRUCTURAL_HARMONIC_DIRECT_METHOD,
            self.COUPLED_HARMONIC_DIRECT_METHOD,
        ]
    
    def is_mode_superposition(self):
        return self in [
            self.STRUCTURAL_HARMONIC_MODE_SUPERPOSITION,
            self.COUPLED_HARMONIC_MODE_SUPERPOSITION,
        ]

    def is_static(self):
        return self in [self.STATIC_ANALYSIS]
