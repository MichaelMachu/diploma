from Interfaces.FunctionInterface import FunctionInterface

class FunctionBase(FunctionInterface):

    def __init__(self, name: str, lineArray: list) -> None:
        self._name = name
        self._lineArray = lineArray

    def get_name(self) -> None:
        return self._name

    def get_line_array(self) -> None:
        return self._lineArray

    def get(self, r: float, x: float) -> float:
        return 0

    def __str__(self) -> str:
        return ""