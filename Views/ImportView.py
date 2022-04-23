from tkinter import *
from tkinter import ttk
from os import walk

from Bases.ViewBase import ViewBase
from . import ApplicationView

from Domain.Settings import Settings
from Data.DataProcess import DataProcess

class ImportView(ViewBase):

    def __init__(self, applicationView: ApplicationView, filePath: str, name: str = "") -> None:
        super().__init__(Toplevel(applicationView.mainWindow), 500, 100, "Import "+ name +" from a file", applicationView.windowHandler)
        self.applicationView = applicationView

        self.filePath = filePath
        self.paths = Settings.get_files_in_directory(filePath)
        self.fileNames = [key for key in self.paths]

        self.__build()

    def __run(self) -> None:
        """Main method for running a view."""
        pass

    def __build(self) -> None:
        # Main frame
        self.frame = Frame(self.mainWindow, bg=self.frameBG)
        self.frame.pack(side=TOP, fill=None, expand=False, padx=1, pady=1)
        self.frame.columnconfigure(1, weight=1)

        # Filename
        self.labelFileName = Label(self.frame, text="Filename", anchor='w', bg=self.frameBG) #or full path with a filename\n - without file suffix name (string)
        self.labelFileName.grid(column=0, row=0, sticky=W)
        self.comboboxFileName = ttk.Combobox(self.frame, width=30)
        self.comboboxFileName["values"] = self.fileNames
        self.comboboxFileName["state"] = "readonly"
        self.comboboxFileName.grid(column=1, row=0, padx=10, pady=5, sticky=W)

        # Create button
        self.buttonCreate = Button(self.frame, text="Import", command=self.__import)
        self.buttonCreate.grid(column=0, row=1, columnspan=2, padx=10, pady=5)

    def draw(self) -> None:
        """Drawing method used for canvas"""
        pass

    def __import(self) -> None:
        filename = self.comboboxFileName.get()
        if (not (filename and not filename.isspace())):
            return

        dataDict = DataProcess.load_from_json_file(self.filePath + filename)
        self.applicationView.set_import_data(dataDict)

        self.on_closing()