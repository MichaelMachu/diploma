from Interfaces.FunctionInterface import FunctionInterface

class FunctionBase(FunctionInterface):

    def __init__(self, name: str, lineArray: list) -> None:
        _name = name
        _lineArray = lineArray

    def get_name(self) -> None:
        return _name

    def get_line_array(self) -> None:
        return _lineArray

    def get(self, r: float, x: float) -> float:
        return 0

    def __str__(self) -> str:
        return ""