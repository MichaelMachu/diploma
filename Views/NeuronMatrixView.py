from tkinter import *
from tkinter import ttk

from Interfaces.GraphicalUserInterface import GraphicalUserInterface
from . import ApplicationView

from Domain.Print import Print

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
        # Right menu
        self.frameRight = Frame(self.mainWindow, width=150, height=100, bg="#ababab")
        self.frameRight.grid(column=1, row=0, sticky="nsew")

        self.frameRight.rowconfigure(0, weight=1)
        self.frameRight.rowconfigure(1, weight=1)

        self.btn0 = Button(self.frameRight, bg = "#ade4ff")
        self.btn0["text"] = "Show matrix"
        self.btn0["command"] = lambda matrix = self.applicationView.saved_matrices[self.ids].matrix, typeOfMatrix = "Matrix:": Print.print_matrix_2d(matrix, typeOfMatrix)
        #self.btn0.grid(row = 0, column = 1)
        self.btn0.pack(fill='x')

        self.btn1 = Button(self.frameRight, bg = "#ade4ff")
        self.btn1["text"] = "Show matrix without zeros"
        self.btn1["command"] = lambda matrix = self.applicationView.saved_matrices[self.ids].matrixWithoutZeros, typeOfMatrix = "Matrix without zeros:": Print.print_matrix_2d(matrix, typeOfMatrix)
        #self.btn1.grid(row = 1, column = 1, padx = 5)
        self.btn1.pack(fill='x')

        self.btn2 = Button(self.frameRight, bg = "#ade4ff")
        self.btn2["text"] = "Show vector"
        self.btn2["command"] = lambda vector = self.applicationView.saved_matrices[self.ids].vector: Print.print_vector(vector)
        #self.btn2.grid(row = 2, column = 1)
        self.btn2.pack(fill='x')

        self.btn3 = Button(self.frameRight, bg = "#ade4ff")
        self.btn3["text"] = "Show weighted matrix"
        self.btn3["command"] = lambda matrix = self.applicationView.saved_matrices[self.ids].weightMatrix, typeOfMatrix = "Weighted matrix:": Print.print_matrix_2d(matrix, typeOfMatrix)
        #self.btn3.grid(row = 3, column = 1, padx = 5)
        self.btn3.pack(fill='x')

        self.btn4 = Button(self.frameRight, bg = "#ade4ff")
        self.btn4["text"] = "Show full pattern"
        self.btn4["command"] = lambda matrix = self.applicationView.saved_matrices[self.ids].fullPattern, typeOfMatrix = "Full pattern matrix:": Print.print_matrix_2d(matrix, typeOfMatrix)
        #self.btn4.grid(row = 4, column = 1)
        self.btn4.pack(fill='x')

        self.btn5 = Button(self.frameRight, bg = "#ffb7ad")
        self.btn5["text"] = "Forget the pattern"
        self.btn5["command"] = lambda ids = self.ids, window = self.mainWindow: self.applicationView.forget_pattern(ids, window)
        #self.btn5.grid(row = 5, column = 1)
        self.btn5.pack(fill='x', pady=(20, 0))

        # Canvas
        self.frameCanvas = Frame(self.mainWindow, bg="#ababab")
        self.frameCanvas.grid(column=0, row=0, sticky="nsew")
        self.frameCanvas.grid_rowconfigure(0, weight=1)
        self.frameCanvas.grid_columnconfigure(0, weight=1)

        self.canvas = Canvas(self.frameCanvas, width = 301, height = 301, bg = "#fff")
        self.canvas.grid(row = 0, column = 0, sticky="nsew")

        # Link a scrollbar to the canvas
        self.scrollbarVerticalCanvas = Scrollbar(self.frameCanvas, orient="vertical", command=self.canvas.yview)
        self.scrollbarVerticalCanvas.grid(row=0, column=1, sticky='ns')
        self.canvas.configure(yscrollcommand=self.scrollbarVerticalCanvas.set)

        self.scrollbarHorizontalCanvas = Scrollbar(self.frameCanvas, orient="horizontal", command=self.canvas.xview)
        self.scrollbarHorizontalCanvas.grid(row=1, column=0, sticky='ew')
        self.canvas.configure(xscrollcommand=self.scrollbarHorizontalCanvas.set)

        self.mainWindow.grid_rowconfigure(0, weight=1)
        self.mainWindow.grid_columnconfigure(0, weight=1)

        self.draw()

    def draw(self) -> None:
        offset = 2
        for i in range(self.n):
            for j in range(self.m):
                color = "white" if self.applicationView.saved_matrices[self.ids].matrix[i][j] == 0 else "black"
                self.canvas.create_rectangle(offset + j * self.size, offset + i * self.size, offset + (j + 1) * self.size, offset + (i + 1) * self.size, fill = color, outline = "black")

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_closing(self) -> None:
        self.mainWindow.destroy()
        self.applicationView.neuronMatrixViews.remove(self)