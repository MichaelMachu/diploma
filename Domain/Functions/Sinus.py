from numpy import sin

from Interfaces.FunctionInterface import FunctionInterface

class Sinus(FunctionInterface):

    def get(self, r: float, x: float) -> float:
        return sin(r)

    def __str__(self) -> str:
        return "sin(r)"