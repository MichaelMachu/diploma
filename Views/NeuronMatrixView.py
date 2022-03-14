from tkinter import *
from tkinter import ttk

from Interfaces.GraphicalUserInterface import GraphicalUserInterface
from . import ApplicationView

from Data.CellularAutomatonTransferObject import CellularAutomatonTransferObject
from Data.DataProcess import DataProcess

class NeuronMatrixView(GraphicalUserInterface):

    def __init__(self, applicationView: ApplicationView, ids: int, n: int, m: int, size: int) -> None:
        super().__init__(Toplevel(applicationView.mainWindow), 500, 304, str(ids + 1) + ". matrix")
        self.applicationView = applicationView

        self.ids = ids
        self.n = n
        self.m = m
        self.size = size

        self.mainWindow.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.__build()

    def __run(self) -> None:
        """Main method for running a view."""
        pass

    def __build(self) -> None:
        self.btn0 = Button(self.mainWindow, bg = "#ade4ff")
        self.btn0["text"] = "Show matrix"
        self.btn0["command"] = lambda matrix = self.applicationView.saved_matrices[self.ids].matrix, typeOfMatrix = "Matrix:": self.print_matrix(matrix, typeOfMatrix)
        self.btn0.grid(row = 0, column = 1)

        self.btn1 = Button(self.mainWindow, bg = "#ade4ff")
        self.btn1["text"] = "Show matrix without zeros"
        self.btn1["command"] = lambda matrix = self.applicationView.saved_matrices[self.ids].matrix_without_zeros, typeOfMatrix = "Matrix without zeros:": self.print_matrix(matrix, typeOfMatrix)
        self.btn1.grid(row = 1, column = 1, padx = 5)

        self.btn2 = Button(self.mainWindow, bg = "#ade4ff")
        self.btn2["text"] = "Show vector"
        self.btn2["command"] = lambda text_length = "Length:", length = len(self.applicationView.saved_matrices[self.ids].vector), vector_text = "Vector:", vector = self.applicationView.saved_matrices[self.ids].vector: print(text_length, length, vector_text, vector)
        self.btn2.grid(row = 2, column = 1)

        self.btn3 = Button(self.mainWindow, bg = "#ade4ff")
        self.btn3["text"] = "Show weighted matrix"
        self.btn3["command"] = lambda matrix = self.applicationView.saved_matrices[self.ids].weightMatrix, typeOfMatrix = "Weighted matrix:": self.print_matrix(matrix, typeOfMatrix)
        self.btn3.grid(row = 3, column = 1, padx = 5)

        self.btn4 = Button(self.mainWindow, bg = "#ade4ff")
        self.btn4["text"] = "Show full pattern"
        self.btn4["command"] = lambda matrix = self.applicationView.saved_matrices[self.ids].fullPattern, typeOfMatrix = "Full pattern matrix:": self.print_matrix(matrix, typeOfMatrix)
        self.btn4.grid(row = 4, column = 1)

        self.btn5 = Button(self.mainWindow, bg = "#ffb7ad")
        self.btn5["text"] = "Forget the pattern"
        self.btn5["command"] = lambda ids = self.ids, window = self.mainWindow: self.applicationView.forget_pattern(ids, window)
        self.btn5.grid(row = 5, column = 1)

        self.canvas = Canvas(self.mainWindow, width = 301, height = 301, bg = "white")
        self.canvas.grid(row = 0, column = 0, rowspan = 6)

        self.draw()

    def draw(self) -> None:
        offset = 2
        for i in range(self.n):
            for j in range(self.m):
                color = "white" if self.applicationView.saved_matrices[self.ids].matrix[i][j] == 0 else "black"
                self.canvas.create_rectangle(offset + j * self.size, offset + i * self.size, offset + (j + 1) * self.size, offset + (i + 1) * self.size, fill = color, outline = "black")

    # Vypsání matice a její délky
    def print_matrix(self, matrix, typeOfMatrix):
        matrix_size = len(matrix)
        print("--------------------------------------------------------")
        print("Size:", str(matrix_size)+"x"+str(matrix_size))
        print(typeOfMatrix)
        if matrix_size > 20:
            self.print_matrix_head_tail(matrix, 10, 10)
        else:
            print(matrix)
        print("--------------------------------------------------------")

    def print_matrix_head_tail(self, matrix, first, last) -> None:
        print("[")
        for i in range(first):
            self.print_part_of_matrix(matrix[i][:first])
        print("\t...\t")
        for i in range(last):
            self.print_part_of_matrix(matrix[-i][:last])
        print("]")

    def print_part_of_matrix(self, matrix) -> None:
        result = "["
        for val in matrix:
            result += str(val) + " "
        result += "... ]"
        print(result)

    def on_closing(self) -> None:
        #self.applicationView.isSaveCaExists = False
        self.mainWindow.destroy()
        self.applicationView.neuronMatrixViews.remove(self)