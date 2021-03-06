from tkinter import *
from tkinter import ttk

from Domain.NeuronMatrix import NeuronMatrix
from Domain.HopfieldNetwork import HopfieldNetwork
from Domain.ActivationFunctions import ActivationFunctions

from Data.NeuronMatrixTransferObject import NeuronMatrixTransferObject
from Data.HopfieldNetworkHistoryTransferObject import HopfieldNetworkHistoryTransferObject

from Bases.ViewBase import ViewBase
from . import ApplicationView
from .NeuronMatrixView import NeuronMatrixView
from .ImportView import ImportView
from .ExportView import ExportView
from .NewHopfieldNetworkView import NewHopfieldNetworkView

import numpy as np
import copy as copy
import math as math

class HopfieldNetworkView(ViewBase):
    
    def __init__(self, applicationView: ApplicationView) -> None:
        super().__init__(Toplevel(applicationView.mainWindow), 600, 500, "Hopfield Network", applicationView.windowHandler)
        self.applicationView = applicationView
        
        # Singletons objects
        self.importView = None
        self.newView = None

        self.neuronMatrixViews = []

        self.networkSize = (10, 10)
        self.hopfieldNetwork = HopfieldNetwork(self.networkSize)

        #self.n = self.m = 10 # 10
        self.max_patterns = self.hopfieldNetwork.get_max_patterns()     # self.get_max_patterns()
        self.cellSize = self.applicationView.settings.hopfieldnetworkCellSize # 30
        self.main_matrix = np.zeros(self.networkSize) # (self.n, self.m)
        self.main_matrix_rectangles = []
        self.saved_matrices = []

        self.__build()

    def __run(self) -> None:
        """Main method for running a view."""
        pass
    
    # Sestavení layoutu včetně tlačítek a canvasu
    def __build(self) -> None:
        # Top menu
        self.menu = Menu(self.mainWindow)
        self.mainWindow.config(menu=self.menu)

        self.menuFile = Menu(self.menu, tearoff=False)
        self.menuFile.add_command(
            label="New",
            command=self.__show_new_menu
        )
        self.menuFile.add_command(
            label="Import pattern",
            command=self.__show_import_neuron_matrix_menu
        )
        #self.menuFile.add_command(
        #    label="Import image as pattern",
            #command=  # TODO => Could be a new feature (just make a conversion of pixels into black/white points)
        #)
        self.menuFile.add_command(
            label="Export history of repairing",
            command=self.__show_export_menu
        )

        self.menu.add_cascade(label="File", menu=self.menuFile)

        # Right menu
        self.frameRight = Frame(self.mainWindow, width=150, height=100, bg="#ababab")
        self.frameRight.grid(column=1, row=0, sticky="nsew")

        self.frameRight.rowconfigure(0, weight=1)
        self.frameRight.rowconfigure(1, weight=1)

        # Buttons
        self.buttonnSave = Button(self.frameRight, bg = "#b9ffad")
        self.buttonnSave["text"] = "Save pattern"
        self.buttonnSave["command"] = self.save_matrix
        self.buttonnSave.pack(fill='x', pady=(0, 20))

        self.buttonnSave = Button(self.frameRight, bg = "#b9ffad")
        self.buttonnSave["text"] = "Add 50 % noise"
        self.buttonnSave["command"] = self.__add_noise
        self.buttonnSave.pack(fill='x', pady=(0, 20))

        self.buttonRepairSync = Button(self.frameRight, bg = "#fff4ad")
        self.buttonRepairSync["text"] = "Repair pattern Sync"
        self.buttonRepairSync["command"] = self.repair_pattern_sync
        self.buttonRepairSync.pack(fill='x')

        self.buttonRepairAsync = Button(self.frameRight, bg = "#fff4ad")
        self.buttonRepairAsync["text"] = "Repair pattern Async"
        self.buttonRepairAsync["command"] = self.repair_pattern_async
        self.buttonRepairAsync.pack(fill='x')

        self.buttonShowSavedPatterns = Button(self.frameRight, bg = "#ade4ff")
        self.buttonShowSavedPatterns["text"] = "Show saved patterns"
        self.buttonShowSavedPatterns["command"] = self.show_matrices
        self.buttonShowSavedPatterns.pack(fill='x', pady=(20, 10))

        self.buttonClearGrid = Button(self.frameRight, bg = "#ffb7ad")
        self.buttonClearGrid["text"] = "Clear grid"
        self.buttonClearGrid["command"] = self.clear_grid
        self.buttonClearGrid.pack(fill='x', pady=10)

        self.labelMaxPatterns = Label(self.frameRight, bg=self.mainBG)
        self.labelMaxPatterns["text"] = "Max recommended amount\n of saved patterns is " + str(self.max_patterns)
        self.labelMaxPatterns.pack(fill='x', pady=10)

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

        self.create_grid()

    # Returns max patterns
    #def get_max_patterns(self) -> int:
    #    return int((self.n * self.m) / (2 * math.sqrt(self.n * self.m)))

    # Vytvoření gridu na canvasu
    def create_grid(self) -> None:
        offset = 2
        offsetY = 0
        for i in range(self.networkSize[0]):
            array = []
            offsetX = 0
            for j in range(self.networkSize[1]):
                blockName = "block-" + str(i) + "-" + str(j)
                array.append(self.canvas.create_rectangle(
                    #offset + j * self.cellSize, 
                    #offset + i * self.cellSize, 
                    #offset + (j + 1) * self.cellSize, 
                    #offset + (i + 1) * self.cellSize,
                    offsetX + offset, offsetY + offset,
                    offsetX + self.cellSize + offset, offsetY + self.cellSize + offset,
                    fill = "white", outline = "black", tags = blockName))
                self.canvas.tag_bind(blockName, "<Button-1>", lambda event, i=i, j=j: self.change_value(event, i, j))
                offsetX += self.cellSize
            self.main_matrix_rectangles.append(array)
            offsetY += self.cellSize

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def draw(self) -> None:
        """Drawing method used for canvas"""
        pass

    # Event změny hodnoty na canvasu a matici
    def change_value(self, event: EventType, i: int, j: int) -> None:
        if self.main_matrix[i][j] == 0:
            self.main_matrix[i][j] = 1
            color = "black"
            #outColor = "white"
        else:
            self.main_matrix[i][j] = 0
            color = "white"
            #outColor = "black"
        self.canvas.itemconfig(self.main_matrix_rectangles[i][j], fill = color)
        #self.canvas.itemconfig(self.main_matrix_rectangles[i][j], fill = color, outline = outColor)

    # Opravení paternu synchronním způsobem
    def repair_pattern_sync(self) -> None:
        vector = self.serialized_matrix(self.main_matrix)
        result_vector = self.hopfieldNetwork.HopfieldNetworkSync(2, ActivationFunctions.Signum, vector, self.saved_matrices)

        #print("result_vector", result_vector)
        for i in range(len(self.main_matrix)):
            for j in range(len(self.main_matrix[i])):
                self.main_matrix[i][j] = result_vector[j + (i * self.networkSize[0])]
        
        self.refresh_grid()

    # Opravení paternu asynchronním způsobem
    def repair_pattern_async(self) -> None:
        vector = self.serialized_matrix(self.main_matrix)
        result_vector = self.hopfieldNetwork.HopfieldNetworkAsync(2, ActivationFunctions.Signum, vector, self.saved_matrices)

        #print("result_vector", result_vector)
        for i in range(len(self.main_matrix)):
            for j in range(len(self.main_matrix[i])):
                self.main_matrix[i][j] = result_vector[j + (i * self.networkSize[0])]
        
        self.refresh_grid()

        print("iterations:", self.hopfieldNetwork.iter)

    # Obnovení gridu
    def refresh_grid(self) -> None:
        for i in range(self.networkSize[0]):
            for j in range(self.networkSize[1]):
                if self.main_matrix[i][j] == 0:
                    color = "white"
                else:
                    color = "black"
                self.canvas.itemconfig(self.main_matrix_rectangles[i][j], fill = color)

    # Vyčištění gridu
    def clear_grid(self) -> None:
        for i in range(self.networkSize[0]):
            for j in range(self.networkSize[1]):
                self.main_matrix[i][j] = 0
                self.canvas.itemconfig(self.main_matrix_rectangles[i][j], fill = "white")

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def __add_noise(self) -> None:
        noise = [[np.random.rand() < 0.5 for _ in range(self.networkSize[1])] for _ in range(self.networkSize[0])]
        self.main_matrix = [[int(bool(self.main_matrix[i][j]) != bool(noise[i][j])) for j in range(self.networkSize[1])] for i in range(self.networkSize[0])]
        self.refresh_grid()

    # Serializování matice do vektoru
    def serialized_matrix(self, matrix: list) -> list:
        array = []
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                array.append(matrix[i][j])

        return array

    # Uložení matice skrze objekt NeuronMatrix do seznamu matic
    def save_matrix(self) -> None:
        neuronMatrix = NeuronMatrix(copy.deepcopy(self.main_matrix))
        self.saved_matrices.append(neuronMatrix)

    def __show_import_neuron_matrix_menu(self) -> None:
        if self.windowHandler.exists(self.importView):
            return

        path = self.applicationView.settings.pathMain + "/" + self.applicationView.settings.pathHopfieldNetwork + "/"
        self.importView = ImportView(self, path, "Neuron Matrix")
        self.windowHandler.register(self.importView)

    def __show_export_menu(self) -> None:
        if self.windowHandler.exists(self.exportView):
            return

        transferObject = HopfieldNetworkHistoryTransferObject(self.hopfieldNetwork.history)

        path = self.applicationView.settings.pathMain + "/" + self.applicationView.settings.pathHopfieldNetwork + "/"
        self.exportView = ExportView(self, transferObject, path, "history data of repairing")
        self.windowHandler.register(self.exportView)

    def __show_new_menu(self) -> None:
        if self.windowHandler.exists(self.newView):
            return

        self.newView = NewHopfieldNetworkView(self)
        self.windowHandler.register(self.newView)

    def set_import_data(self, data: dict) -> None:
        super().set_import_data(data)

        if self._importData is None:
            return

        transferObject = NeuronMatrixTransferObject.set_by_dict(self._importData)

        neuronMatrix = NeuronMatrix()
        neuronMatrix.matrix = transferObject.matrix
        neuronMatrix.matrixWithoutZeros = transferObject.matrixWithoutZeros
        neuronMatrix.vector = transferObject.vector
        neuronMatrix.weightMatrix = transferObject.weightMatrix
        neuronMatrix.fullPattern = transferObject.fullPattern

        if len(neuronMatrix.matrix) != self.networkSize[0] or len(neuronMatrix.matrix[0]) != self.networkSize[1]:
            print("Error: size of imported pattern is not same as the size of hopfield field")
            return

        self.saved_matrices.append(neuronMatrix)

    # Zobrazení všech uložených paternů
    def show_matrices(self) -> None:
        if self.neuronMatrixViews:
            return
        
        for ids in range(len(self.saved_matrices)):
            neuronMatrixView = NeuronMatrixView(self.applicationView, self, ids, self.networkSize[0], self.networkSize[1], self.cellSize)
            self.neuronMatrixViews.append(neuronMatrixView)

    def on_closing(self) -> None:
        super().on_closing()
        self.applicationView.hopfieldNetworkView = None