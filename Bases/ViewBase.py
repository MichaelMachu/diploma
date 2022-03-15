from tkinter import *

from Domain.WindowsHandler import WindowHandler
from Interfaces.GraphicalUserInterface import GraphicalUserInterface

class ViewBase(GraphicalUserInterface):

    def __init__(self, appWindow: Tk or Toplevel, width: int, height: int, title: str, windowHandler: WindowHandler = None, backgroundColor: str = "#ababab", frameBackgroundColor: str = "#ffffff") -> None:
        self.mainWindow = appWindow
        self.id = -1
        self.windowHandler = windowHandler
        self._importData = None

        self.exportView = None
        self.importView = None

        self.mainBG = backgroundColor
        self.frameBG = frameBackgroundColor

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

    def set_import_data(self, data: dict) -> None:
        self._importData = data

    def get_import_data(self) -> dict:
        return self._importData