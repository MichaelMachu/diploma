import copy

class NeuronMatrix:
    def __init__(self, matrix):
        self.matrix = matrix
        self.matrix_without_zeros = self.remove_zeros_from_matrix(copy.deepcopy(self.matrix))
        self.vector = self.serialized_matrix(copy.deepcopy(self.matrix_without_zeros))
        self.weightMatrix = self.create_weighted_matrix(copy.deepcopy(self.vector))
        self.fullPattern = self.create_full_pattern(copy.deepcopy(self.weightMatrix))

    # Odstranění nulových hodnot z matice na hodnoty mínus jedna
    def remove_zeros_from_matrix(self, matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == 0:
                    matrix[i][j] = -1

        return matrix

    # Serializování matice do vektoru
    def serialized_matrix(self, matrix):
        array = []
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                array.append(matrix[i][j])

        return array

    # Výpočet vah podle vzorce X*X^T kde X je vektor z původní matice
    def create_weighted_matrix(self, serializedMatrix):
        result_array = []
        for i in range(len(serializedMatrix)):
            array = []
            for j in range(len(serializedMatrix)):
                result = serializedMatrix[i] * serializedMatrix[j]
                array.append(result)
            result_array.append(array)

        return result_array

    # Odečtení jednotkové matice od váhové matice
    def create_full_pattern(self, weightMatrix):
        for i in range(len(weightMatrix)):
            for j in range(len(weightMatrix[i])):
                if (i == j):
                    weightMatrix[i][j] -= 1
                    #weightMatrix[i][j] = 0

        return weightMatrix