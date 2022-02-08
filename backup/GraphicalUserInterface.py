from tkinter import *
from tkinter import ttk


class GraphicalUserInterface():
    """Settings the whole view"""

    def __init__(self, appWindow: Tk or Toplevel, width: int, height: int, title: str, backgroundColor: str = "#ababab") -> None:
        self.mainWindow = appWindow

        self.mainWindow.minsize(width, height)
        self.mainWindow.title(title)
        self.mainWindow.configure(background=backgroundColor)

        #self.root.protocol("WM_DELETE_WINDOW", self.on_closing_root)

        self.__build()
        self.__run()

    def __run(self) -> None:
        """Main method for running a view."""
        pass

    def __build(self) -> None:
        """Method for building the whole view"""
        pass

    def draw(self) -> None:
        """Drawing method used for canvas"""
        pass