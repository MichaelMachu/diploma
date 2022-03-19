from tkinter import *
from tkinter import ttk

from Bases.ViewBase import ViewBase
from . import ApplicationView
from .Domain.Graph import Graph

class Chaos01View(ViewBase):

    def __init__(self, applicationView: ApplicationView) -> None:
        super().__init__(Toplevel(applicationView.mainWindow), 500, 100, "Import "+ name +" from a file", applicationView.windowHandler)
        self.applicationView = applicationView

        self.filePath = filePath
        self.graph = Graph()

        self.__build()

    def __run(self) -> None:
        """Main method for running a view."""
        pass

    def __build(self) -> None:
        # Main frame
        self.frame = Frame(self.mainWindow, bg=self.frameBG)
        self.frame.pack(side=TOP, fill=None, expand=False, padx=1, pady=1)
        self.frame.columnconfigure(1, weight=1)

        # Chaos01
        self.frameChaos01 = Frame(self.mainWindow, bg=self.frameBG)
        self.frameChaos01.pack(side=TOP, fill=None, expand=False, padx=1, pady=1)
        self.frameChaos01.columnconfigure(1, weight=1)

        self.labelSkip = Label(self.frame, text="Skip (int)", anchor='w', bg=self.frameBG)
        self.labelSkip.grid(column=0, row=0, sticky=W)
        self.entrySkip = Entry(self.frame)
        self.entrySkip.grid(column=1, row=0, padx=10, pady=5, sticky=W)

        self.labelCut = Label(self.frame, text="Cut (int)", anchor='w', bg=self.frameBG)
        self.labelCut.grid(column=0, row=1, sticky=W)
        self.entryCut = Entry(self.frame)
        self.entryCut.grid(column=1, row=1, padx=10, pady=5, sticky=W)

        # Function
        self.frameFunction = Frame(self.mainWindow, bg=self.frameBG)
        self.frameFunction.pack(side=TOP, fill=None, expand=False, padx=1, pady=1)
        self.frameFunction.columnconfigure(1, weight=1)

        # Matplotlib Canvas
        self.frameCanvas = Frame(self.mainWindow, bg="#ababab")
        self.frameCanvas.grid(column=0, row=0, sticky="nsew")
        self.frameCanvas.grid_rowconfigure(0, weight=1)
        self.frameCanvas.grid_columnconfigure(0, weight=1)

        self.frameCanvas.rowconfigure(0, weight=1)
        self.frameCanvas.rowconfigure(1, weight=1)

        self.canvas = FigureCanvasTkAgg(self.graph.fig, master=self.mainWindow)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        self.canvasToolbar = NavigationToolbar2Tk(self.canvas, self.mainWindow, pack_toolbar=False)
        self.canvasToolbar.update()
        self.canvasToolbar.pack(side=BOTTOM, fill=X)
        

        # Create button
        self.buttonCreate = Button(self.frame, text="Import", command=self.__import)
        self.buttonCreate.grid(column=0, row=1, columnspan=2, padx=10, pady=5)

    def __clear_frame(self) -> int:
        for widget in self.frameFunction.winfo_children():
            widget.destroy()
        return 0

    def __create_entry_size(self, row: int) -> int:
        # Size of the neighborhood (1 dimension)
        self.labelSize = Label(self.frameCA, text="Size of the world (int)", anchor='w', bg=self.frameBG)
        self.labelSize.grid(column=0, row=row, sticky=W)
        self.entrySize = Entry(self.frameCA)
        self.entrySize.grid(column=1, row=row, padx=10, pady=5, sticky=W)
        return row + 1

    def __create_entry_size_2D(self, row: int) -> int:
        # Size of the neighborhood (2 dimension)
        self.labelSizeX = Label(self.frameCA, text="Width of the world (int)", anchor='w', bg=self.frameBG)
        self.labelSizeX.grid(column=0, row=row, sticky=W)
        self.entrySizeX = Entry(self.frameCA)
        self.entrySizeX.grid(column=1, row=row, padx=10, pady=5, sticky=W)
        row += 1
        self.labelSizeY = Label(self.frameCA, text="Height of the world (int)", anchor='w', bg=self.frameBG)
        self.labelSizeY.grid(column=0, row=row, sticky=W)
        self.entrySizeY = Entry(self.frameCA)
        self.entrySizeY.grid(column=1, row=row, padx=10, pady=5, sticky=W)
        return row + 1

    def __create_entry_rule(self, row: int) -> int:
        # Rule number for generating the next generation
        self.labelRule = Label(self.frameCA, text="Rule value (int)", anchor='w', bg=self.frameBG)
        self.labelRule.grid(column=0, row=row, sticky=W)
        self.entryRule = Entry(self.frameCA)
        self.entryRule.grid(column=1, row=row, padx=10, pady=5, sticky=W)
        return row + 1

    def __create_entry_K(self, row: int) -> int:
        # Number of states for a cell (color)
        self.labelK = Label(self.frameCA, text="Number of states K (int)", anchor='w', bg=self.frameBG)
        self.labelK.grid(column=0, row=row, sticky=W)
        self.entryK = Entry(self.frameCA)
        self.entryK.grid(column=1, row=row, padx=10, pady=5, sticky=W)
        return row + 1

    def __create_entry_N(self, row: int) -> int:
        # Number of pattern of neighborhood
        self.labelN = Label(self.frameCA, text="Neighborhood pattern N (int)", anchor='w', bg=self.frameBG)
        self.labelN.grid(column=0, row=row, sticky=W)
        self.entryN = Entry(self.frameCA)
        self.entryN.grid(column=1, row=row, padx=10, pady=5, sticky=W)
        return row + 1

    def __create_entry_lambda(self, row: int) -> int:
        # Number of pattern of neighborhood
        self.labelLambda = Label(self.frameCA, text="Lambda value λ (float)", anchor='w', bg=self.frameBG)
        self.labelLambda.grid(column=0, row=row, sticky=W)
        self.entryLambda = Entry(self.frameCA)
        self.entryLambda.grid(column=1, row=row, padx=10, pady=5, sticky=W)
        return row + 1

    def __create_entry_seed(self, row: int) -> int:
        # Number of pattern of neighborhood
        self.labelSeed = Label(self.frameCA, text="Seed value - optional (int)", anchor='w', bg=self.frameBG)
        self.labelSeed.grid(column=0, row=row, sticky=W)
        self.entrySeed = Entry(self.frameCA)
        self.entrySeed.grid(column=1, row=row, padx=10, pady=5, sticky=W)
        return row + 1

    def __create_random_selection(self, row: int) -> int:
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
        row = row + 1
        # generate first cell at center, left or right side (in the middle of the dimension, first position of the dimension or last position)
        self.labelSelection = Label(self.frameCA, text="Selection (it is set only, if random is False)", anchor='w', bg=self.frameBG)
        self.labelSelection.grid(column=0, row=row, sticky=W)
        self.comboboxSelection = ttk.Combobox(self.frameCA)
        self.comboboxSelection['values'] = ("center", "left", "right")
        self.comboboxSelection['state'] = "disabled"
        self.comboboxSelection.set("center")
        self.comboboxSelection.grid(column=1, row=row, padx=10, pady=5, sticky=W)
        return row + 1

    def __create_pattern2D_selection(self, row: int) -> int:
        # Selection of the 2D pattern
        self.labelPattern2D = Label(self.frameCA, text="Select neighborhood pattern", anchor='w', bg=self.frameBG)
        self.labelPattern2D.grid(column=0, row=row, sticky=W)
        self.comboboxPattern2D = ttk.Combobox(self.frameCA)
        self.comboboxPattern2D['values'] = ("moore", "neuman")
        self.comboboxPattern2D['state'] = 'readonly'
        self.comboboxPattern2D.set("moore")
        self.comboboxPattern2D.grid(column=1, row=row, padx=10, pady=5, sticky=W)
        return row + 1

    def __create_button_create(self, row: int) -> int:
        # Create button
        self.buttonCreate = Button(self.frameCA, text="Create a new Cellular Automaton", command=self.__create_ca)
        self.buttonCreate.grid(column=0, row=row, columnspan=2, padx=10, pady=5)
        return row + 1

    def __build_frame_CA(self) -> None:
        row = self.__clear_frame()
        row = self.__create_entry_size(row)
        row = self.__create_entry_rule(row)
        row = self.__create_entry_K(row)
        row = self.__create_random_selection(row)   # It takes two rows
        row = self.__create_button_create(row)

    def __build_frame_CA_EdgeOfChaos(self) -> None:
        row = self.__clear_frame()
        row = self.__create_entry_size(row)
        row = self.__create_entry_K(row)
        row = self.__create_entry_N(row)
        row = self.__create_entry_lambda(row)
        row = self.__create_entry_seed(row)
        row = self.__create_random_selection(row)   # It takes two rows
        row = self.__create_button_create(row)

    def __build_frame_CA_2D(self) -> None:
        row = self.__clear_frame()
        row = self.__create_entry_size_2D(row)  # It takes two rows
        row = self.__create_entry_rule(row)
        #row = self.__create_entry_K(row)
        row = self.__create_pattern2D_selection(row)
        row = self.__create_random_selection(row)   # It takes two rows
        row = self.__create_button_create(row)

    def __build_frame_CA_FromFile(self) -> None:
        row = self.__clear_frame()
        self.labelFileName = Label(self.frameCA, text="Filename or full path with a filename\n - without file suffix name (string)", anchor='w', bg=self.frameBG)
        self.labelFileName.grid(column=0, row=row, sticky=W)
        self.entryFileName = Entry(self.frameCA)
        self.entryFileName.grid(column=1, row=row, padx=10, pady=5, sticky=W)
        row = row + 1
        row = self.__create_button_create(row)

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
                if self.cellularAutomaton.dimension == 2:
                    self.__entry_set_value(self.entrySizeX, self.cellularAutomaton.size[0])
                    self.__entry_set_value(self.entrySizeY, self.cellularAutomaton.size[1])
                    self.__combobox_set_value(self.comboboxPattern2D, self.cellularAutomaton.pattern2D)
                else:
                    self.__entry_set_value(self.entrySize, self.cellularAutomaton.size)
                self.__entry_set_value(self.entryRule, self.cellularAutomaton.ruleNumber)
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
        elif self.comboboxCAType.get() == "2D":
            self.__build_frame_CA_2D()
        else:
            self.__build_frame_CA_FromFile()

        self.__set_values_to_entries()

    def draw(self) -> None:
        """Drawing method used for canvas"""
        pass

    def __show_graph(self) -> None:
        filename = self.entryFileName.get()
        if (not (filename and not filename.isspace())):
            return

        

        self.on_closing()