
from Domain.Color import Color

class AnimationSettings:

    def __init__(self, cellSize: int = 5, color: Color = Color(((0,0,0),"#000000"))) -> None:
        self.cellSize = cellSize
        self.color = color

    def save_to_file(self) -> None:
        pass

    def load_from_file(self) -> None:
        pass