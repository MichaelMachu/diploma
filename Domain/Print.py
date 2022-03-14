
class Print:
    
    def print_matrix_2d(matrix: list, typeOfMatrix: str, maxSizeToShow: int = 20) -> None:
        """Prints matrix and its size"""
        matrixSize = len(matrix)
        print("--------------------------------------------------------")
        print("Size:", str(matrixSize)+"x"+str(matrixSize))
        print(typeOfMatrix)
        if matrixSize > maxSizeToShow:
            Print.print_matrix_2d_head_tail(matrix, 10, 10)
        else:
            print(matrix)
        print("--------------------------------------------------------")

    def print_matrix_2d_head_tail(matrix: list, first: int, last: int) -> None:
        print("[")
        for i in range(first):
            Print.print_part_of_matrix(matrix[i][:first])
        print("\t...\t")
        for i in range(last):
            Print.print_part_of_matrix(matrix[-i][:last])
        print("]")

    def print_matrix_2d_head(matrix: list, size: int) -> None:
        print("[")
        for i in range(size):
            Print.print_part_of_matrix(matrix[i][:size])
        print("\t...\t")
        print("]")

    def print_matrix_2d_tail(matrix: list, size: int) -> None:
        print("[")
        for i in range(size):
            Print.print_part_of_matrix(matrix[-i][:size])
        print("\t...\t")
        print("]")

    def print_part_of_matrix(matrix: list) -> None:
        result = "["
        for val in matrix:
            result += str(val) + " "
        result += "... ]"
        print(result)

    def print_vector(vector: list, maxSizeToShow: int = 40) -> None:
        vectorSize = len(vector)
        print("--------------------------------------------------------")
        print("Size:", str(vectorSize))
        if vectorSize > maxSizeToShow:
            print("[")
            Print.print_vector_values(vector[:20])
            print("\t...\t")
            Print.print_vector_values(vector[-20:])
            print("]")
        else:
            print(vector)
        print("--------------------------------------------------------")

    def print_vector_values(vector: list) -> None:
        result = ""
        for val in vector:
            result += str(val) + " "
        print(result)