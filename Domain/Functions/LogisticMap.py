from Interfaces.FunctionInterface import FunctionInterface

class LogisticMap(FunctionInterface):

    def get(self, r: float, x: float) -> float:
        return r * x * (1 - x)

    def __str__(self) -> str:
        return "r * x * (1 - x)"