
from dataclasses import dataclass
from enum import IntEnum


class BbarDilatationalEvaluation(IntEnum):
    VOLUME_AVERAGED = 0
    ELEMENT_CENTRE = 1


@dataclass
class HEX8_structural:
    Bbar_formulation: bool = False
    reduced_integration: bool = False
    simple_enhanced_strain: bool = False
    enhanced_assumed_strain: bool = False
    EAS_internal_dofs: int = 9+4
    extra_shape_functions: bool = False
    Bbar_dilatational_evaluation: IntEnum = BbarDilatationalEvaluation.VOLUME_AVERAGED

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