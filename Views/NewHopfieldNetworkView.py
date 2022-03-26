from tkinter import *
import numpy as np

from Bases.ViewBase import ViewBase

from Domain.HopfieldNetwork import HopfieldNetwork

class NewHopfieldNetworkView(ViewBase):

    def __init__(self, hopfieldNetworkView: ViewBase) -> None:
        super().__init__(Toplevel(hopfieldNetworkView.mainWindow), 400, 300, "New Hopfield Network", hopfieldNetworkView.applicationView.windowHandler)
        self.applicationView = hopfieldNetworkView.applicationView
        self.mainWindow.attributes("-topmost", True)

        self.hopfieldNetworkView = hopfieldNetworkView

        self.__build()

    def __run(self) -> None:
        """Main method for running a view."""
        pass

    def __build(self) -> None:
        # Main frame
        self.frame = Frame(self.mainWindow, bg="#fff")
        self.frame.pack(side=TOP, fill=None, expand=False, padx=10, pady=10)

        # Set size M - Width
        self.labelWidth = Label(self.frame, text="Width (int)", anchor='w', bg=self.frameBG)
        self.labelWidth.grid(column=0, row=1, sticky=W)
        self.entryWidth = Entry(self.frame)
        self.entryWidth.grid(column=1, row=1, padx=10, pady=5, sticky=W)
        self.entryWidth.insert(0, self.hopfieldNetworkView.networkSize[1])

        # Set size N - Height
        self.labelHeight = Label(self.frame, text="Height (int)", anchor='w', bg=self.frameBG)
        self.labelHeight.grid(column=0, row=2, sticky=W)
        self.entryHeight = Entry(self.frame)
        self.entryHeight.grid(column=1, row=2, padx=10, pady=5, sticky=W)
        self.entryHeight.insert(0, self.hopfieldNetworkView.networkSize[0])

        self.labelWarning = Label(self.frame, text="It is recommended to keep the width and height with a same value", anchor='w', bg=self.frameBG)
        self.labelWarning.grid(column=0, row=3, columnspan=2, sticky=W)

        # Apply button
        self.buttonApply = Button(self.frame, text="Apply", command=self.__apply)
        self.buttonApply.grid(column=0, row=4, columnspan=2, padx=10, pady=5)

    def draw(self) -> None:
        """Drawing method used for canvas"""
        pass

    def __apply(self) -> None:
        widthStr = self.entryWidth.get()
        heightStr = self.entryHeight.get()
        if not widthStr.isnumeric() or not heightStr.isnumeric():
            return

        width = int(widthStr)
        height = int(heightStr)

        #self.hopfieldNetworkView.n = height
        #self.hopfieldNetworkView.m = width

        self.hopfieldNetworkView.networkSize = (height, width)
        self.hopfieldNetworkView.hopfieldNetwork = HopfieldNetwork(self.hopfieldNetworkView.networkSize)

        self.hopfieldNetworkView.main_matrix = np.zeros(self.hopfieldNetworkView.networkSize)
        self.hopfieldNetworkView.main_matrix_rectangles = []
        self.hopfieldNetworkView.saved_matrices = []
        self.hopfieldNetworkView.max_patterns = self.hopfieldNetworkView.hopfieldNetwork.get_max_patterns()

        self.hopfieldNetworkView.canvas.delete("all")
        self.hopfieldNetworkView.create_grid()
        self.hopfieldNetworkView.labelMaxPatterns["text"] = "Max recommended amount\n of saved patterns is " + str(self.hopfieldNetworkView.max_patterns)
        
        self.on_closing()