from Domain.CellularAutomaton import CellularAutomaton

class CellularAutomatonTransferObject:

    def __init__(self, cellularAutomaton: CellularAutomaton = None) -> None:
        if cellularAutomaton is None:
            return
        self.size = cellularAutomaton.size
        self.K = cellularAutomaton.K
        self.N = cellularAutomaton.N
        self.λ = cellularAutomaton.λ
        self.quiescentState = cellularAutomaton.quiescentState
        self.possibleStates = cellularAutomaton.possibleStates
        self.ruleNumber = cellularAutomaton.ruleNumber
        self.seedNumber = cellularAutomaton.seedNumber
        self.rule = cellularAutomaton.rule
        self.isQuiscentState = cellularAutomaton.isQuiscentState
        self.cellHistory = cellularAutomaton.cellHistory
        self.currentState = cellularAutomaton.currentState

    # Class functions
    def set_by_dict(dictValue: dict) -> "CellularAutomatonTransferObject":
        result = CellularAutomatonTransferObject()
        result.size = dictValue["size"]
        result.K = dictValue["K"]
        result.N = dictValue["N"]
        result.λ = dictValue["λ"]
        result.quiescentState = dictValue["quiescentState"]
        result.possibleStates = dictValue["possibleStates"]
        result.ruleNumber = dictValue["ruleNumber"]
        result.seedNumber = dictValue["seedNumber"]
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
            "λ": self.λ,
            "quiescentState": self.quiescentState,
            "possibleStates": self.possibleStates,
            "ruleNumber": self.ruleNumber,
            "seedNumber": self.seedNumber,
            "rule": self.rule,
            "isQuiscentState": self.isQuiscentState,
            "cellHistory": self.cellHistory.tolist(),
            "currentState": self.currentState,
        }