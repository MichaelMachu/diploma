from numpy.random import normal

from Interfaces.FunctionInterface import FunctionInterface

class ScaledRandomNormal(FunctionInterface):

    def __init__(self, a: float = 4, scale: float = 0.1) -> None:
        self.a = a
        self.scale = scale

    def get(self, r: float, x: float) -> float:
        return self.a * normal(scale=self.scale) * (1 - r)

    def __str__(self) -> str:
        return "{} * normal(scale={}) * (1 - r)".format(self.a, self.scale)