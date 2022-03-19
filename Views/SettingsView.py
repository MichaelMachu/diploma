from tkinter import *
from tkinter.colorchooser import askcolor
from Domain.Color import Color

from Bases.ViewBase import ViewBase
from . import ApplicationView

class SettingsView(ViewBase):

    def __init__(self, applicationView: ApplicationView) -> None:
        super().__init__(Toplevel(applicationView.mainWindow), 400, 550, "Settings", applicationView.windowHandler)
        self.applicationView = applicationView
        self.mainWindow.attributes("-topmost", True)

        self.colorCode = self.applicationView.settings.color.colorObject
        self.colorCodeDeterminism = self.applicationView.settings.chaos01ColorDeterminism.colorObject
        self.colorCodeChaotic = self.applicationView.settings.chaos01ColorChaotic.colorObject

        self.__build()

    def __run(self) -> None:
        """Main method for running a view."""
        pass

    def __build(self) -> None:
        # Main frame
        self.frame = Frame(self.mainWindow, bg="#fff")
        self.frame.pack(side=TOP, fill=None, expand=False, padx=10, pady=10)

        # Main frame
        self.frameAnimation = Frame(self.frame, bg="#fff")
        self.frameAnimation.pack(side=TOP, fill=None, expand=False, padx=10, pady=10, anchor=NW)
        
        self.labelAnimation = Label(self.frameAnimation, text="Animation", anchor='w', bg=self.frameBG)
        self.labelAnimation.grid(column=0, row=0, sticky=W)

        # Set size of cells (for increasing and decreasing size it works like a zoom)
        self.labelSize = Label(self.frameAnimation, text="Cell size (int)", anchor='w', bg=self.frameBG)
        self.labelSize.grid(column=0, row=1, sticky=W)
        self.entrySize = Entry(self.frameAnimation)
        self.entrySize.grid(column=1, row=1, padx=10, pady=5, sticky=W)
        self.entrySize.insert(0, self.applicationView.settings.cellSize)

        # Set a main color of a cell, if cell has a more than two states it makes other colors automatically based on the main color
        self.labelRule = Label(self.frameAnimation, text="Cell color", anchor='w', bg=self.frameBG)
        self.labelRule.grid(column=0, row=2, sticky=W)
        self.entryColor = Button(self.frameAnimation, text="", width=5, background=self.applicationView.settings.color.get_hex(), command=lambda buttonColor = self, colorCode = self.colorCode: self.__choose_color(buttonColor, colorCode)) # self.__choose_color
        self.entryColor.grid(column=1, row=2, padx=10, pady=5, sticky=W)

        # Paths frame
        self.framePaths = Frame(self.frame, bg="#fff")
        self.framePaths.pack(side=TOP, fill=None, expand=False, padx=10, pady=10, anchor=NW)
        
        self.labelPaths = Label(self.framePaths, text="Paths", anchor='w', bg=self.frameBG)
        self.labelPaths.grid(column=0, row=0, sticky=W)

        # Paths
        self.labelPathMain = Label(self.framePaths, text="Main path (string)", anchor='w', bg=self.frameBG)
        self.labelPathMain.grid(column=0, row=1, sticky=W)
        self.entryPathMain = Entry(self.framePaths)
        self.entryPathMain.grid(column=1, row=1, padx=10, pady=5, sticky=W)
        self.entryPathMain.insert(0, self.applicationView.settings.pathMain)

        self.labelPathCellularAutomaton = Label(self.framePaths, text="Cellular automaton path (string)", anchor='w', bg=self.frameBG)
        self.labelPathCellularAutomaton.grid(column=0, row=2, sticky=W)
        self.entryPathCellularAutomaton = Entry(self.framePaths)
        self.entryPathCellularAutomaton.grid(column=1, row=2, padx=10, pady=5, sticky=W)
        self.entryPathCellularAutomaton.insert(0, self.applicationView.settings.pathCellularAutomaton)

        self.labelPathHopfieldNetwork = Label(self.framePaths, text="Hopfield network path (string)", anchor='w', bg=self.frameBG)
        self.labelPathHopfieldNetwork.grid(column=0, row=3, sticky=W)
        self.entryPathHopfieldNetwork = Entry(self.framePaths)
        self.entryPathHopfieldNetwork.grid(column=1, row=3, padx=10, pady=5, sticky=W)
        self.entryPathHopfieldNetwork.insert(0, self.applicationView.settings.pathHopfieldNetwork)

        self.labelPathChaos01 = Label(self.framePaths, text="Chaos01 path (string)", anchor='w', bg=self.frameBG)
        self.labelPathChaos01.grid(column=0, row=4, sticky=W)
        self.entryPathChaos01 = Entry(self.framePaths)
        self.entryPathChaos01.grid(column=1, row=4, padx=10, pady=5, sticky=W)
        self.entryPathChaos01.insert(0, self.applicationView.settings.pathChaos01)

        # Modules
        # Hopfield Network frame
        self.frameHopfieldNetwork = Frame(self.frame, bg="#fff")
        self.frameHopfieldNetwork.pack(side=TOP, fill=None, expand=False, padx=10, pady=10, anchor=NW)
        
        self.labelHopfieldNetwork = Label(self.frameHopfieldNetwork, text="Hopfield Network", anchor='w', bg=self.frameBG)
        self.labelHopfieldNetwork.grid(column=0, row=0, sticky=W)

        self.labelHopfieldNetworkCellSize = Label(self.frameHopfieldNetwork, text="Cell size (int)", anchor='w', bg=self.frameBG)
        self.labelHopfieldNetworkCellSize.grid(column=0, row=1, sticky=W)
        self.entryHopfieldNetworkCellSize = Entry(self.frameHopfieldNetwork)
        self.entryHopfieldNetworkCellSize.grid(column=1, row=1, padx=10, pady=5, sticky=W)
        self.entryHopfieldNetworkCellSize.insert(0, self.applicationView.settings.hopfieldnetworkCellSize)

        # Chaos01
        self.frameChaos01 = Frame(self.frame, bg="#fff")
        self.frameChaos01.pack(side=TOP, fill=None, expand=False, padx=10, pady=10, anchor=NW)
        
        self.labelChaos01 = Label(self.frameChaos01, text="Chaos01", anchor='w', bg=self.frameBG)
        self.labelChaos01.grid(column=0, row=0, sticky=W)

        self.labelRule = Label(self.frameChaos01, text="Determinism color", anchor='w', bg=self.frameBG)
        self.labelRule.grid(column=0, row=1, sticky=W)
        self.entryColorDeterminism = Button(self.frameChaos01, text="", width=5, background=self.applicationView.settings.chaos01ColorDeterminism.get_hex(), command=lambda buttonColor = self, colorCode = self.colorCodeDeterminism: self.__choose_color(buttonColor, colorCode))
        self.entryColorDeterminism.grid(column=1, row=1, padx=10, pady=5, sticky=W)

        self.labelRule = Label(self.frameChaos01, text="Chaotic color", anchor='w', bg=self.frameBG)
        self.labelRule.grid(column=0, row=2, sticky=W)
        self.entryColorChaotic = Button(self.frameChaos01, text="", width=5, background=self.applicationView.settings.chaos01ColorChaotic.get_hex(), command=lambda buttonColor = self, colorCode = self.colorCodeChaotic: self.__choose_color(buttonColor, colorCode))
        self.entryColorChaotic.grid(column=1, row=2, padx=10, pady=5, sticky=W)

        # Apply button
        self.buttonApply = Button(self.frame, text="Apply", command=self.__apply)
        #self.buttonApply.grid(column=0, row=3, columnspan=2, padx=10, pady=5)
        self.buttonApply.pack(side=RIGHT, fill=None, expand=False, padx=10, pady=10)

    def draw(self) -> None:
        """Drawing method used for canvas"""
        pass

    def __choose_color(self, buttonColor: Button, colorCode: tuple) -> None:
        colorCode = askcolor(parent=self.mainWindow, title ="Choose color")
        buttonColor.configure(background=colorCode[1])

    def __apply(self) -> None:
        cellSizeStr = self.entrySize.get()
        entryPathMainStr = self.entryPathMain.get()
        entryPathCellularAutomatonStr = self.entryPathCellularAutomaton.get()
        entryPathHopfieldNetworkStr = self.entryPathHopfieldNetwork.get()
        entryPathChaos01Str = self.entryPathChaos01.get()
        entryHopfieldNetworkCellSizeStr = self.entryHopfieldNetworkCellSize.get()
        if not cellSizeStr.isnumeric() or not entryHopfieldNetworkCellSizeStr.isnumeric():
            return

        cellSize = int(cellSizeStr)
        hopfieldnetworkCellSize = int(entryHopfieldNetworkCellSizeStr)

        self.applicationView.settings.cellSize = cellSize
        self.applicationView.settings.color = Color(self.colorCode)
        self.applicationView.settings.pathMain = entryPathMainStr
        self.applicationView.settings.pathCellularAutomaton = entryPathCellularAutomatonStr
        self.applicationView.settings.pathHopfieldNetwork = entryPathHopfieldNetworkStr
        self.applicationView.settings.pathChaos01 = entryPathChaos01Str
        self.applicationView.settings.hopfieldnetworkCellSize = hopfieldnetworkCellSize
        self.applicationView.settings.chaos01ColorDeterminism = Color(self.colorCodeDeterminism)
        self.applicationView.settings.chaos01ColorChaotic = Color(self.colorCodeChaotic)
        self.applicationView.settings.save_to_file()

        self.applicationView.re_draw()

        if self.applicationView.hopfieldNetworkView is not None:
            self.applicationView.hopfieldNetworkView.size = hopfieldnetworkCellSize
            self.applicationView.hopfieldNetworkView.main_matrix_rectangles = []
            self.applicationView.hopfieldNetworkView.canvas.delete("all")
            self.applicationView.hopfieldNetworkView.create_grid()
            self.applicationView.hopfieldNetworkView.refresh_grid()

            if self.applicationView.hopfieldNetworkView.neuronMatrixViews:
                for neuronMatrixView in self.applicationView.hopfieldNetworkView.neuronMatrixViews:
                    neuronMatrixView.size = hopfieldnetworkCellSize
                    neuronMatrixView.canvas.delete("all")
                    neuronMatrixView.draw()
        
        self.on_closing()