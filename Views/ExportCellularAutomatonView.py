from tkinter import *
from tkinter import ttk

from Interfaces.GraphicalUserInterface import GraphicalUserInterface
from . import ApplicationView

from Data.CellularAutomatonTransferObject import CellularAutomatonTransferObject
from Data.DataProcess import DataProcess

class ExportCellularAutomatonView(GraphicalUserInterface):

    def __init__(self, applicationView: ApplicationView) -> None:
        super().__init__(Toplevel(applicationView.mainWindow), 500, 400, "Export Cellular Automaton to a file")
        self.applicationView = applicationView

        self.cellularAutomaton = self.applicationView.cellularAutomaton

        self.mainWindow.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.__build()

    def __run(self) -> None:
        """Main method for running a view."""
        pass

    def __build(self) -> None:
        self.frameBG = "#fff"

        # Main frame
        self.frame = Frame(self.mainWindow, bg=self.frameBG)
        self.frame.pack(side=TOP, fill=None, expand=False, padx=1, pady=1)
        self.frame.columnconfigure(1, weight=1)

        # Filename
        self.labelFileName = Label(self.frame, text="Filename or full path with a filename\n - without file suffix name (string)", anchor='w', bg=self.frameBG)
        self.labelFileName.grid(column=0, row=0, sticky=W)
        self.entryFileName = Entry(self.frame)
        self.entryFileName.grid(column=1, row=0, padx=10, pady=5, sticky=W)

        # Create button
        self.buttonCreate = Button(self.frame, text="Save a Cellular Automaton", command=self.__save_ca)
        self.buttonCreate.grid(column=0, row=1, columnspan=2, padx=10, pady=5)

    def draw(self) -> None:
        """Drawing method used for canvas"""
        pass

    def __save_ca(self) -> None:
        filename = self.entryFileName.get()
        if (not (filename and not filename.isspace())):
            return

        CATransferObject = CellularAutomatonTransferObject(self.cellularAutomaton)
        jsonData = DataProcess.to_json(CATransferObject.get_as_dict())

        DataProcess.save_to_json_file(filename, jsonData)

    def on_closing(self) -> None:
        self.applicationView.isSaveCaExists = False
        self.mainWindow.destroy()