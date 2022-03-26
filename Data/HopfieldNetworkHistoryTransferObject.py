from Interfaces.TransferObjectInterface import TransferObjectInterface
from .DataProcess import DataProcess

class HopfieldNetworkHistoryTransferObject(TransferObjectInterface):

    def __init__(self, history: list = None) -> None:
        if history is None:
            return
        self.history = history

    # Class functions
    def set_by_dict(dictValue: dict) -> list:
        return dictValue["history"]

    # Object functions
    def get_as_dict(self) -> dict:
        self.history = DataProcess.to_list(self.history)
        return {"history": self.history}