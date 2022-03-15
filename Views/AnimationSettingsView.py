from tkinter import *
from tkinter.colorchooser import askcolor
from Domain.Color import Color

from Bases.ViewBase import ViewBase
from . import ApplicationView

class AnimationSettingsView(ViewBase):

    def __init__(self, applicationView: ApplicationView) -> None:
        super().__init__(Toplevel(applicationView.mainWindow), 500, 400, "Animation settings", applicationView.windowHandler)
        self.applicationView = applicationView
        self.mainWindow.attributes("-topmost", True)

        self.colorCode = self.applicationView.animationSettings.color.colorObject

        self.__build()

    def __run(self) -> None:
        """Main method for running a view."""
        pass

    def __build(self) -> None:
        # Main frame
        self.frame = Frame(self.mainWindow, bg="#fff")
        self.frame.pack(side=TOP, fill=None, expand=False, padx=10, pady=10)
        
        # Set size of cells (for increasing and decreasing size it works like a zoom)
        self.labelSize = Label(self.frame, text="Cell size (int)", anchor='w', bg=self.frameBG)
        self.labelSize.grid(column=0, row=0, sticky=W)
        self.entrySize = Entry(self.frame)
        self.entrySize.grid(column=1, row=0, padx=10, pady=5, sticky=W)
        self.entrySize.insert(0, self.applicationView.animationSettings.cellSize)

        # Set a main color of a cell, if cell has a more than two states it makes other colors automatically based on the main color
        self.labelRule = Label(self.frame, text="Cell color", anchor='w', bg=self.frameBG)
        self.labelRule.grid(column=0, row=1, sticky=W)
        self.entryColor = Button(self.frame, text="", width=5, background=self.applicationView.animationSettings.color.get_hex(), command=self.__choose_color)
        self.entryColor.grid(column=1, row=1, padx=10, pady=5, sticky=W)

        # Apply button
        self.buttonApply = Button(self.frame, text="Apply", command=self.__apply)
        self.buttonApply.grid(column=0, row=2, columnspan=2, padx=10, pady=5)

    def draw(self) -> None:
        """Drawing method used for canvas"""
        pass

    def __choose_color(self) -> None:
        self.colorCode = askcolor(parent=self.mainWindow, title ="Choose color")
        self.entryColor.configure(background=self.colorCode[1])

    def __apply(self) -> None:
        cellSizeStr = self.entrySize.get()
        if not cellSizeStr.isnumeric():
            return

        cellSize = int(cellSizeStr)

        self.applicationView.animationSettings.cellSize = cellSize
        self.applicationView.animationSettings.color = Color(self.colorCode)

        self.applicationView.re_draw()
        
        self.on_closing()