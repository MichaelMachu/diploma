# Interval pro funkce
class Interval:

    def __init__(self, lowerBound: float, upperBound: float, step: float = 1) -> None:
        self.lowerBound = lowerBound
        self.upperBound = upperBound
        self.step = step