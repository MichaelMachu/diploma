from numpy import linspace

from Bases.FunctionBase import FunctionBase

class LogisticMap(FunctionBase):

    def __init__(self) -> None:
        super().__init__("logistic map", linspace(1.4, 4, 100))

    def get(self, r: float, x: float) -> float:
        return r * x * (1 - x)

    def __str__(self) -> str:
        return "r * x * (1 - x)"