from tkinter import *
from tkinter import ttk

from Domain.NeuronMatrix import NeuronMatrix
from Domain.HopfieldNetwork import HopfieldNetwork
from Domain.ActivationFunctions import ActivationFunctions

from Interfaces.GraphicalUserInterface import GraphicalUserInterface
from . import ApplicationView
from .NeuronMatrixView import NeuronMatrixView

import numpy as np
import copy as copy
import math as math

class HopfieldNetworkView(GraphicalUserInterface):
    
    def __init__(self, applicationView: ApplicationView) -> None:
        super().__init__(Toplevel(applicationView.mainWindow), 500, 304, "Hopfield Network")
        self.applicationView = applicationView

        self.neuronMatrixViews = []

        self.mainWindow.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.minWidth = 304
        self.minHeight = 500
        self.maxWidth = 304
        self.maxHeight = 500
        self.mainWindow.minsize(self.minHeight, self.minWidth)
        self.mainWindow.maxsize(self.maxHeight, self.maxWidth)

        self.n = self.m = 25 # 10
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
        self.btn1 = Button(self.mainWindow, bg = "#b9ffad")
        self.btn1["text"] = "Save pattern"
        self.btn1["command"] = self.save_matrix
        self.btn1.grid(row = 0, column = 1)

        self.btn2 = Button(self.mainWindow, bg = "#fff4ad")
        self.btn2["text"] = "Repair pattern Sync"
        self.btn2["command"] = self.repair_pattern_sync
        self.btn2.grid(row = 1, column = 1, padx = 5)

        self.btn3 = Button(self.mainWindow, bg = "#fff4ad")
        self.btn3["text"] = "Repair pattern Async"
        self.btn3["command"] = self.repair_pattern_async
        self.btn3.grid(row = 2, column = 1, padx = 5)

        self.btn4 = Button(self.mainWindow, bg = "#ade4ff")
        self.btn4["text"] = "Show saved patterns"
        self.btn4["command"] = self.show_matrices
        self.btn4.grid(row = 3, column = 1, padx = 5)

        self.btn5 = Button(self.mainWindow, bg = "#ffb7ad")
        self.btn5["text"] = "Clear grid"
        self.btn5["command"] = self.clear_grid
        self.btn5.grid(row = 4, column = 1)

        self.label = Label(self.mainWindow, bg=self.mainBG)
        self.label["text"] = "Max recommended amount\n of saved patterns is " + str(self.max_patterns)
        self.label.grid(row = 5, column = 1)

        self.canvas = Canvas(self.mainWindow, width = 301, height = 301, bg = "white")
        self.canvas.grid(row = 0, column = 0, rowspan = 6)

        self.create_grid()

    # Vytvoření gridu na canvasu
    def create_grid(self):
        offset = 2
        for i in range(self.n):
            array = []
            for j in range(self.m):
                block_name = "block" + str(i) + str(j)
                array.append(self.canvas.create_rectangle(offset + j * self.size, offset + i * self.size, offset + (j + 1) * self.size, offset + (i + 1) * self.size, fill = "white", outline = "black", tags = block_name))
                self.canvas.tag_bind(block_name, "<Button-1>", lambda event, i=i, j=j: self.change_value(i, j))
            self.main_matrix_rectangles.append(array)

    def draw(self) -> None:
        """Drawing method used for canvas"""
        pass

    # Event změny hodnoty na canvasu a matici
    def change_value(self, i, j):
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
    def repair_pattern_sync(self):
        algorithms = HopfieldNetwork()
        activationFunctions = ActivationFunctions()
        vector = self.serialized_matrix(self.main_matrix)
        result_vector = algorithms.HopfieldNetworkSync(2, activationFunctions.Signum, vector, self.saved_matrices, self.n, self.m)

        #print("result_vector", result_vector)
        for i in range(len(self.main_matrix)):
            for j in range(len(self.main_matrix[i])):
                self.main_matrix[i][j] = result_vector[j + (i * self.n)]
        
        self.refresh_grid()

    # Opravení paternu asynchronním způsobem
    def repair_pattern_async(self):
        algorithms = HopfieldNetwork()
        activationFunctions = ActivationFunctions()
        vector = self.serialized_matrix(self.main_matrix)
        result_vector = algorithms.HopfieldNetworkAsync(2, activationFunctions.Signum, vector, self.saved_matrices, self.n, self.m)

        #print("result_vector", result_vector)
        for i in range(len(self.main_matrix)):
            for j in range(len(self.main_matrix[i])):
                self.main_matrix[i][j] = result_vector[j + (i * self.n)]
        
        self.refresh_grid()

        print("iterations:", algorithms.iter)

    # Obnovení gridu
    def refresh_grid(self):
        for i in range(self.n):
            for j in range(self.m):
                if self.main_matrix[i][j] == 0:
                    color = "white"
                else:
                    color = "black"
                self.canvas.itemconfig(self.main_matrix_rectangles[i][j], fill = color)

    # Vyčištění gridu
    def clear_grid(self):
        for i in range(self.n):
            for j in range(self.m):
                self.main_matrix[i][j] = 0
                self.canvas.itemconfig(self.main_matrix_rectangles[i][j], fill = "white")

    # Serializování matice do vektoru
    def serialized_matrix(self, matrix):
        array = []
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                array.append(matrix[i][j])

        return array

    # Uložení matice skrze objekt NeuronMatrix do seznamu matic
    def save_matrix(self):
        specificMatrix = NeuronMatrix(copy.deepcopy(self.main_matrix))
        self.saved_matrices.append(specificMatrix)

    # Zobrazení všech uložených paternů
    def show_matrices(self):
        if self.neuronMatrixViews:
            return

        for ids in range(len(self.saved_matrices)):
            neuronMatrixView = NeuronMatrixView(self, ids, self.n, self.m, self.size)
            self.neuronMatrixViews.append(neuronMatrixView)

    # Odstranění paternu z uložených paternů
    def forget_pattern(self, ids, window):
        self.saved_matrices.pop(ids)
        window.destroy()

    def on_closing(self) -> None:
        self.applicationView.isHopfieldNetworkExists = False
        self.mainWindow.destroy()