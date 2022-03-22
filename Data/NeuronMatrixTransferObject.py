from Interfaces.TransferObjectInterface import TransferObjectInterface
from Domain.NeuronMatrix import NeuronMatrix
from .DataProcess import DataProcess

class NeuronMatrixTransferObject(TransferObjectInterface):

    def __init__(self, neuronMatrix: NeuronMatrix = None) -> None:
        if neuronMatrix is None:
            return
        self.matrix = neuronMatrix.matrix
        self.matrixWithoutZeros = neuronMatrix.matrixWithoutZeros
        self.vector = neuronMatrix.vector
        self.weightMatrix = neuronMatrix.weightMatrix
        self.fullPattern = neuronMatrix.fullPattern

    # Class functions
    def set_by_dict(dictValue: dict) -> "NeuronMatrixTransferObject":
        result = NeuronMatrixTransferObject()
        result.matrix = dictValue["matrix"]
        result.matrixWithoutZeros = dictValue["matrixWithoutZeros"]
        result.vector = dictValue["vector"]
        result.weightMatrix = dictValue["weightMatrix"]
        result.fullPattern = dictValue["fullPattern"]
        return result

    # Object functions
    def get_as_dict(self) -> dict:
        return {
            "matrix": DataProcess.to_list(self.matrix),
            "matrixWithoutZeros": DataProcess.to_list(self.matrixWithoutZeros),
            "vector": self.vector,
            "weightMatrix": self.weightMatrix,
            "fullPattern": self.fullPattern,
        }