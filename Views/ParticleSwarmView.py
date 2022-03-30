from tkinter import *
from tkinter import ttk
from types import MethodType
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

from Bases.ViewBase import ViewBase
from . import ApplicationView
from Domain.BiologicallyInspiredAlgorithms.Graph import Graph
from Domain.BiologicallyInspiredAlgorithms.TestFunctions import TestFunctions
from Domain.BiologicallyInspiredAlgorithms.ParticleSwarm import ParticleSwarm
from Domain.Settings import Settings
from .ImportView import ImportView
from .ExportView import ExportView
from Data.ParticleSwarmTransferObject import ParticleSwarmTransferObject
from Data.DataProcess import DataProcess

from EnumTypes.GraphType import GraphType

class ParticleSwarmView(ViewBase):

    def __init__(self, applicationView: ApplicationView) -> None:
        super().__init__(Toplevel(applicationView.mainWindow), 900, 600, "Particle Swarm", applicationView.windowHandler)
        self.applicationView = applicationView

        self.particleSwarm = ParticleSwarm()
        self.graph = Graph()
        self.bestFound = None
        self.populationHistory = None
        self.animationSpeed = 1

        # Create object variables
        # Frames
        self.frame = None
        self.frameParticleSwarm = None
        self.frameFunction = None
        self.frameCanvas = None
        # Labels
        self.labelParticleSwarm = None
        self.labelPopulationSize = None
        self.labelConstant1 = None
        self.labelConstant2 = None
        self.labelMaxGenerations = None
        self.labelFunctionType = None
        self.labelDefinition = None
        self.labelFunctionDefinition = None
        self.labelA = None
        self.labelScale = None
        self.labelRangeFrom = None
        self.labelRangeTo = None
        self.labelFileName = None
        # Entries
        self.entryPopulationSize = None
        self.entryConstant1 = None
        self.entryConstant2 = None
        self.entryMaxGenerations = None
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
        self.menuFile.add_command(
            label="Export",
            command=self.__show_export_menu
        )

        self.menu.add_cascade(label="File", menu=self.menuFile)

        # Main frame
        self.frame = Frame(self.mainWindow, bg=self.frameBG)
        self.frame.pack(side=TOP, fill=BOTH, expand=1, padx=1, pady=1)

        # Particle Swarm
        self.frameParticleSwarm = Frame(self.frame, bg=self.frameBG)
        self.frameParticleSwarm.grid(column=1, row=0, sticky="nsew", padx=(0, 10), pady=10)

        self.labelParticleSwarm = Label(self.frameParticleSwarm, text="Particle Swarm", anchor='w', bg=self.frameBG)
        self.labelParticleSwarm.grid(column=0, row=0, sticky=W, pady=(10, 0))

        self.labelPopulationSize = Label(self.frameParticleSwarm, text="Size of population (int)", anchor='w', bg=self.frameBG)
        self.labelPopulationSize.grid(column=0, row=1, sticky=W)
        self.entryPopulationSize = Entry(self.frameParticleSwarm)
        self.entryPopulationSize.grid(column=1, row=1, padx=10, pady=5, sticky=W)

        self.labelConstant1 = Label(self.frameParticleSwarm, text="C1 constant for vector v (float)", anchor='w', bg=self.frameBG)
        self.labelConstant1.grid(column=0, row=2, sticky=W)
        self.entryConstant1 = Entry(self.frameParticleSwarm)
        self.entryConstant1.grid(column=1, row=2, padx=10, pady=5, sticky=W)

        self.labelConstant2 = Label(self.frameParticleSwarm, text="C2 constant for vector v (float)", anchor='w', bg=self.frameBG)
        self.labelConstant2.grid(column=0, row=3, sticky=W)
        self.entryConstant2 = Entry(self.frameParticleSwarm)
        self.entryConstant2.grid(column=1, row=3, padx=10, pady=5, sticky=W)

        self.labelMaxGenerations = Label(self.frameParticleSwarm, text="Maximum generations (int)", anchor='w', bg=self.frameBG)
        self.labelMaxGenerations.grid(column=0, row=4, sticky=W)
        self.entryMaxGenerations = Entry(self.frameParticleSwarm)
        self.entryMaxGenerations.grid(column=1, row=4, padx=10, pady=5, sticky=W)

        self.labelFunctionType = Label(self.frameParticleSwarm, text="Type of test function", anchor='w', bg=self.frameBG)
        self.labelFunctionType.grid(column=0, row=5, padx=5, pady=10, sticky=W)
        self.comboboxFunctionType = ttk.Combobox(self.frameParticleSwarm)
        self.comboboxFunctionType["values"] = ("sphere", "schwefel", "rosenbrock", "rastrigin", "griewank", "levy", "michalewicz", "zakharov", "ackley")
        self.comboboxFunctionType["state"] = "readonly"
        self.comboboxFunctionType.set("sphere")
        self.comboboxFunctionType.grid(column=1, row=5, padx=0, pady=10, sticky=W)

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
        self.buttonCalculateAndShow = Button(self.frameParticleSwarm, text="Calculate and show on graph", command=self.__calculate_and_show_graph)
        self.buttonCalculateAndShow.grid(column=0, row=6, padx=5, pady=5)
        
        self.buttonReplayAnimation = Button(self.frameParticleSwarm, text="Replay animation", command=self.__replay_animation)
        self.buttonReplayAnimation.grid(column=1, row=6, padx=5, pady=5)
        

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

    def draw(self) -> None:
        self.graph.refresh()
        self.graph.ShowByPopulation(self.bestFound, self.populationHistory, self.animationSpeed)
        self.canvas.draw()

    def is_string_numeric_and_not_empty(self, string: str) -> bool:
        if string:
            if string.isnumeric():
                return True
        return False

    def __calculate_and_show_graph(self) -> None:
        populationSizeStr = self.entryPopulationSize.get()
        constant1Str = self.entryConstant1.get()
        constant2Str = self.entryConstant2.get()
        maxGenerationsStr = self.entryMaxGenerations.get()

        if not populationSizeStr.isnumeric() or not constant1Str.isnumeric() or not constant2Str.isnumeric() or not maxGenerationsStr.isnumeric():
            return

        selection = self.comboboxFunctionType.get()
        if (not (selection and not selection.isspace())):
            return

        self.particleSwarm.pop_size = int(populationSizeStr)
        self.particleSwarm.c_1 = float(constant1Str)
        self.particleSwarm.c_2 = float(constant2Str)
        self.particleSwarm.M_max = int(maxGenerationsStr)

        function, interval = TestFunctions.GetByName(selection)

        self.graph.func = function
        self.graph.interval = interval

        self.bestFound, self.populationHistory = self.particleSwarm.execute(2, interval, function)

        self.graph.figName = selection
        self.draw()

    def __replay_animation(self) -> None:
        if not self.populationHistory:
            return

        self.draw()

    def __show_import_menu(self) -> None:
        if self.windowHandler.exists(self.importView):
            return

        path = self.applicationView.settings.pathMain + "/" + self.applicationView.settings.pathParticleSwarm + "/"
        self.importView = ImportView(self, path, "Particle Swarm data")
        self.windowHandler.register(self.importView)

    def __show_export_menu(self) -> None:
        if self.windowHandler.exists(self.exportView):
            return

        transferObject = ParticleSwarmTransferObject(self.particleSwarm)

        path = self.applicationView.settings.pathMain + "/" + self.applicationView.settings.pathParticleSwarm + "/"
        self.exportView = ExportView(self, transferObject, path, "Particle Swarm data")
        self.windowHandler.register(self.exportView)

    def set_import_data(self, data: dict) -> None:
        super().set_import_data(data)

        if self._importData is None:
            return

        transferObject = ParticleSwarmTransferObject.set_by_dict(self._importData)
        
        self.particleSwarm.pop_size = transferObject.populationSize
        self.particleSwarm.c_1 = transferObject.c1
        self.particleSwarm.c_2 = transferObject.c2
        self.particleSwarm.M_max = transferObject.maxGeneration

        self.populationHistory = transferObject.history

        self.draw()

    def on_closing(self) -> None:
        self.graph.close()
        super().on_closing()
        self.applicationView.chaos01View = None