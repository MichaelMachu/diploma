from typing import Tuple
from numpy import ndarray
from Interfaces.TransferObjectInterface import TransferObjectInterface
from Domain.Chaos01 import Chaos01

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
            self.data[i]["xx"] = self.__to_list(self.data[i]["xx"])
            self.data[i]["yy"] = self.__to_list(self.data[i]["yy"])
            if self.fast:
                self.data[i].pop("Kc")
                self.data[i].pop("PC")
                self.data[i].pop("QC")
            else:
                self.data[i]["Kc"] = self.__to_list(self.data[i]["Kc"])
                self.data[i]["PC"] = self.__to_list(self.data[i]["PC"])
                self.data[i]["QC"] = self.__to_list(self.data[i]["QC"])
            #dictValue[i] = self.data[i]
        dictValue = {"functionName": self.functionName, "data": self.data}
        return dictValue
        #return {i: self.data[i] for i in range(len(self.data))}

    def __to_list(self, data: ndarray) -> list:
        return data.tolist() if type(data) == ndarray else data