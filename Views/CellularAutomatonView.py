from tkinter import *
from tkinter import ttk

from Interfaces.GraphicalUserInterface import GraphicalUserInterface
from . import ApplicationView
#from . import CellularAutomaton
from Domain.CellularAutomaton import CellularAutomaton
from Domain.TestCA import TestCA
from Data.DataProcess import DataProcess
from Data.CellularAutomatonTransferObject import CellularAutomatonTransferObject

from random import randint

class CellularAutomatonView(GraphicalUserInterface):

    def __init__(self, applicationView: ApplicationView) -> None: # aw.ApplicationView
        super().__init__(Toplevel(applicationView.mainWindow), 500, 400, "Cellular Automaton settings")
        self.applicationView = applicationView

        self.cellularAutomaton = self.applicationView.cellularAutomaton

        self.mainWindow.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Create object variables
        # Frames
        self.frame = None
        self.frameCA = None
        # Labels
        self.labelCAType = None
        self.labelSize = None
        self.labelRule = None
        self.labelK = None
        self.labelN = None
        self.labelLambda = None
        self.labelSeed = None
        self.labelRandom = None
        self.labelSelection = None
        self.labelFileName = None
        # Entries
        self.entrySize = None
        self.entryRule = None
        self.entryK = None
        self.entryN = None
        self.entryLambda = None
        self.entrySeed = None
        self.entryFileName = None
        # Buttons
        self.buttonCreate = None
        # Comboboxes
        self.comboboxCAType = None
        self.comboboxRandom = None
        self.comboboxSelection = None


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

        # Selection of type of CA
        self.labelCAType = Label(self.frame, text="Type of CA", anchor='w', bg=self.frameBG)
        self.labelCAType.grid(column=0, row=0, padx=5, pady=10, sticky=W)
        self.comboboxCAType = ttk.Combobox(self.frame)
        self.comboboxCAType['values'] = ("Elementary / Totalistic", "Edge of chaos", "Load from file")
        self.comboboxCAType['state'] = 'readonly'
        self.comboboxCAType.set("Elementary / Totalistic")
        self.comboboxCAType.bind("<<ComboboxSelected>>", self.__selection_CA_type)
        self.comboboxCAType.grid(column=1, row=0, padx=0, pady=10, sticky=W)

        # CA frame
        self.frameCA = Frame(self.frame, bg=self.frameBG)
        self.frameCA.grid(column=0, row=1, columnspan=2, padx=10, pady=5, sticky=W)

        # Build CA form
        self.__build_frame_CA()
        self.__set_values_to_entries()
        

    def __clear_frame(self) -> None:
        for widget in self.frameCA.winfo_children():
            widget.destroy()

    def __create_entry_size(self, row: int) -> None:
        # Size of the neighborhood (1 dimension)
        self.labelSize = Label(self.frameCA, text="Size of the world (int)", anchor='w', bg=self.frameBG)
        self.labelSize.grid(column=0, row=row, sticky=W)
        self.entrySize = Entry(self.frameCA)
        self.entrySize.grid(column=1, row=row, padx=10, pady=5, sticky=W)

    def __create_entry_rule(self, row: int) -> None:
        # Rule number for generating the next generation
        self.labelRule = Label(self.frameCA, text="Rule value (int)", anchor='w', bg=self.frameBG)
        self.labelRule.grid(column=0, row=row, sticky=W)
        self.entryRule = Entry(self.frameCA)
        self.entryRule.grid(column=1, row=row, padx=10, pady=5, sticky=W)

    def __create_entry_K(self, row: int) -> None:
        # Number of states for a cell (color)
        self.labelK = Label(self.frameCA, text="Number of states K (int)", anchor='w', bg=self.frameBG)
        self.labelK.grid(column=0, row=row, sticky=W)
        self.entryK = Entry(self.frameCA)
        self.entryK.grid(column=1, row=row, padx=10, pady=5, sticky=W)

    def __create_entry_N(self, row: int) -> None:
        # Number of pattern of neighborhood
        self.labelN = Label(self.frameCA, text="Neighborhood pattern N (int)", anchor='w', bg=self.frameBG)
        self.labelN.grid(column=0, row=row, sticky=W)
        self.entryN = Entry(self.frameCA)
        self.entryN.grid(column=1, row=row, padx=10, pady=5, sticky=W)

    def __create_entry_lambda(self, row: int) -> None:
        # Number of pattern of neighborhood
        self.labelLambda = Label(self.frameCA, text="Lambda value λ (float)", anchor='w', bg=self.frameBG)
        self.labelLambda.grid(column=0, row=row, sticky=W)
        self.entryLambda = Entry(self.frameCA)
        self.entryLambda.grid(column=1, row=row, padx=10, pady=5, sticky=W)

    def __create_entry_seed(self, row: int) -> None:
        # Number of pattern of neighborhood
        self.labelSeed = Label(self.frameCA, text="Seed value - optional (int)", anchor='w', bg=self.frameBG)
        self.labelSeed.grid(column=0, row=row, sticky=W)
        self.entrySeed = Entry(self.frameCA)
        self.entrySeed.grid(column=1, row=row, padx=10, pady=5, sticky=W)

    def __create_random_selection(self, row: int) -> None:
        # Selection of the creation of the first generation
        # random base on the posibility
        self.labelRandom = Label(self.frameCA, text="Random start generation", anchor='w', bg=self.frameBG)
        self.labelRandom.grid(column=0, row=row, sticky=W)
        self.comboboxRandom = ttk.Combobox(self.frameCA)
        self.comboboxRandom['values'] = ("True", "False")
        self.comboboxRandom['state'] = 'readonly'
        self.comboboxRandom.set("True")
        self.comboboxRandom.bind("<<ComboboxSelected>>", self.__selection_change_status)
        self.comboboxRandom.grid(column=1, row=row, padx=10, pady=5, sticky=W)
        # generate first cell at center, left or right side (in the middle of the dimension, first position of the dimension or last position)
        self.labelSelection = Label(self.frameCA, text="Selection (it is set only, if random is False)", anchor='w', bg=self.frameBG)
        self.labelSelection.grid(column=0, row=row+1, sticky=W)
        self.comboboxSelection = ttk.Combobox(self.frameCA)
        self.comboboxSelection['values'] = ("center", "left", "right")
        self.comboboxSelection['state'] = "disabled"
        self.comboboxSelection.set("center")
        self.comboboxSelection.grid(column=1, row=row+1, padx=10, pady=5, sticky=W)

    def __create_button_create(self, row: int) -> None:
        # Create button
        self.buttonCreate = Button(self.frameCA, text="Create a new Cellular Automaton", command=self.__create_ca)
        self.buttonCreate.grid(column=0, row=row, columnspan=2, padx=10, pady=5)

    def __build_frame_CA(self) -> None:
        self.__clear_frame()
        self.__create_entry_size(0)
        self.__create_entry_rule(1)
        self.__create_entry_K(2)
        self.__create_random_selection(3)   # It takes two rows
        self.__create_button_create(5)

    def __build_frame_CA_EdgeOfChaos(self) -> None:
        self.__clear_frame()
        self.__create_entry_size(0)
        self.__create_entry_K(1)
        self.__create_entry_N(2)
        self.__create_entry_lambda(3)
        self.__create_entry_seed(4)
        self.__create_random_selection(5)   # It takes two rows
        self.__create_button_create(7)

    def __build_frame_CA_FromFile(self) -> None:
        self.__clear_frame()
        self.labelFileName = Label(self.frameCA, text="Filename or full path with a filename\n - without file suffix name (string)", anchor='w', bg=self.frameBG)
        self.labelFileName.grid(column=0, row=0, sticky=W)
        self.entryFileName = Entry(self.frameCA)
        self.entryFileName.grid(column=1, row=0, padx=10, pady=5, sticky=W)

        self.__create_button_create(1)

    def __entry_set_value(self, entry: Entry, value: str) -> None:
        if entry is None:
            return

        if not entry.winfo_exists():
            return

        entry.delete(0, "end")
        entry.insert(0, value)

    def __combobox_set_value(self, combobox: ttk.Combobox, value: str) -> None:
        if combobox is None:
            return

        if not combobox.winfo_exists():
            return
        
        combobox.set(value)

    def __set_values_to_entries(self) -> None:
        if self.cellularAutomaton is not None:
            if self.cellularAutomaton.λ is None:
                self.__entry_set_value(self.entrySize, self.cellularAutomaton.size)
                self.__entry_set_value(self.entryRule, self.cellularAutomaton.rule)
                self.__entry_set_value(self.entryK, self.cellularAutomaton.K)
                #self.__combobox_set_value(self.comboboxRandom, self.cellularAutomaton.K)
                #self.__combobox_set_value(self.comboboxSelection, self.cellularAutomaton.K)
            else:
                self.__entry_set_value(self.entrySize, self.cellularAutomaton.size)
                self.__entry_set_value(self.entryK, self.cellularAutomaton.K)
                self.__entry_set_value(self.entryN, self.cellularAutomaton.N)
                self.__entry_set_value(self.entryLambda, self.cellularAutomaton.λ)
                self.__entry_set_value(self.entrySeed, self.cellularAutomaton.seedNumber)

    def __selection_CA_type(self, event: EventType) -> None:
        if self.comboboxCAType.get() == "Elementary / Totalistic":
            self.__build_frame_CA()
        elif self.comboboxCAType.get() == "Edge of chaos":
            self.__build_frame_CA_EdgeOfChaos()
        else:
            self.__build_frame_CA_FromFile()

        self.__set_values_to_entries()


    def __selection_change_status(self, event) -> None:
        state = "disabled" if self.comboboxRandom.get() == "True" else "readonly"
        self.comboboxSelection.configure(state=state)

    def draw(self) -> None:
        """Drawing method used for canvas"""
        pass

    def is_float(self, value: str) -> bool:
        """Check if a string value can be converted to float."""
        try:
            float(value)
            return True
        except ValueError:
            return False

    def is_int(self, value: str) -> bool:
        """Check if a string value can be converted to int."""
        try:
            int(value)
            return True
        except ValueError:
            return False

    def __create_ca(self) -> None:
        if self.comboboxCAType.get() == "Elementary / Totalistic":
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

            self.cellularAutomaton = CellularAutomaton(size, rule, sizeK)

            # Check if given parameters are valid
            if not self.cellularAutomaton.is_rule_valid():
                return

            self.__set_ca(random, selection)
        elif self.comboboxCAType.get() == "Edge of chaos":
            sizeStr = self.entrySize.get()
            KStr = self.entryK.get()
            NStr = self.entryN.get()
            lambdaStr = self.entryLambda.get()
            seedStr = self.entrySeed.get()
            if not sizeStr.isnumeric() or not KStr.isnumeric() or not NStr.isnumeric() or not self.is_float(lambdaStr):
                return

            size = int(sizeStr)
            size = 1 if size < 1 else size
            sizeK = int(KStr)
            sizeK = 2 if sizeK < 2 else sizeK
            sizeN = int(NStr)
            sizeN = 3 if sizeN < 3 else sizeN
            lambdaValue = float(lambdaStr)
            lambdaValue = 0.0 if lambdaValue < 0.0 else 1.0 if lambdaValue > 1.0 else lambdaValue
            if seedStr.isnumeric():
                seedNumber = int(seedStr)
                seedNumber = 0 if seedNumber < 0 else seedNumber
            else:
                seedNumber = None
            #seedNumber = int(seedStr) if seedStr.isnumeric() else None # seed can support only positive values because of numpy
            random = self.comboboxRandom.get() == "True"
            selection = self.comboboxSelection.get()

            self.cellularAutomaton = CellularAutomaton(size=size, K=sizeK, N=sizeN, λ=lambdaValue, seedNumber=seedNumber)

            #testCa = TestCA(5, 4, size, False, True, randint(-2147483648, 2147483647))    # 123
            #print("val = ", testCa.getRulesUsed())
            #print("max = ", testCa.getRuleCount())
            #print("lambda = ", testCa.getLambda())
            #testCa.setRulesUsed(100) # 189
            #print("lambda = ", testCa.getLambda())

            self.__set_ca(random, selection)
        else:
            filename = self.entryFileName.get()
            if (not (filename and not filename.isspace())):
                return

            dictData = DataProcess.load_from_json_file(filename)
            if dictData is None:
                return
            #dictData = DataProcess.to_dict(jsonData)
            CATransferObject = CellularAutomatonTransferObject.set_by_dict(dictData)

            self.cellularAutomaton = CellularAutomaton(
                CATransferObject.size, CATransferObject.rule, CATransferObject.K, 
                CATransferObject.N, CATransferObject.λ, CATransferObject.seedNumber)
            self.cellularAutomaton.quiescentState = CATransferObject.quiescentState
            self.cellularAutomaton.currentState = CATransferObject.currentState
            self.cellularAutomaton.cellHistory = CATransferObject.cellHistory
            
            self.applicationView.re_draw()
            self.applicationView.buttonAnim.configure(state=DISABLED)
            self.applicationView.buttonAnimPause.configure(state=ACTIVE)
            self.applicationView.buttonAnimContinue.configure(state=ACTIVE)
            


        #self.cellularAutomaton.generate_start(random, selection)

        #print(self.cellularAutomaton.rule)
        

        self.applicationView.buttonCaSave.configure(state=ACTIVE)

        self.applicationView.cellularAutomaton = self.cellularAutomaton
        #self.applicationView.testCa = testCa

        #self.on_closing()
    
    def __set_ca(self, random: bool, selection: str) -> None:
        self.cellularAutomaton.generate_start(random, selection)

        self.applicationView.continueDraw = False
        self.applicationView.offsetY = 0
        self.applicationView.canvas.delete("all")
        self.applicationView.buttonAnim.configure(state=ACTIVE)
        self.applicationView.buttonAnimPause.configure(state=DISABLED)
        self.applicationView.buttonAnimContinue.configure(state=DISABLED)
        self.applicationView.draw_step(self.cellularAutomaton.currentState)

    def on_closing(self) -> None:
        self.applicationView.isCaMenuExists = False
        self.mainWindow.destroy()