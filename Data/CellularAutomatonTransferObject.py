from Interfaces.TransferObjectInterface import TransferObjectInterface
from Domain.CellularAutomaton import CellularAutomaton

class CellularAutomatonTransferObject(TransferObjectInterface):

    def __init__(self, cellularAutomaton: CellularAutomaton = None) -> None:
        if cellularAutomaton is None:
            return
        self.size = cellularAutomaton.size
        self.K = cellularAutomaton.K
        self.N = cellularAutomaton.N
        self.lambdaValue = cellularAutomaton.lambdaValue
        self.quiescentState = cellularAutomaton.quiescentState
        self.possibleStates = cellularAutomaton.possibleStates
        self.ruleNumber = cellularAutomaton.ruleNumber
        self.seedNumber = cellularAutomaton.seedNumber
        self.pattern2D = cellularAutomaton.pattern2D
        self.rule = cellularAutomaton.rule
        self.isQuiscentState = cellularAutomaton.isQuiscentState
        self.cellHistory = cellularAutomaton.cellHistory
        self.currentState = cellularAutomaton.currentState

    # Class functions
    def set_by_dict(dictValue: dict) -> "CellularAutomatonTransferObject":
        result = CellularAutomatonTransferObject()
        result.size = tuple(dictValue["size"]) if type(dictValue["size"]) is list else dictValue["size"]
        result.K = dictValue["K"]
        result.N = dictValue["N"]
        result.lambdaValue = dictValue["lambdaValue"]
        result.quiescentState = dictValue["quiescentState"]
        result.possibleStates = dictValue["possibleStates"]
        result.ruleNumber = dictValue["ruleNumber"]
        result.seedNumber = dictValue["seedNumber"]
        result.pattern2D = dictValue["pattern2D"]
        result.rule = dictValue["rule"]
        result.isQuiscentState = dictValue["isQuiscentState"]
        result.cellHistory = dictValue["cellHistory"]
        result.currentState = dictValue["currentState"]
        return result

    # Object functions
    def get_as_dict(self) -> dict:
        return {
            "size": self.size,
            "K": self.K,
            "N": self.N,
            "lambdaValue": self.lambdaValue,
            "quiescentState": self.quiescentState,
            "possibleStates": self.possibleStates,
            "ruleNumber": self.ruleNumber,
            "pattern2D": self.pattern2D,
            "seedNumber": self.seedNumber,
            "rule": self.rule.tolist(),
            "isQuiscentState": self.isQuiscentState,
            "cellHistory": self.cellHistory.tolist(),
            "currentState": self.currentState.tolist(),
        }