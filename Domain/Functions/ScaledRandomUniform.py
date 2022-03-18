from numpy.random import uniform

from Interfaces.FunctionInterface import FunctionInterface

class ScaledRandomUniform(FunctionInterface):

    def __init__(self, a: float = 4, range: tuple[int, int] = (0, 1)) -> None:
        self.a = a
        self.range = range

    def get(self, r: float, x: float) -> float:
        return self.a * uniform(self.range[0], self.range[1]) * (1 - r)

    def __str__(self) -> str:
        return "{} * uniform({}, {}) * (1 - r)".format(self.a, self.range[0], self.range[1])