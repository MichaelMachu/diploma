from typing import Tuple
from Interfaces.TransferObjectInterface import TransferObjectInterface
from .DataProcess import DataProcess

class Chaos01TransferObject(TransferObjectInterface):

    def __init__(self, data: list = None, functionName: str = None, fast: bool = True) -> None:
        if data is None or functionName is None:
            return
        self.data = data
        self.functionName = functionName
        self.fast = fast

    # Class functions
    def set_by_dict(dictValue: dict) -> Tuple[list, str]:
        #[dictValue["data"][i] for i in range(len(dictValue))]
        return dictValue["data"], dictValue["functionName"]

    # Object functions
    def get_as_dict(self) -> dict:
        for i in range(len(self.data)):
            self.data[i]["xx"] = DataProcess.to_list(self.data[i]["xx"])
            self.data[i]["yy"] = DataProcess.to_list(self.data[i]["yy"])
            if self.fast:
                self.data[i].pop("Kc")
                self.data[i].pop("PC")
                self.data[i].pop("QC")
            else:
                self.data[i]["Kc"] = DataProcess.to_list(self.data[i]["Kc"])
                self.data[i]["PC"] = DataProcess.to_list(self.data[i]["PC"])
                self.data[i]["QC"] = DataProcess.to_list(self.data[i]["QC"])
            #dictValue[i] = self.data[i]
        dictValue = {"functionName": self.functionName, "data": self.data}
        return dictValue
        #return {i: self.data[i] for i in range(len(self.data))}