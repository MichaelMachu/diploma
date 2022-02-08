from tkinter import *
from tkinter import ttk

from GraphicalUserInterface import GraphicalUserInterface
from CellularAutomaton import CellularAutomaton
#import ApplicationView as aw
#from ApplicationView import ApplicationView

class CellularAutomatonView(GraphicalUserInterface):

    def __init__(self, applicationView) -> None: # aw.ApplicationView
        super().__init__(Toplevel(applicationView.mainWindow), 500, 400, "Cellular Automaton settings")
        self.applicationView = applicationView

        self.mainWindow.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.__build()

    def __run(self) -> None:
        """Main method for running a view."""
        pass

    def __build(self) -> None:
        self.frame = Frame(self.mainWindow, bg="#fff") # width=150, height=100
        #frame.grid(column=0, row=0, sticky="n")
        self.frame.pack(side=TOP, fill=None, expand=False, padx=10, pady=10)
        
        self.label_size = Label(self.frame, text="Size (int)", anchor='w')
        self.label_size.grid(column=0, row=0, sticky=W)
        self.entry_size = Entry(self.frame)
        self.entry_size.grid(column=1, row=0, padx=10, pady=5, sticky=W)

        self.label_rule = Label(self.frame, text="Rule (int)", anchor='w')
        self.label_rule.grid(column=0, row=1, sticky=W)
        self.entry_rule = Entry(self.frame)
        self.entry_rule.grid(column=1, row=1, padx=10, pady=5, sticky=W)

        self.label_random = Label(self.frame, text="Random start generation", anchor='w')
        self.label_random.grid(column=0, row=2, sticky=W)
        self.combobox_random = ttk.Combobox(self.frame)
        self.combobox_random['values'] = ("True", "False")
        self.combobox_random['state'] = 'readonly'
        self.combobox_random.set("True")
        self.combobox_random.grid(column=1, row=2, padx=10, pady=5, sticky=W)

        self.label_selection = Label(self.frame, text="Selection (it is set only, if random is False)", anchor='w')
        self.label_selection.grid(column=0, row=3, sticky=W)
        self.combobox_selection = ttk.Combobox(self.frame)
        self.combobox_selection['values'] = ("center", "left", "right")
        self.combobox_selection['state'] = 'readonly'
        self.combobox_selection.set("center")
        self.combobox_selection.grid(column=1, row=3, padx=10, pady=5, sticky=W)

        self.button_create = Button(self.frame, text="Create a new Cellular Automaton", command=self.__create_ca)
        self.button_create.grid(column=0, row=4, columnspan=2, padx=10, pady=5)

    def draw(self) -> None:
        """Drawing method used for canvas"""
        pass

    def __create_ca(self):
        size_str = self.entry_size.get()
        rule_str = self.entry_rule.get()
        if not size_str.isnumeric() or not rule_str.isnumeric():
            return

        size = int(size_str)
        rule = int(rule_str)
        random = self.combobox_random.get() == "True"
        selection = self.combobox_selection.get()

        print(size, rule, random, selection)

        if rule > 256:
            return

        self.cellularAutomaton = CellularAutomaton(size, rule)
        self.cellularAutomaton.generate_start(random, selection)

        self.applicationView.continue_draw = True
        self.applicationView.offsetY = 0
        self.applicationView.canvas.delete("all")
        self.applicationView.draw_ca_step(self.cellularAutomaton.currentState)

        #self.__close_ca_menu()
        #self.ca_menu.quit()
        
        #self.on_closing_ca_menu()
        self.mainWindow.destroy()

    def on_closing(self):
        self.applicationView.is_ca_menu_exists = False
        self.mainWindow.destroy()