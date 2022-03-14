import copy

class NeuronMatrix:
    def __init__(self, matrix: list) -> None:
        self.matrix = matrix
        self.matrixWithoutZeros = self.__remove_zeros_from_matrix(copy.deepcopy(self.matrix))
        self.vector = self.__serialized_matrix(copy.deepcopy(self.matrixWithoutZeros))
        self.weightMatrix = self.__create_weighted_matrix(copy.deepcopy(self.vector))
        self.fullPattern = self.__create_full_pattern(copy.deepcopy(self.weightMatrix))

    # Odstranění nulových hodnot z matice na hodnoty mínus jedna
    def __remove_zeros_from_matrix(self, matrix: list) -> list:
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
        result_array = []
        for i in range(len(serializedMatrix)):
            array = []
            for j in range(len(serializedMatrix)):
                result = serializedMatrix[i] * serializedMatrix[j]
                array.append(result)
            result_array.append(array)

        return result_array

    # Odečtení jednotkové matice od váhové matice
    def __create_full_pattern(self, weightMatrix: list) -> list:
        for i in range(len(weightMatrix)):
            for j in range(len(weightMatrix[i])):
                if (i == j):
                    weightMatrix[i][j] -= 1
                    #weightMatrix[i][j] = 0

        return weightMatrix