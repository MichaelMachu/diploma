from numpy import sin, linspace

from Bases.FunctionBase import FunctionBase

class Sinus(FunctionBase):

    def __init__(self) -> None:
        super().__init__("sinus", linspace(0, 10, 100, endpoint=False))

    def get(self, r: float, x: float) -> float:
        return sin(r)

    def __str__(self) -> str:
        return "sin(r)"