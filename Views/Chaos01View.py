from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

from Bases.ViewBase import ViewBase
from . import ApplicationView
from Domain.Graph import Graph
from Domain.FunctionSelection import FunctionSelection

class Chaos01View(ViewBase):

    def __init__(self, applicationView: ApplicationView) -> None:
        super().__init__(Toplevel(applicationView.mainWindow), 500, 100, "Chaos01", applicationView.windowHandler)
        self.applicationView = applicationView

        self.graph = Graph()
        self.function = FunctionSelection.GetByName("logistic map")

        # Create object variables
        # Frames
        self.frame = None
        self.frameChaos01 = None
        self.frameFunction = None
        self.frameCanvas = None
        # Labels
        self.labelSkip = None
        self.labelCut = None
        self.labelFunctionType = None
        self.labelFunctionDefinition = None
        self.labelA = None
        self.labelScale = None
        self.labelRangeFrom = None
        self.labelRangeTo = None
        self.labelFileName = None
        # Entries
        self.entrySkip = None
        self.entryCut = None
        self.entryA = None
        self.entryScale = None
        self.entryRangeFrom = None
        self.entryRangeTo = None
        self.entryFileName = None
        # Buttons
        self.buttonShow = None
        # Comboboxes
        self.comboboxFunctionType = None

        self.__build()

    def __run(self) -> None:
        """Main method for running a view."""
        pass

    def __build(self) -> None:
        # Main frame
        self.frame = Frame(self.mainWindow, bg=self.frameBG)
        self.frame.pack(side=TOP, fill=None, expand=False, padx=1, pady=1)
        #self.frame.columnconfigure(1, weight=1)
        #self.frame.columnconfigure(0)
        #self.frame.rowconfigure(0, weight=1)

        # Chaos01
        self.frameChaos01 = Frame(self.frame, bg=self.frameBG)
        #self.frameChaos01.pack(side=TOP, fill=None, expand=False, padx=1, pady=1)
        self.frameChaos01.grid(column=0, row=0, sticky="nsew")
        #self.frameChaos01.columnconfigure(0, weight=1)
        #self.frameChaos01.rowconfigure(0, weight=1)

        self.labelSkip = Label(self.frameChaos01, text="Skip (int)", anchor='w', bg=self.frameBG)
        self.labelSkip.grid(column=0, row=0, sticky=W)
        self.entrySkip = Entry(self.frameChaos01)
        self.entrySkip.grid(column=1, row=0, padx=10, pady=5, sticky=W)

        self.labelCut = Label(self.frameChaos01, text="Cut (int)", anchor='w', bg=self.frameBG)
        self.labelCut.grid(column=0, row=1, sticky=W)
        self.entryCut = Entry(self.frameChaos01)
        self.entryCut.grid(column=1, row=1, padx=10, pady=5, sticky=W)

        self.labelFunctionType = Label(self.frameChaos01, text="Type of function", anchor='w', bg=self.frameBG)
        self.labelFunctionType.grid(column=0, row=2, padx=5, pady=10, sticky=W)
        self.comboboxFunctionType = ttk.Combobox(self.frameChaos01)
        self.comboboxFunctionType["values"] = ("logistic map", "sinus", "scaled normal", "scaled uniform", "Load from file")
        self.comboboxFunctionType["state"] = "readonly"
        self.comboboxFunctionType.set("logistic map")
        self.comboboxFunctionType.bind("<<ComboboxSelected>>", self.__selection_function_type)
        self.comboboxFunctionType.grid(column=1, row=2, padx=0, pady=10, sticky=W)

        # Function
        self.frameFunction = Frame(self.frameChaos01, bg=self.frameBG)
        #self.frameFunction.pack(side=TOP, fill=None, expand=False, padx=1, pady=1)
        self.frameFunction.grid(column=0, row=3, columnspan=2, padx=10, pady=5)

        # Matplotlib Canvas
        self.frameCanvas = Frame(self.frame, bg=self.frameBG) # "#ababab"
        #self.frameCanvas.pack(side=TOP, fill=None, expand=False, padx=1, pady=1, sticky=N)
        self.frameCanvas.grid(column=1, row=0, rowspan=3, sticky="nsew")
        #self.frameCanvas.grid_rowconfigure(0, weight=1)
        #self.frameCanvas.grid_columnconfigure(0, weight=1)

        #self.frameCanvas.columnconfigure(1)
        #self.frameCanvas.rowconfigure(1, weight=2)

        self.canvas = FigureCanvasTkAgg(self.graph.fig, master=self.frameCanvas)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        #self.canvas.get_tk_widget().grid(column=0, row=0, sticky="nsew")

        self.canvasToolbar = NavigationToolbar2Tk(self.canvas, self.frameCanvas, pack_toolbar=False)
        self.canvasToolbar.update()
        self.canvasToolbar.pack(side=BOTTOM, fill=X)
        #self.canvasToolbar.grid(column=0, row=1, sticky="nsew")

        # Show button
        self.buttonShow = Button(self.frameChaos01, text="Show on graph", command=self.__show_graph)
        self.buttonShow.grid(column=0, row=4, columnspan=2, padx=10, pady=5)
        #self.buttonShow.pack(fill=None, expand=False, padx=10, pady=10)

    def __clear_frame(self) -> int:
        for widget in self.frameFunction.winfo_children():
            widget.destroy()
        return 0

    def __create_label_function_definition(self, row: int) -> int:
        self.labelFunctionDefinition = Label(self.frameFunction, text="definition of the function", anchor='w', bg=self.frameBG)
        self.labelFunctionDefinition.grid(column=0, row=row, sticky=W)
        return row + 1

    def __create_entry_a(self, row: int) -> int:
        self.labelA = Label(self.frameFunction, text="a (float)", anchor='w', bg=self.frameBG)
        self.labelA.grid(column=0, row=row, sticky=W)
        self.entryA = Entry(self.frameFunction)
        self.entryA.grid(column=1, row=row, padx=10, pady=5, sticky=W)
        return row + 1

    def __create_entry_scale(self, row: int) -> int:
        self.labelScale = Label(self.frameFunction, text="scale (float)", anchor='w', bg=self.frameBG)
        self.labelScale.grid(column=0, row=row, sticky=W)
        self.entryScale = Entry(self.frameFunction)
        self.entryScale.grid(column=1, row=row, padx=10, pady=5, sticky=W)
        return row + 1

    def __create_entry_range(self, row: int) -> int:
        self.labelRangeFrom = Label(self.frameFunction, text="range from (int)", anchor='w', bg=self.frameBG)
        self.labelRangeFrom.grid(column=0, row=row, sticky=W)
        self.entryRangeFrom = Entry(self.frameFunction)
        self.entryRangeFrom.grid(column=1, row=row, padx=10, pady=5, sticky=W)
        row += 1
        self.labelRangeTo = Label(self.frameFunction, text="range to (int)", anchor='w', bg=self.frameBG)
        self.labelRangeTo.grid(column=0, row=row, sticky=W)
        self.entryRangeTo = Entry(self.frameFunction)
        self.entryRangeTo.grid(column=1, row=row, padx=10, pady=5, sticky=W)
        return row + 1

    def __build_frame_scaled_normal(self) -> None:
        row = self.__clear_frame()
        row = self.__create_entry_a(row)
        row = self.__create_entry_scale(row)

    def __build_frame_scaled_uniform(self) -> None:
        row = self.__clear_frame()
        row = self.__create_entry_a(row)
        row = self.__create_entry_range(row)

    def __build_frame_FromFile(self) -> None:
        row = self.__clear_frame()
        self.labelFileName = Label(self.frameFunction, text="Filename or full path with a filename\n - without file suffix name (string)", anchor='w', bg=self.frameBG)
        self.labelFileName.grid(column=0, row=row, sticky=W)
        self.entryFileName = Entry(self.frameFunction)
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

    def __selection_function_type(self, event: EventType) -> None:
        selection = self.comboboxFunctionType.get()
        self.function = FunctionSelection.GetByName(selection)

        if selection == "logistic map":
            self.__clear_frame()
        elif selection == "sinus":
            self.__clear_frame()
        elif selection == "scaled normal":
            self.__build_frame_scaled_normal()
            self.__entry_set_value(self.entryA, self.function.a)
            self.__entry_set_value(self.entryScale, self.function.scale)
        elif selection == "scaled uniform":
            self.__build_frame_scaled_uniform()
            self.__entry_set_value(self.entryA, self.function.a)
            self.__entry_set_value(self.entryRangeFrom, self.function.valueRange[0])
            self.__entry_set_value(self.entryRangeTo, self.function.valueRange[1])
        else:
            self.__build_frame_FromFile()

    def draw(self) -> None:
        """Drawing method used for canvas"""
        pass

    def __show_graph(self) -> None:
        filename = self.entryFileName.get()
        if (not (filename and not filename.isspace())):
            return

        

        self.on_closing()