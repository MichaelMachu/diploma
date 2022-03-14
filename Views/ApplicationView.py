#import tkinter as tk
from tkinter import *

from click import command

from Domain.AnimationSettings import AnimationSettings

from Interfaces.GraphicalUserInterface import GraphicalUserInterface
from .CellularAutomatonView import CellularAutomatonView
from .AnimationSettingsView import AnimationSettingsView
from .SaveCellularAutomatonView import SaveCellularAutomatonView
from .HopfieldNetworkView import HopfieldNetworkView

class ApplicationView(GraphicalUserInterface):
    
    def __init__(self) -> None:
        """The main thread of the application"""
        super().__init__(Tk(), 600, 500, "Systems at the edge of chaos by Michael Machů")
        self.root = self.mainWindow
        
        # Singletons objects
        self.animationSettings = AnimationSettings()
        self.cellularAutomaton = None
        self.cellularAutomatonView = None
        self.animationSettingsView = None
        self.saveCellularAutomatonView = None
        self.hopfieldNetworkView = None

        self.testCa = None

        # Control parameters
        self.isCaMenuExists = False
        self.isAnimationSettingsExists = False
        self.isSaveCaExists = False
        self.isAnimationRunning = False
        self.isHopfieldNetworkExists = False
        self.continueDraw = False

        self.world = [] # World for 2D

        # Y offset used as history for 1 dimensional Cellular Automaton
        self.offsetY = 0

        self.__build()
        self.__run()

    def __run(self) -> None:
        self.root.mainloop()

    def __build(self) -> None:
        # Top menu
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)
        self.menuModules = Menu(self.menu, tearoff=False)
        self.menuModules.add_command(
            label="Hopfield Network",
            command=self.__show_hopfield_network
        )
        self.menu.add_cascade(label="Modules", menu=self.menuModules)

        # Right menu
        self.frameRight = Frame(self.root, width=150, height=100, bg="#ababab")
        self.frameRight.grid(column=1, row=0, sticky="nsew")

        self.frameRight.rowconfigure(0, weight=1)
        self.frameRight.rowconfigure(1, weight=1)

        # Split right menu into two separate menus - upper and lower.
        self.frameSplitUpper = Frame(self.frameRight, width=150, height=100, bg="#ababab")
        self.frameSplitUpper.grid(column=0, row=0, sticky="nsew")

        self.frameSplitLower = Frame(self.frameRight, width=150, height=100, bg="#ababab")
        self.frameSplitLower.grid(column=0, row=1, sticky="nsew")

        # Buttons
        self.buttonAnimationSettings = Button(self.frameSplitUpper, text="Animation settings", command=self.__show_animation_settings_menu)
        self.buttonAnimationSettings.pack(fill='x')

        self.buttonCa = Button(self.frameSplitUpper, text="Cellular Automaton", command=self.__show_cellular_automaton_menu)
        self.buttonCa.pack(fill='x')

        self.buttonCaSave = Button(self.frameSplitUpper, text="Save Cellular Automaton", command=self.__show_save_cellular_automaton_menu)
        self.buttonCaSave.configure(state=DISABLED)
        self.buttonCaSave.pack(fill='x')

        self.buttonAnim = Button(self.frameSplitLower, text="Start animation", command=self.start_draw)
        self.buttonAnim.configure(state=DISABLED)
        self.buttonAnim.pack(fill='x')

        self.buttonAnimPause = Button(self.frameSplitLower, text="Pause animation", command=self.pause_animation)
        self.buttonAnimPause.configure(state=DISABLED)
        self.buttonAnimPause.pack(fill='x')

        self.buttonAnimContinue = Button(self.frameSplitLower, text="Continue animation", command=self.continue_animation)
        self.buttonAnimContinue.configure(state=DISABLED)
        self.buttonAnimContinue.pack(fill='x')

        # Canvas
        self.frameCanvas = Frame(self.root, bg="#ababab")
        self.frameCanvas.grid(column=0, row=0, sticky="nsew")
        self.frameCanvas.grid_rowconfigure(0, weight=1)
        self.frameCanvas.grid_columnconfigure(0, weight=1)

        self.canvas = Canvas(self.frameCanvas, bg="#fff")
        self.canvas.grid(column=0, row=0, sticky="nsew")

        # Link a scrollbar to the canvas
        self.scrollbarVerticalCanvas = Scrollbar(self.frameCanvas, orient="vertical", command=self.canvas.yview)
        self.scrollbarVerticalCanvas.grid(row=0, column=1, sticky='ns')
        self.canvas.configure(yscrollcommand=self.scrollbarVerticalCanvas.set)

        self.scrollbarHorizontalCanvas = Scrollbar(self.frameCanvas, orient="horizontal", command=self.canvas.xview)
        self.scrollbarHorizontalCanvas.grid(row=1, column=0, sticky='ew')
        self.canvas.configure(xscrollcommand=self.scrollbarHorizontalCanvas.set)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
    # Other windows for specific configuration
    def __show_animation_settings_menu(self) -> None:
        if self.isAnimationSettingsExists:
            return

        self.isAnimationSettingsExists = True
        self.animationSettingsView = AnimationSettingsView(self)

    def __show_cellular_automaton_menu(self) -> None:
        if self.isCaMenuExists:
            return

        self.isCaMenuExists = True
        self.cellularAutomatonView = CellularAutomatonView(self)

    def __show_save_cellular_automaton_menu(self) -> None:
        if self.isSaveCaExists:
            return

        self.isSaveCaExists = True
        self.saveCellularAutomatonView = SaveCellularAutomatonView(self)
    
    def __show_hopfield_network(self) -> None:
        if self.isHopfieldNetworkExists:
            return

        self.isHopfieldNetworkExists = True
        self.hopfieldNetworkView = HopfieldNetworkView(self)

    def create_world(self) -> None:
        if self.cellularAutomatonView.cellularAutomaton.dimension == 2:
            self.offsetY = 0
            for y in range(self.cellularAutomatonView.cellularAutomaton.size[0]):
                color = self.animationSettings.color.get_colors_by_K(self.cellularAutomatonView.cellularAutomaton.K - 1)
                offsetX = 0
                self.world.append([])
                for x in range(self.cellularAutomatonView.cellularAutomaton.size[1]):
                    item = self.canvas.create_rectangle(
                        0 + offsetX, 0 + self.offsetY, 
                        self.animationSettings.cellSize + offsetX, self.animationSettings.cellSize + self.offsetY, 
                        #outline=color[x - 1], fill=color[x - 1]
                        outline="#ffffff", fill="#ffffff"
                    )
                    self.world[y].append(item)
                    offsetX += self.animationSettings.cellSize
                self.offsetY += self.animationSettings.cellSize

    # Draw and animation methods
    def start_draw(self) -> None:
        self.buttonAnim.configure(state=DISABLED)
        self.buttonAnimPause.configure(state=ACTIVE)
        self.buttonAnimContinue.configure(state=ACTIVE)

        self.animationSettings.color.get_colors_by_K(self.cellularAutomatonView.cellularAutomaton.K - 1, True)

        self.continueDraw = True
        self.draw()

    def re_draw(self) -> None:
        """Clears the whole canvas and do redrawing based on the history"""
        if self.cellularAutomatonView is None:
            print("CA view not exists")
            return

        if self.cellularAutomatonView.cellularAutomaton is None:
            print("CA not exists")
            return

        self.continueDraw = False
        self.offsetY = 0
        self.canvas.delete("all")

        if self.cellularAutomatonView.cellularAutomaton.dimension == 2:
            self.world = []
            self.create_world()
            self.draw_step(self.cellularAutomatonView.cellularAutomaton.currentState)
            #for step in self.cellularAutomatonView.cellularAutomaton.currentState:
            #    self.draw_step(step)
        else:
            for step in self.cellularAutomatonView.cellularAutomaton.cellHistory:
                self.draw_step(step)

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def draw_step(self, step: list) -> None:
        if self.cellularAutomatonView.cellularAutomaton.dimension == 2:
            self.__draw_step_2D(step)
            return
        
        offsetX = 0
        for item in step:
            color = self.animationSettings.color.get_colors_by_K(self.cellularAutomatonView.cellularAutomaton.K - 1)
            
            # if cell is not in a state of "death" then draw state by color
            if item > 0:
                self.canvas.create_rectangle(
                    0 + offsetX, 0 + self.offsetY, 
                    self.animationSettings.cellSize + offsetX, self.animationSettings.cellSize + self.offsetY, 
                    outline=color[item - 1], fill=color[item - 1]
                )
            offsetX += self.animationSettings.cellSize
        self.offsetY += self.animationSettings.cellSize

    def __draw_step_2D(self, step: list) -> None:
        #offsetX = 0
        #print(self.world)
        for y in range(len(step)):
            for x in range(len(step[y])):
                item = step[y][x]
                color = "#ffffff" if item == 0 else self.animationSettings.color.get_colors_by_K(self.cellularAutomatonView.cellularAutomaton.K - 1)[item - 1]
                
                # if cell is not in a state of "death" then draw state by color
                #if x > 0:
                
                #print(self.world[y][x], y, x, item, color)
                    #self.canvas.create_rectangle(
                    #    0 + offsetX, 0 + self.offsetY, 
                    #    self.animationSettings.cellSize + offsetX, self.animationSettings.cellSize + self.offsetY, 
                    #    outline=color[item - 1], fill=color[item - 1]
                    #)
                self.canvas.itemconfig(self.world[y][x], outline=color, fill=color)#color[item]
                #offsetX += self.animationSettings.cellSize
            #self.offsetY += self.animationSettings.cellSize

    def draw(self) -> None:
        if self.cellularAutomatonView.cellularAutomaton is not None:
            step = self.cellularAutomatonView.cellularAutomaton.execute()
            self.draw_step(step)
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            
            if self.continueDraw:
                self.root.after(100, self.draw)

    def pause_animation(self) -> None:
        self.continueDraw = False

    def continue_animation(self) -> None:
        if not self.continueDraw:
            self.continueDraw = True
            self.root.after(100, self.draw)

    def on_closing_root(self) -> None:
        if self.isCaMenuExists:
            self.cellularAutomatonView.mainWindow.quit()
        self.root.quit()

    def on_closing_ca_menu(self) -> None:
        if self.isCaMenuExists:
            self.isCaMenuExists = False
            self.cellularAutomatonView.mainWindow.destroy()