class ModelStatus:
    materials_setted: bool
    width_setted: bool
    solution_executed: bool


class Model:
    nodes: list
    elements: list
    prescribed_degrees_of_freedom: list
    prescribed_loads: list
    status: ModelStatus
