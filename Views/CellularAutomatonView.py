from tkinter import *
from tkinter import ttk

from Interfaces.GraphicalUserInterface import GraphicalUserInterface
from . import ApplicationView
#from . import CellularAutomaton
from Domain.CellularAutomaton import CellularAutomaton
from Domain.TestCA import TestCA

from random import randint

class CellularAutomatonView(GraphicalUserInterface):

    def __init__(self, applicationView: ApplicationView) -> None: # aw.ApplicationView
        super().__init__(Toplevel(applicationView.mainWindow), 500, 400, "Cellular Automaton settings")
        self.applicationView = applicationView

        self.cellularAutomaton = self.applicationView.cellularAutomaton

        self.mainWindow.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.__build()

    def __run(self) -> None:
        """Main method for running a view."""
        pass

    def __build(self) -> None:
        # Main frame
        self.frame = Frame(self.mainWindow, bg="#fff")
        self.frame.pack(side=TOP, fill=None, expand=False, padx=10, pady=10)
        
        # Size of the neighborhood (1 dimension)
        self.labelSize = Label(self.frame, text="Size (int)", anchor='w')
        self.labelSize.grid(column=0, row=0, sticky=W)
        self.entrySize = Entry(self.frame)
        self.entrySize.grid(column=1, row=0, padx=10, pady=5, sticky=W)

        # Rule number for generating the next generation
        self.labelRule = Label(self.frame, text="Rule (int)", anchor='w')
        self.labelRule.grid(column=0, row=1, sticky=W)
        self.entryRule = Entry(self.frame)
        self.entryRule.grid(column=1, row=1, padx=10, pady=5, sticky=W)

        # Number of states for a cell (color)
        self.labelK = Label(self.frame, text="K states (int)", anchor='w')
        self.labelK.grid(column=0, row=2, sticky=W)
        self.entryK = Entry(self.frame)
        self.entryK.grid(column=1, row=2, padx=10, pady=5, sticky=W)

        # Selection of the creation of the first generation
        # random base on the posibility
        self.labelRandom = Label(self.frame, text="Random start generation", anchor='w')
        self.labelRandom.grid(column=0, row=3, sticky=W)
        self.comboboxRandom = ttk.Combobox(self.frame)
        self.comboboxRandom['values'] = ("True", "False")
        self.comboboxRandom['state'] = 'readonly'
        self.comboboxRandom.set("True")
        self.comboboxRandom.grid(column=1, row=3, padx=10, pady=5, sticky=W)
        # generate first cell at center, left or right side (in the middle of the dimension, first position of the dimension or last position)
        self.labelSelection = Label(self.frame, text="Selection (it is set only, if random is False)", anchor='w')
        self.labelSelection.grid(column=0, row=4, sticky=W)
        self.comboboxSelection = ttk.Combobox(self.frame)
        self.comboboxSelection['values'] = ("center", "left", "right")
        self.comboboxSelection['state'] = 'readonly'
        self.comboboxSelection.set("center")
        self.comboboxSelection.grid(column=1, row=4, padx=10, pady=5, sticky=W)

        # Create button
        self.buttonCreate = Button(self.frame, text="Create a new Cellular Automaton", command=self.__create_ca)
        self.buttonCreate.grid(column=0, row=5, columnspan=2, padx=10, pady=5)

    def draw(self) -> None:
        """Drawing method used for canvas"""
        pass

    def __create_ca(self) -> None:
        sizeStr = self.entrySize.get()
        ruleStr = self.entryRule.get()
        KStr = self.entryK.get()
        if not sizeStr.isnumeric() or not ruleStr.isnumeric() or not KStr.isnumeric():
            return

        size = int(sizeStr)
        rule = int(ruleStr)
        sizeK = int(KStr)
        random = self.comboboxRandom.get() == "True"
        selection = self.comboboxSelection.get()

        #print(size, rule, sizeK, random, selection)

        #self.cellularAutomaton = CellularAutomaton(size, rule, sizeK)
        self.cellularAutomaton = CellularAutomaton(size, rule, 4, 5, 0.2) # rule = 100  544
        #testCa = TestCA(5, 4, size, False, True, randint(-2147483648, 2147483647))    # 123
        #print("val = ", testCa.getRulesUsed())
        #print("max = ", testCa.getRuleCount())
        #print("lambda = ", testCa.getLambda())
        #testCa.setRulesUsed(100) # 189
        #print("lambda = ", testCa.getLambda())

        # Check if given parameters are valid
        if not self.cellularAutomaton.is_rule_valid():
            return

        self.cellularAutomaton.generate_start(random, selection)

        #print(self.cellularAutomaton.rule)

        self.applicationView.continueDraw = False
        self.applicationView.offsetY = 0
        self.applicationView.canvas.delete("all")
        self.applicationView.draw_step(self.cellularAutomaton.currentState)

        self.applicationView.buttonAnim.configure(state=ACTIVE)
        self.applicationView.buttonAnimPause.configure(state=DISABLED)
        self.applicationView.buttonAnimContinue.configure(state=DISABLED)

        self.applicationView.cellularAutomaton = self.cellularAutomaton
        #self.applicationView.testCa = testCa

        #self.on_closing()

    def on_closing(self) -> None:
        self.applicationView.isCaMenuExists = False
        self.mainWindow.destroy()