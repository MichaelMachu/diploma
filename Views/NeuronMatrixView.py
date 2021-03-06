from tkinter import *
from tkinter import ttk
from copy import deepcopy

from Bases.ViewBase import ViewBase
from . import ApplicationView
from .ExportView import ExportView

from Domain.Print import Print
from Data.NeuronMatrixTransferObject import NeuronMatrixTransferObject

class NeuronMatrixView(ViewBase):

    def __init__(self, applicationView: ApplicationView, hopfieldNetworkView: ViewBase, ids: int, n: int, m: int, size: int) -> None:
        super().__init__(Toplevel(hopfieldNetworkView.mainWindow), 500, 304, str(ids + 1) + ". matrix pattern", applicationView.windowHandler)
        self.applicationView = applicationView
        self.hopfieldNetworkView = hopfieldNetworkView

        # Singletons objects
        self.exportNeuronMatrixView = None
        self.exportView = None

        # Control parameters
        self.isExportNeuronMatrixExists = False

        self.ids = ids
        self.n = n
        self.m = m
        self.size = size

        self.neuronMatrix = self.hopfieldNetworkView.saved_matrices[self.ids]

        self.__build()

    def __run(self) -> None:
        """Main method for running a view."""
        pass

    def __build(self) -> None:
        # Top menu
        self.menu = Menu(self.mainWindow)
        self.mainWindow.config(menu=self.menu)

        self.menuFile = Menu(self.menu, tearoff=False)
        self.menuFile.add_command(
            label="Export pattern",
            command=self.__show_export_neuron_matrix_menu
        )
        
        self.menu.add_cascade(label="File", menu=self.menuFile)

        # Right menu
        self.frameRight = Frame(self.mainWindow, width=150, height=100, bg="#ababab")
        self.frameRight.grid(column=1, row=0, sticky="nsew")

        self.frameRight.rowconfigure(0, weight=1)
        self.frameRight.rowconfigure(1, weight=1)

        # Buttons
        self.buttonPrint = Button(self.frameRight, bg = "#b9ffad")
        self.buttonPrint["text"] = "Print on network"
        self.buttonPrint["command"] = self.print_on_network
        self.buttonPrint.pack(fill='x', pady=(0, 20))

        self.buttonMatrix = Button(self.frameRight, bg = "#ade4ff")
        self.buttonMatrix["text"] = "Show matrix"
        self.buttonMatrix["command"] = lambda matrix = self.neuronMatrix.matrix, typeOfMatrix = "Matrix:": Print.print_matrix_2d(matrix, typeOfMatrix)
        self.buttonMatrix.pack(fill='x')

        self.buttonMatrixWithoutZeros = Button(self.frameRight, bg = "#ade4ff")
        self.buttonMatrixWithoutZeros["text"] = "Show matrix without zeros"
        self.buttonMatrixWithoutZeros["command"] = lambda matrix = self.neuronMatrix.matrixWithoutZeros, typeOfMatrix = "Matrix without zeros:": Print.print_matrix_2d(matrix, typeOfMatrix)
        self.buttonMatrixWithoutZeros.pack(fill='x')

        self.buttonVector = Button(self.frameRight, bg = "#ade4ff")
        self.buttonVector["text"] = "Show vector"
        self.buttonVector["command"] = lambda vector = self.neuronMatrix.vector: Print.print_vector(vector)
        self.buttonVector.pack(fill='x')

        self.buttonWeightedMatrix = Button(self.frameRight, bg = "#ade4ff")
        self.buttonWeightedMatrix["text"] = "Show weighted matrix"
        self.buttonWeightedMatrix["command"] = lambda matrix = self.neuronMatrix.weightMatrix, typeOfMatrix = "Weighted matrix:": Print.print_matrix_2d(matrix, typeOfMatrix)
        self.buttonWeightedMatrix.pack(fill='x')

        self.buttonFullPattern = Button(self.frameRight, bg = "#ade4ff")
        self.buttonFullPattern["text"] = "Show full pattern"
        self.buttonFullPattern["command"] = lambda matrix = self.neuronMatrix.fullPattern, typeOfMatrix = "Full pattern matrix:": Print.print_matrix_2d(matrix, typeOfMatrix)
        self.buttonFullPattern.pack(fill='x')

        self.buttonForgetPattern = Button(self.frameRight, bg = "#ffb7ad")
        self.buttonForgetPattern["text"] = "Forget the pattern"
        self.buttonForgetPattern["command"] = self.forget_pattern
        self.buttonForgetPattern.pack(fill='x', pady=(20, 0))

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
                color = "white" if self.neuronMatrix.matrix[i][j] == 0 else "black"
                self.canvas.create_rectangle(offset + j * self.size, offset + i * self.size, offset + (j + 1) * self.size, offset + (i + 1) * self.size, fill = color, outline = "black")

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def __show_export_neuron_matrix_menu(self) -> None:
        if self.windowHandler.exists(self.exportView):
            return

        path = self.applicationView.settings.pathMain + "/" + self.applicationView.settings.pathHopfieldNetwork + "/"
        self.exportView = ExportView(self, NeuronMatrixTransferObject(self.neuronMatrix), path, "Neuron Matrix")
        self.windowHandler.register(self.exportView)

    def print_on_network(self) -> None:
        self.hopfieldNetworkView.main_matrix = deepcopy(self.neuronMatrix.matrix)
        self.hopfieldNetworkView.refresh_grid()

    # Odstran??n?? paternu z ulo??en??ch patern??
    def forget_pattern(self) -> None:
        self.hopfieldNetworkView.saved_matrices.remove(self.neuronMatrix)
        self.on_closing()

    def on_closing(self) -> None:
        self.mainWindow.destroy()
        self.hopfieldNetworkView.neuronMatrixViews.remove(self)