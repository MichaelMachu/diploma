
from Domain.Color import Color

class Settings:

    def __init__(self, cellSize: int = 5, color: Color = Color(((0,0,0),"#000000"))) -> None:
        self.cellSize = cellSize
        self.color = color
        self.pathMain = "TestData"
        self.pathCellularAutomaton = "ca"
        self.pathHopfieldNetwork = "hn"
        self.hopfieldnetworkCellSize = 30

    def save_to_file(self) -> None:
        pass

    def load_from_file(self) -> None:
        pass