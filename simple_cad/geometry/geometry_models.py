from math import radians
from typing import Tuple

from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.gp import gp_Trsf, gp_Quaternion, gp_Vec
from PySide6.QtCore import QObject, Signal


class BaseGeometry(QObject):
    on_geometry_change = Signal()

    name: str = ''
    translation: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    rotation: Tuple[float, float, float] = (0.0, 0.0, 0.0)

    def __init__(self, **kwargs):
        super().__init__()
        for (key, value) in kwargs.items():
            setattr(self, key, value)

    def Draw(self):
        pass

    def GetShape(self):
        shape = self.Draw()

        transformation = gp_Trsf()
        x_angle = radians(self.rotation[0])
        y_angle = radians(self.rotation[1])
        z_angle = radians(self.rotation[2])

        quat = gp_Quaternion()
        quat.SetEulerAngles(1, z_angle, y_angle, x_angle)

        translation_vector = gp_Vec(*self.translation)
        transformation.SetTransformation(quat, translation_vector)

        return BRepBuilderAPI_Transform(shape, transformation, True).Shape()

    def __setattr__(self, key, value):
        if key in self.__dict__ and self.__dict__[key] == value:
            return
        self.__dict__[key] = value
        self.on_geometry_change.emit()


class Imported(BaseGeometry):

    def __init__(self, reader, **kwargs):
        super().__init__(**kwargs)
        self.reader = reader

    def Draw(self):
        return self.reader.Shape()


