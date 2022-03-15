from tkinter import *
from tkinter import ttk

from Bases.ViewBase import ViewBase
from Interfaces.TransferObjectInterface import TransferObjectInterface
from . import ApplicationView

from Data.DataProcess import DataProcess

class ImportView(ViewBase):

    def __init__(self, applicationView: ApplicationView, transferObject: TransferObjectInterface, name: str = "") -> None:
        super().__init__(Toplevel(applicationView.mainWindow), 500, 400, "Import "+ name +" from a file", applicationView.windowHandler)
        self.applicationView = applicationView

        self.transferObject = transferObject

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
        self.buttonCreate = Button(self.frame, text="Import", command=self.__import)
        self.buttonCreate.grid(column=0, row=1, columnspan=2, padx=10, pady=5)

    def draw(self) -> None:
        """Drawing method used for canvas"""
        pass

    def __import(self) -> None:
        filename = self.entryFileName.get()
        if (not (filename and not filename.isspace())):
            return

        dictData = DataProcess.load_from_json_file(filename)
        if dictData is None:
            return
        

        transferObject = type(self.transferObject).set_by_dict(dictData)

        """self.cellularAutomaton = CellularAutomaton(
            CATransferObject.size, CATransferObject.ruleNumber, CATransferObject.K, 
            CATransferObject.N, CATransferObject.λ, CATransferObject.seedNumber)
        self.cellularAutomaton.quiescentState = CATransferObject.quiescentState
        self.cellularAutomaton.currentState = CATransferObject.currentState
        self.cellularAutomaton.cellHistory = CATransferObject.cellHistory"""

        #jsonData = DataProcess.to_json(self.transferObject.get_as_dict())

        #DataProcess.save_to_json_file(filename, jsonData)