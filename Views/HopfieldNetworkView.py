from tkinter import *
from tkinter import ttk

from Domain.NeuronMatrix import NeuronMatrix
from Domain.HopfieldNetwork import HopfieldNetwork
from Domain.ActivationFunctions import ActivationFunctions

from Data.NeuronMatrixTransferObject import NeuronMatrixTransferObject

from Bases.ViewBase import ViewBase
from . import ApplicationView
from .NeuronMatrixView import NeuronMatrixView
from .ImportView import ImportView

import numpy as np
import copy as copy
import math as math

class HopfieldNetworkView(ViewBase):
    
    def __init__(self, applicationView: ApplicationView) -> None:
        super().__init__(Toplevel(applicationView.mainWindow), 500, 304, "Hopfield Network", applicationView.windowHandler)
        self.applicationView = applicationView
        
        # Singletons objects
        self.importView = None

        self.neuronMatrixViews = []

        self.n = self.m = 10 # 10
        self.max_patterns = int((self.n * self.m) / (2 * math.sqrt(self.n * self.m)))
        self.size = 30 # 30
        self.main_matrix = np.zeros((self.n, self.m))
        self.main_matrix_rectangles = []
        self.saved_matrices = []

        self.__build()

    def __run(self) -> None:
        """Main method for running a view."""
        pass
    
    # Sestavení layoutu včetně tlačítek a canvasu
    def __build(self) -> None:
        # Right menu
        self.frameRight = Frame(self.mainWindow, width=150, height=100, bg="#ababab")
        self.frameRight.grid(column=1, row=0, sticky="nsew")

        self.frameRight.rowconfigure(0, weight=1)
        self.frameRight.rowconfigure(1, weight=1)

        # Buttons
        self.buttonnSave = Button(self.frameRight, bg = "#b9ffad")
        self.buttonnSave["text"] = "Save pattern"
        self.buttonnSave["command"] = self.save_matrix
        #self.buttonnSave.grid(row = 0, column = 0)
        self.buttonnSave.pack(fill='x', pady=(0, 10))

        self.buttonImport = Button(self.frameRight, bg = "#b9ffad")
        self.buttonImport["text"] = "Import pattern"
        self.buttonImport["command"] = self.__show_import_neuron_matrix_menu
        #self.buttonImport.grid(row = 0, column = 0)
        self.buttonImport.pack(fill='x', pady=(0, 10))

        self.buttonRepairSync = Button(self.frameRight, bg = "#fff4ad")
        self.buttonRepairSync["text"] = "Repair pattern Sync"
        self.buttonRepairSync["command"] = self.repair_pattern_sync
        #self.buttonRepairSync.grid(row = 1, column = 0, padx = 5)
        self.buttonRepairSync.pack(fill='x')

        self.buttonRepairAsync = Button(self.frameRight, bg = "#fff4ad")
        self.buttonRepairAsync["text"] = "Repair pattern Async"
        self.buttonRepairAsync["command"] = self.repair_pattern_async
        #self.buttonRepairAsync.grid(row = 2, column = 0, padx = 5)
        self.buttonRepairAsync.pack(fill='x')

        self.buttonShowSavedPatterns = Button(self.frameRight, bg = "#ade4ff")
        self.buttonShowSavedPatterns["text"] = "Show saved patterns"
        self.buttonShowSavedPatterns["command"] = self.show_matrices
        #self.buttonShowSavedPatterns.grid(row = 3, column = 0, padx = 5)
        self.buttonShowSavedPatterns.pack(fill='x', pady=10)

        self.buttonClearGrid = Button(self.frameRight, bg = "#ffb7ad")
        self.buttonClearGrid["text"] = "Clear grid"
        self.buttonClearGrid["command"] = self.clear_grid
        #self.buttonClearGrid.grid(row = 4, column = 0)
        self.buttonClearGrid.pack(fill='x', pady=10)

        self.labelMaxPatterns = Label(self.frameRight, bg=self.mainBG)
        self.labelMaxPatterns["text"] = "Max recommended amount\n of saved patterns is " + str(self.max_patterns)
        #self.labelMaxPatterns.grid(row = 5, column = 0)
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

    # Vytvoření gridu na canvasu
    def create_grid(self) -> None:
        offset = 2
        offsetY = 0
        for i in range(self.n):
            array = []
            offsetX = 0
            for j in range(self.m):
                blockName = "block-" + str(i) + "-" + str(j)
                array.append(self.canvas.create_rectangle(
                    #offset + j * self.size, 
                    #offset + i * self.size, 
                    #offset + (j + 1) * self.size, 
                    #offset + (i + 1) * self.size,
                    offsetX + offset, offsetY + offset,
                    offsetX + self.size + offset, offsetY + self.size + offset,
                    fill = "white", outline = "black", tags = blockName))
                self.canvas.tag_bind(blockName, "<Button-1>", lambda event, i=i, j=j: self.change_value(event, i, j))
                offsetX += self.size
            self.main_matrix_rectangles.append(array)
            offsetY += self.size

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
        algorithms = HopfieldNetwork()
        vector = self.serialized_matrix(self.main_matrix)
        result_vector = algorithms.HopfieldNetworkSync(2, ActivationFunctions.Signum, vector, self.saved_matrices, self.n, self.m)

        #print("result_vector", result_vector)
        for i in range(len(self.main_matrix)):
            for j in range(len(self.main_matrix[i])):
                self.main_matrix[i][j] = result_vector[j + (i * self.n)]
        
        self.refresh_grid()

    # Opravení paternu asynchronním způsobem
    def repair_pattern_async(self) -> None:
        algorithms = HopfieldNetwork()
        vector = self.serialized_matrix(self.main_matrix)
        result_vector = algorithms.HopfieldNetworkAsync(2, ActivationFunctions.Signum, vector, self.saved_matrices, self.n, self.m)

        #print("result_vector", result_vector)
        for i in range(len(self.main_matrix)):
            for j in range(len(self.main_matrix[i])):
                self.main_matrix[i][j] = result_vector[j + (i * self.n)]
        
        self.refresh_grid()

        print("iterations:", algorithms.iter)

    # Obnovení gridu
    def refresh_grid(self) -> None:
        for i in range(self.n):
            for j in range(self.m):
                if self.main_matrix[i][j] == 0:
                    color = "white"
                else:
                    color = "black"
                self.canvas.itemconfig(self.main_matrix_rectangles[i][j], fill = color)

    # Vyčištění gridu
    def clear_grid(self) -> None:
        for i in range(self.n):
            for j in range(self.m):
                self.main_matrix[i][j] = 0
                self.canvas.itemconfig(self.main_matrix_rectangles[i][j], fill = "white")

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

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

    #def import_matrix(self) -> None:
    def __show_import_neuron_matrix_menu(self) -> None:
        if self.windowHandler.exists(self.importView):
            return

        self.importView = ImportView(self, "Neuron Matrix")
        self.windowHandler.register(self.importView)

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

        self.saved_matrices.append(neuronMatrix)

    # Zobrazení všech uložených paternů
    def show_matrices(self) -> None:
        if self.neuronMatrixViews:
            return
        # zde upravit, dělá to chyby, chce to předělat na WindowsHandler anebo to opravit
        for ids in range(len(self.saved_matrices)):
            neuronMatrixView = NeuronMatrixView(self, ids, self.n, self.m, self.size)
            self.neuronMatrixViews.append(neuronMatrixView)