from tkinter import *
from tkinter import ttk
from types import MethodType
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from threading import Thread

from Bases.ViewBase import ViewBase
from . import ApplicationView
from Domain.Graph import Graph
from Domain.FunctionSelection import FunctionSelection
from Domain.Chaos01 import Chaos01
from Domain.Settings import Settings
from .ImportView import ImportView
from .ExportView import ExportView
from Data.Chaos01TransferObject import Chaos01TransferObject
from Data.DataProcess import DataProcess

from EnumTypes.GraphType import GraphType

class Chaos01View(ViewBase):

    def __init__(self, applicationView: ApplicationView) -> None:
        super().__init__(Toplevel(applicationView.mainWindow), 900, 600, "Chaos01", applicationView.windowHandler)
        self.applicationView = applicationView

        self.chaos01 = Chaos01()
        self.chaos01.set_skip(1)
        self.chaos01.set_cut(20)        # set skip and cut, because of the first selected function "logistic map"
        self.graph = Graph()
        self.function = FunctionSelection.GetByName("logistic map")
        self.dataType = GraphType.BIFURCATION
        self.dataTypePom = GraphType.BIFURCATION
        self.data = []
        self.paths = {}
        self.dataDict = {}

        # Create object variables
        # Frames
        self.frame = None
        self.frameChaos01 = None
        self.frameFunction = None
        self.frameCanvas = None
        # Labels
        self.labelChaos01 = None
        self.labelCalculationDataChaos01 = None
        self.labelSkip = None
        self.labelCut = None
        self.labelFunctionType = None
        self.labelDefinition = None
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
        # Buttons
        self.buttonCalculateAndShow = None
        # Comboboxes
        self.comboboxFunctionType = None
        self.comboboxFileName = None
        self.comboboxSelectedParameter = None

        self.__build()

    def __run(self) -> None:
        """Main method for running a view."""
        pass

    def __build(self) -> None:
        # Top menu
        self.menu = Menu(self.mainWindow)
        self.mainWindow.config(menu=self.menu)
        
        self.menuFile = Menu(self.menu, tearoff=False)
        self.menuFile.add_command(
            label="Import",
            command=self.__show_import_menu
        )

        self.menuExport = Menu(self.menuFile, tearoff=False)
        self.menuExport.add_command(
            label="Fast",
            command=self.__show_export_fast_menu
        )
        self.menuExport.add_command(
            label="Full",
            command=self.__show_export_full_menu
        )

        self.menuFile.add_cascade(label="Export", menu=self.menuExport)
        self.menu.add_cascade(label="File", menu=self.menuFile)

        # Main frame
        self.frame = Frame(self.mainWindow, bg=self.frameBG)
        self.frame.pack(side=TOP, fill=BOTH, expand=1, padx=1, pady=1) # fill=BOTH, expand=1    fill=None, expand=False
        #self.frame.columnconfigure(1, weight=1)
        #self.frame.columnconfigure(0)
        #self.frame.rowconfigure(0, weight=1)

        # Chaos01
        self.frameChaos01 = Frame(self.frame, bg=self.frameBG)
        #self.frameChaos01.pack(side=TOP, fill=None, expand=False, padx=1, pady=1)
        self.frameChaos01.grid(column=1, row=0, sticky="nsew", padx=(0, 10), pady=10)
        #self.frameChaos01.columnconfigure(0, weight=1)
        #self.frameChaos01.rowconfigure(0, weight=1)
        #self.frameChaos01.rowconfigure(0, weight=1)
        #self.frameChaos01.rowconfigure(1, weight=1)

        self.labelChaos01 = Label(self.frameChaos01, text="Chaos01", anchor='w', bg=self.frameBG)
        self.labelChaos01.grid(column=0, row=0, sticky=W, pady=(10, 0))

        self.labelSkip = Label(self.frameChaos01, text="Skip (int)", anchor='w', bg=self.frameBG)
        self.labelSkip.grid(column=0, row=1, sticky=W)
        self.entrySkip = Entry(self.frameChaos01)
        self.entrySkip.grid(column=1, row=1, padx=10, pady=5, sticky=W)

        self.labelCut = Label(self.frameChaos01, text="Cut (int)", anchor='w', bg=self.frameBG)
        self.labelCut.grid(column=0, row=2, sticky=W)
        self.entryCut = Entry(self.frameChaos01)
        self.entryCut.grid(column=1, row=2, padx=10, pady=5, sticky=W)

        self.labelCalculationDataChaos01 = Label(self.frameChaos01, text="Data for calculation of Chaos01", anchor='w', bg=self.frameBG)    # Bifurcation diagram   # labelBifurcationDiagram
        self.labelCalculationDataChaos01.grid(column=0, row=3, sticky=W, pady=(10, 0))

        self.labelFunctionType = Label(self.frameChaos01, text="Type of function", anchor='w', bg=self.frameBG)
        self.labelFunctionType.grid(column=0, row=4, padx=5, pady=10, sticky=W)
        self.comboboxFunctionType = ttk.Combobox(self.frameChaos01)
        self.comboboxFunctionType["values"] = ("logistic map", "sinus", "scaled normal", "scaled uniform", "Load from file")
        self.comboboxFunctionType["state"] = "readonly"
        self.comboboxFunctionType.set("logistic map")
        self.comboboxFunctionType.bind("<<ComboboxSelected>>", self.__selection_function_type)
        self.comboboxFunctionType.grid(column=1, row=4, padx=0, pady=10, sticky=W)

        # Function
        self.frameFunction = Frame(self.frameChaos01, bg=self.frameBG)
        #self.frameFunction.pack(side=TOP, fill=None, expand=False, padx=1, pady=1)
        self.frameFunction.grid(column=0, row=5, columnspan=2, padx=10, pady=5, sticky=W)

        # Matplotlib Canvas
        self.frameCanvas = Frame(self.frame, bg=self.frameBG) # "#ababab"
        #self.frameCanvas.pack(side=TOP, fill=None, expand=False, padx=1, pady=1, sticky=N)
        self.frameCanvas.grid(column=0, row=0, sticky="nsew") # rowspan=3
        #self.frameCanvas.grid_rowconfigure(0, weight=1)
        #self.frameCanvas.grid_columnconfigure(0, weight=1)
        self.frameCanvas.grid_rowconfigure(0, weight=1)
        self.frameCanvas.grid_columnconfigure(0, weight=1)

        #self.frameCanvas.columnconfigure(1)
        #self.frameCanvas.rowconfigure(1, weight=2)

        self.canvas = FigureCanvasTkAgg(self.graph.fig, master=self.frameCanvas)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        #self.canvas.get_tk_widget().grid(column=0, row=0, sticky="nsew")

        self.canvasToolbar = NavigationToolbar2Tk(self.canvas, self.frameCanvas, pack_toolbar=False)
        self.canvasToolbar.config(background=self.frameBG)
        for button in self.canvasToolbar.winfo_children():
            button.config(background=self.frameBG)
        self.canvasToolbar.update()
        self.canvasToolbar.pack(side=BOTTOM, fill=X)
        #self.canvasToolbar.grid(column=0, row=1, sticky="nsew")

        # Show button
        self.buttonCalculateAndShow = Button(self.frameChaos01, text="Calculate and show on graph", command=self.__calculate_and_show_graph)
        self.buttonCalculateAndShow.grid(column=0, row=6, columnspan=2, padx=10, pady=5)
        #self.buttonCalculateAndShow.pack(fill=None, expand=False, padx=10, pady=10)
        
        self.buttonShowGraphCourseK = Button(self.frameChaos01, text="Show course of K values on graph", command=self.__show_graph_course_of_K_values)
        self.buttonShowGraphCourseK.grid(column=1, row=7, padx=5, pady=50)
        
        self.buttonShowGraphChaos = Button(self.frameChaos01, text="Show chaotic data on graph", command=self.__show_graph_of_chaos)
        self.buttonShowGraphChaos.grid(column=0, row=7, padx=5, pady=50)
        

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.__build_frame_logistic_map()

    def __clear_frame(self) -> int:
        for widget in self.frameFunction.winfo_children():
            widget.destroy()
        return 0

    def __create_label_function_definition(self, row: int) -> int:
        self.labelDefinition = Label(self.frameFunction, text="Definition", anchor='w', bg=self.frameBG)
        self.labelDefinition.grid(column=0, row=row, sticky=W)
        self.labelFunctionDefinition = Label(self.frameFunction, text=self.function, anchor='w', bg=self.frameBG)
        self.labelFunctionDefinition.grid(column=1, row=row, sticky=W)
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

    def __build_frame_logistic_map(self) -> None:
        row = self.__clear_frame()
        row = self.__create_label_function_definition(row)

    def __build_frame_sinus(self) -> None:
        row = self.__clear_frame()
        row = self.__create_label_function_definition(row)

    def __build_frame_scaled_normal(self) -> None:
        row = self.__clear_frame()
        row = self.__create_label_function_definition(row)
        row = self.__create_entry_a(row)
        row = self.__create_entry_scale(row)

    def __build_frame_scaled_uniform(self) -> None:
        row = self.__clear_frame()
        row = self.__create_label_function_definition(row)
        row = self.__create_entry_a(row)
        row = self.__create_entry_range(row)

    def __build_frame_FromFile(self) -> None:
        row = self.__clear_frame()
        self.labelFileName = Label(self.frameFunction, text="Filename", anchor='w', bg=self.frameBG) # (string)\n - without suffix
        self.labelFileName.grid(column=0, row=row, sticky=W)
        #self.comboboxFileName = Entry(self.frameFunction)
        #self.comboboxFileName.grid(column=1, row=row, padx=10, pady=5, sticky=W)
        path = self.applicationView.settings.pathMain + "/" # + self.applicationView.settings.pathCellularAutomaton + "/"
        self.paths = Settings.get_files_in_directory(path)
        self.comboboxFileName = ttk.Combobox(self.frameFunction)
        self.comboboxFileName["values"] = [key for key in self.paths]
        self.comboboxFileName["state"] = "readonly"
        self.comboboxFileName.bind("<<ComboboxSelected>>", self.__selection_of_data)
        self.comboboxFileName.grid(column=1, row=row, padx=10, pady=5, sticky=W)
        row += 1
        self.labelSelectedParameter = Label(self.frameFunction, text="Select parameter", anchor='w', bg=self.frameBG) # (string)\n - without suffix
        self.labelSelectedParameter.grid(column=0, row=row, sticky=W)
        self.comboboxSelectedParameter = ttk.Combobox(self.frameFunction)
        self.comboboxSelectedParameter["state"] = "readonly"
        self.comboboxSelectedParameter.grid(column=1, row=row, padx=10, pady=5, sticky=W)

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
        if selection == "Load from file":
            self.__build_frame_FromFile()
        else:
            self.function = FunctionSelection.GetByName(selection)

            self.chaos01.set_skip(1)
            self.chaos01.set_cut(20)

            if selection == "logistic map":
                self.__build_frame_logistic_map()
            elif selection == "sinus":
                self.__build_frame_sinus()
            elif selection == "scaled normal":
                self.__build_frame_scaled_normal()
                self.__entry_set_value(self.entryA, self.function.a)
                self.__entry_set_value(self.entryScale, self.function.scale)
            elif selection == "scaled uniform":
                self.__build_frame_scaled_uniform()
                self.__entry_set_value(self.entryA, self.function.a)
                self.__entry_set_value(self.entryRangeFrom, self.function.valueRange[0])
                self.__entry_set_value(self.entryRangeTo, self.function.valueRange[1])
            #else:
            #    self.__build_frame_FromFile()

    def __selection_of_data(self, event: EventType) -> None:
        filename = self.comboboxFileName.get()
        if (not (filename and not filename.isspace())):
            return

        path = self.paths[filename]
        self.dataDict = DataProcess.load_from_json_file(path)

        self.comboboxSelectedParameter["values"] = [key for key in self.dataDict]
        self.comboboxSelectedParameter.set("")

        for key in self.dataDict:
            if "history" in key.lower():
                self.comboboxSelectedParameter.set(key)
                break

    def set_data_type(self, dataType: GraphType) -> None:
        #if dataType == GraphType.KVALUES and self.dataType != GraphType.KVALUES:
        #    self.dataTypePom = self.dataType
        
        #self.dataType = self.dataTypePom if self.dataType == GraphType.KVALUES else dataType
        self.dataType = dataType

    def draw(self) -> None:
        self.graph.refresh()

        if self.dataType == GraphType.BIFURCATION:
            self.graph.draw_bifurcation_diagram(self.data, 1, 
                self.applicationView.settings.chaos01ColorDeterminism.get_hex(),
                self.applicationView.settings.chaos01ColorChaotic.get_hex())
        elif self.dataType == GraphType.ITERATION:
            self.graph.draw_iteration(self.data,
                self.applicationView.settings.chaos01ColorDeterminism.get_hex(),
                self.applicationView.settings.chaos01ColorChaotic.get_hex())
        #elif self.dataType == GraphType.KVALUES:
        #    self.graph.draw_course_of_K_values(self.data)
        
        self.canvas.draw()

    def is_string_numeric_and_not_empty(self, string: str) -> bool:
        if string:
            if string.isnumeric():
                return True
        return False

    def __calculate_chaos01(self, function: MethodType, *args): #button: Button, returnData: list, 
        self.data = function(*args)
        self.draw()
        self.buttonCalculateAndShow.configure(state=ACTIVE)
        self.buttonCalculateAndShow["text"] = "Calculate and show on graph"
        

    def __calculate_and_show_graph(self) -> None:
        skipStr = self.entrySkip.get()
        cutStr = self.entryCut.get()

        if self.is_string_numeric_and_not_empty(skipStr):
            print("set skip")
            self.chaos01.set_skip(int(skipStr))

        if self.is_string_numeric_and_not_empty(cutStr):
            print("set cut")
            self.chaos01.set_cut(int(cutStr))

        selection = self.comboboxFunctionType.get()
        if (not (selection and not selection.isspace())):
            return

        if selection == "Load from file":
            filename = self.comboboxFileName.get()
            if (not (filename and not filename.isspace())):
                return

            selectedParameter = self.comboboxSelectedParameter.get()
            if (not (selectedParameter and not selectedParameter.isspace())):
                return

            if selectedParameter in self.dataDict:
                self.set_data_type(GraphType.ITERATION)

                self.buttonCalculateAndShow.configure(state=DISABLED)
                self.buttonCalculateAndShow["text"] = "Data are calculating..."
                #self.data = Chaos01.execute_for_iteration(self.chaos01, self.dataDict[selectedParameter])
                #Thread(target=Chaos01View.__calculate_chaos01, args=(self.buttonCalculateAndShow, self.data, Chaos01.execute_for_iteration, self.chaos01, self.dataDict[selectedParameter],)).start()
                Thread(target=self.__calculate_chaos01, args=(Chaos01.execute_for_iteration, self.chaos01, self.dataDict[selectedParameter],)).start()

                self.graph.figName = "Hopfield Network - Iteration over history with Chaos01"

                #self.draw()
                self.graph.refresh()
            return

        self.set_data_type(GraphType.BIFURCATION)

        self.buttonCalculateAndShow.configure(state=DISABLED)
        self.buttonCalculateAndShow["text"] = "Data are calculating..."
        #self.data = Chaos01.execute_for_bifurcation_diagram(self.chaos01, self.function)
        #Thread(target=Chaos01View.__calculate_chaos01, args=(self.buttonCalculateAndShow, self.data, Chaos01.execute_for_bifurcation_diagram, self.chaos01, self.function,)).start()
        Thread(target=self.__calculate_chaos01, args=(Chaos01.execute_for_bifurcation_diagram, self.chaos01, self.function,)).start()

        self.graph.figName = self.function.get_name()
        
        #self.draw()
        self.graph.refresh()

    def __show_graph_of_chaos(self) -> None:
        if not self.data:
            return

        selection = self.comboboxFunctionType.get()
        if (not (selection and not selection.isspace())):
            return

        #self.set_data_type(self.dataTypePom)
        #self.dataType = GraphType(self.data["dataType"]) if "dataType" in self.data else GraphType.BIFURCATION if selection != "Load from file" else GraphType.ITERATION
        self.draw()

    def __show_graph_course_of_K_values(self) -> None:
        self.graph.refresh()
        self.graph.draw_course_of_K_values(self.data)
        self.canvas.draw()
        #self.set_data_type(GraphType.KVALUES)
        #self.draw()

    def __show_import_menu(self) -> None:
        if self.windowHandler.exists(self.importView):
            return

        path = self.applicationView.settings.pathMain + "/" + self.applicationView.settings.pathChaos01 + "/"
        self.importView = ImportView(self, path, "Chaos01 data")
        self.windowHandler.register(self.importView)

    def __show_export_fast_menu(self) -> None:
        if self.windowHandler.exists(self.exportView):
            return

        transferObject = Chaos01TransferObject(self.data, self.function.get_name(), self.dataType)

        path = self.applicationView.settings.pathMain + "/" + self.applicationView.settings.pathChaos01 + "/"
        self.exportView = ExportView(self, transferObject, path, "main of the Chaos01 data")
        self.windowHandler.register(self.exportView)

    def __show_export_full_menu(self) -> None:
        if self.windowHandler.exists(self.exportView):
            return

        transferObject = Chaos01TransferObject(self.data, self.function.get_name(), self.dataType, False)

        path = self.applicationView.settings.pathMain + "/" + self.applicationView.settings.pathChaos01 + "/"
        self.exportView = ExportView(self, transferObject, path, "all of the Chaos01 data")
        self.windowHandler.register(self.exportView)

    def set_import_data(self, data: dict) -> None:
        super().set_import_data(data)

        if self._importData is None:
            return

        self.data, functionName, dataType = Chaos01TransferObject.set_by_dict(self._importData)
        self.set_data_type(GraphType(dataType))

        if self.dataType == GraphType.BIFURCATION:
            self.function = FunctionSelection.GetByName(functionName)
            self.graph.figName = self.function.get_name()
        elif self.dataType == GraphType.ITERATION:
            self.graph.figName = ""
        
        self.draw()

    def on_closing(self) -> None:
        self.graph.close()
        super().on_closing()
        self.applicationView.chaos01View = None