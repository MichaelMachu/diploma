from typing import Tuple
from Interfaces.TransferObjectInterface import TransferObjectInterface
from Domain.Chaos01 import Chaos01

class Chaos01TransferObject(TransferObjectInterface):

    def __init__(self, data: list = None, functionName: str = None) -> None:
        if data is None or functionName is None:
            return
        self.data = data
        self.functionName = functionName

    # Class functions
    def set_by_dict(dictValue: dict) -> Tuple[list, str]:
        #[dictValue["data"][i] for i in range(len(dictValue))]
        return dictValue["data"], dictValue["functionName"]

    # Object functions
    def get_as_dict(self) -> dict:
        for i in range(len(self.data)):
            self.data[i]["xx"] = self.data[i]["xx"].tolist()
            self.data[i]["yy"] = self.data[i]["yy"].tolist()
            #dictValue[i] = self.data[i]
        dictValue = {"functionName": self.functionName, "data": self.data}
        return dictValue
        #return {i: self.data[i] for i in range(len(self.data))}