import copy

from numpy import ndarray

class NeuronMatrix:
    def __init__(self, matrix: ndarray or list = None) -> None:
        if matrix is None:
            return
        self.matrix = matrix
        self.matrixWithoutZeros = self.__remove_zeros_from_matrix(copy.deepcopy(self.matrix))
        self.vector = self.__serialized_matrix(copy.deepcopy(self.matrixWithoutZeros))
        self.weightMatrix = self.__create_weighted_matrix(copy.deepcopy(self.vector))
        self.fullPattern = self.__create_full_pattern(copy.deepcopy(self.weightMatrix))

    # Odstranění nulových hodnot z matice na hodnoty mínus jedna
    def __remove_zeros_from_matrix(self, matrix: ndarray or list) -> ndarray or list:
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == 0:
                    matrix[i][j] = -1

        return matrix

    # Serializování matice do vektoru
    def __serialized_matrix(self, matrix: list) -> list:
        array = []
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                array.append(matrix[i][j])

        return array

    # Výpočet vah podle vzorce X*X^T kde X je vektor z původní matice
    def __create_weighted_matrix(self, serializedMatrix: list) -> list:
        length = len(serializedMatrix)
        return [[serializedMatrix[i] * serializedMatrix[j] for j in range(length)] for i in range(length)]

    # Odečtení jednotkové matice od váhové matice
    def __create_full_pattern(self, weightMatrix: list) -> list:
        for i in range(len(weightMatrix)):
            for j in range(len(weightMatrix[i])):
                if (i == j):
                    weightMatrix[i][j] -= 1     # weightMatrix[i][j] = 0 <=> it should works in the same way

        return weightMatrix