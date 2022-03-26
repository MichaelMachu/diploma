from typing import Tuple
from copy import deepcopy

from Interfaces.TransferObjectInterface import TransferObjectInterface
from .DataProcess import DataProcess
from EnumTypes.GraphType import GraphType

class Chaos01TransferObject(TransferObjectInterface):

    def __init__(self, data: list = None, functionName: str = None, dataType: GraphType = None, fast: bool = True) -> None:
        if data is None or functionName is None or dataType is None:
            return
        self.data = data
        self.functionName = functionName
        self.dataType = dataType
        self.fast = fast

    # Class functions
    def set_by_dict(dictValue: dict) -> Tuple[list, str, GraphType]:
        #[dictValue["data"][i] for i in range(len(dictValue))]
        return dictValue["data"], dictValue["functionName"], GraphType(dictValue["dataType"])

    # Object functions
    def get_as_dict(self) -> dict:
        data = deepcopy(self.data)
        for i in range(len(data)):
            if self.dataType == GraphType.BIFURCATION:      # xx and yy data exists only for BIFURCATION type, ITERATION has segments
                data[i]["xx"] = DataProcess.to_list(data[i]["xx"])
                data[i]["yy"] = DataProcess.to_list(data[i]["yy"])
            if self.fast:
                data[i].pop("Kc")
                data[i].pop("PC")
                data[i].pop("QC")
            else:
                data[i]["Kc"] = DataProcess.to_list(data[i]["Kc"])
                data[i]["PC"] = DataProcess.to_list(data[i]["PC"])
                data[i]["QC"] = DataProcess.to_list(data[i]["QC"])
            #dictValue[i] = self.data[i]
        dictValue = {"functionName": self.functionName, "dataType": self.dataType.value, "data": data}
        return dictValue
        #return {i: self.data[i] for i in range(len(self.data))}