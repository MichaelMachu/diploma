from numpy import linspace
from numpy.random import normal

from Bases.FunctionBase import FunctionBase

class ScaledRandomNormal(FunctionBase):

    def __init__(self, a: float = 4, scale: float = 0.1) -> None:
        super().__init__("scaled normal", linspace(1, 100))
        self.a = a
        self.scale = scale

    def get(self, r: float, x: float) -> float:
        return self.a * normal(scale=self.scale) * (1 - r)

    def __str__(self) -> str:
        #return "{} * normal(scale={}) * (1 - r)".format(self.a, self.scale)
        return "a * normal(scale) * (1 - r)"