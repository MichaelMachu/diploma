from Domain.Color import Color
from Data.DataProcess import DataProcess

class Settings:

    def __init__(self, cellSize: int = 5, color: Color = Color(((0,0,0),"#000000"))) -> None:
        self.cellSize = cellSize
        self.color = color
        self.pathMain = "TestData"
        self.pathCellularAutomaton = "ca"
        self.pathHopfieldNetwork = "hn"
        self.hopfieldnetworkCellSize = 30

        self.filename = "settings"

        self.load_from_file()

    def save_to_file(self) -> None:
        dataDict = {
            "cellSize": self.cellSize,
            "color": self.color.colorObject,
            "pathMain": self.pathMain,
            "pathCellularAutomaton": self.pathCellularAutomaton,
            "pathHopfieldNetwork": self.pathHopfieldNetwork,
            "hopfieldnetworkCellSize": self.hopfieldnetworkCellSize,
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
        self.hopfieldnetworkCellSize = dataDict["hopfieldnetworkCellSize"]