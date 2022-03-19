from numpy import linspace
from numpy.random import uniform

from Bases.FunctionBase import FunctionBase

class ScaledRandomUniform(FunctionBase):

    def __init__(self, a: float = 4, valueRange: tuple[int, int] = (0, 1)) -> None:
        super().__init__("scaled uniform", linspace(1, 100))
        self.a = a
        self.valueRange = valueRange

    def get(self, r: float, x: float) -> float:
        return self.a * uniform(self.valueRange[0], self.valueRange[1]) * (1 - r)

    def __str__(self) -> str:
        return "{} * uniform({}, {}) * (1 - r)".format(self.a, self.valueRange[0], self.valueRange[1])