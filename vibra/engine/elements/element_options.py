
from dataclasses import dataclass, field
from enum import IntEnum


class BbarDilatationalEvaluation(IntEnum):
    VOLUME_AVERAGED = 0
    ELEMENT_CENTRE = 1


@dataclass
class HEX8_structural:
    Bbar_formulation: bool = field(default_factory=False)
    reduced_integration: bool = field(default_factory=False)
    simple_enhanced_strain: bool = field(default_factory=False)
    enhanced_assumed_strain: bool = field(default_factory=False)
    EAS_internal_dofs: int = field(default_factory = 15)
    extra_shape_functions: bool = field(default_factory=False)
    Bbar_dilatational_evaluation: IntEnum = field(default_factory=BbarDilatationalEvaluation.VOLUME_AVERAGED)

    def get_data(self) -> dict:
        data = dict()

        for attr, value in self.__dict__.items():
            if value is None:
                continue

            if "option_" in attr:
                continue

            data[attr] = value

        return data

@dataclass
class TET10_structural:
    option_1: bool = False
    option_2: bool = False
    option_3: bool = False