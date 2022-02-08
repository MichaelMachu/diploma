from tkinter import *
from tkinter import ttk

from GraphicalUserInterface import GraphicalUserInterface

class AnimationSettingsView(GraphicalUserInterface):

    def __init__(self) -> None:
        super().__init__(Toplevel(), 500, 400, "Cellular Automaton settings")