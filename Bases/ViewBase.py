from tkinter import *

from Domain.WindowsHandler import WindowHandler
from Interfaces.GraphicalUserInterface import GraphicalUserInterface

class ViewBase(GraphicalUserInterface):

    def __init__(self, appWindow: Tk or Toplevel, width: int, height: int, title: str, windowHandler: WindowHandler = None, backgroundColor: str = "#ababab") -> None:
        self.mainWindow = appWindow
        self.id = -1
        self.windowHandler = windowHandler

        self.mainBG = backgroundColor

        self.mainWindow.minsize(width, height)
        self.mainWindow.title(title)
        self.mainWindow.configure(background=backgroundColor)

        if self.windowHandler is not None:
            self.mainWindow.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.__build()
        self.__run()

    def __run(self) -> None:
        pass

    def __build(self) -> None:
        pass

    def draw(self) -> None:
        pass

    def on_closing(self) -> None:
        self.windowHandler.destroy(self)