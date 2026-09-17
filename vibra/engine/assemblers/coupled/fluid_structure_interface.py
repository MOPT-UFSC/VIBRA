
from collections import defaultdict

import numpy as np

from vibra.engine.model import Model
from vibra.engine.properties.fluid import Fluid
from vibra.engine.properties.material import Material


class FluidStructureInterface:
    def __init__(self, model : Model):

        self.model = model
        self.properties = model.properties

        self.reset()


    def reset(self):
        pass