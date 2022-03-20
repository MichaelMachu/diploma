from Domain.Color import Color
from Data.DataProcess import DataProcess

class Settings:

    def __init__(self, cellSize: int = 5, color: Color = Color(((0,0,0),"#000000"))) -> None:
        self.cellSize = cellSize
        self.color = color
        self.pathMain = "TestData"
        self.pathCellularAutomaton = "ca"
        self.pathHopfieldNetwork = "hn"
        self.pathChaos01 = "ch"
        self.hopfieldnetworkCellSize = 30
        self.chaos01ColorDeterminism = Color(((0,255,0),"#00ff00"))
        self.chaos01ColorChaotic = Color(((255,0,0),"#ff0000"))

        self.filename = "settings"

        self.load_from_file()

    def set_default(self) -> None:
        self.cellSize = 5
        self.color = Color(((0,0,0),"#000000"))
        self.pathMain = "TestData"
        self.pathCellularAutomaton = "ca"
        self.pathHopfieldNetwork = "hn"
        self.pathChaos01 = "ch"
        self.hopfieldnetworkCellSize = 30
        self.chaos01ColorDeterminism = Color(((0,255,0),"#00ff00"))
        self.chaos01ColorChaotic = Color(((255,0,0),"#ff0000"))

    def save_to_file(self) -> None:
        dataDict = {
            "cellSize": self.cellSize,
            "color": self.color.colorObject,
            "pathMain": self.pathMain,
            "pathCellularAutomaton": self.pathCellularAutomaton,
            "pathHopfieldNetwork": self.pathHopfieldNetwork,
            "pathChaos01": self.pathChaos01,
            "hopfieldnetworkCellSize": self.hopfieldnetworkCellSize,
            "chaos01ColorDeterminism": self.chaos01ColorDeterminism.colorObject,
            "chaos01ColorChaotic": self.chaos01ColorChaotic.colorObject,
        }

        jsonData = DataProcess.to_json(dataDict)
        DataProcess.save_to_json_file(self.filename, jsonData)

    def load_from_file(self) -> None:
        dataDict = DataProcess.load_from_json_file(self.filename)
        if dataDict is None:
            self.save_to_file()
            return

        self.cellSize = dataDict["cellSize"]
        self.color = Color(tuple(dataDict["color"]))
        self.pathMain = dataDict["pathMain"]
        self.pathCellularAutomaton = dataDict["pathCellularAutomaton"]
        self.pathHopfieldNetwork = dataDict["pathHopfieldNetwork"]
        self.pathChaos01 = dataDict["pathChaos01"]
        self.hopfieldnetworkCellSize = dataDict["hopfieldnetworkCellSize"]
        self.chaos01ColorDeterminism = Color(tuple(dataDict["chaos01ColorDeterminism"]))
        self.chaos01ColorChaotic = Color(tuple(dataDict["chaos01ColorChaotic"]))