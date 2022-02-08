#import tkinter as tk
from tkinter import *
from tkinter import ttk

from numpy.lib.function_base import select
from CellularAutomaton import CellularAutomaton

class Gui():
    
    def __init__(self) -> None:
        self.root = Tk()
        self.root.minsize(600, 500)
        self.root.title("Systems at the edge of chaos by Michael Machů")
        self.root.configure(background='#ababab')
        #self.frame = Frame(self.root, padx=10, pady=10, width=600, height=600)
        #self.frame.pack(expand=True, fill="both")
        #self.frame.pack_propagate(0)
        #self.frame.grid_propagate(0)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing_root)

        self._is_ca_menu_exists = False
        self._is_animation_running = False
        self.continue_draw = False

        self.cellularAutomaton = None
        self.offsetY = 0

        self.__build()
        self.__run()

    def __run(self) -> None:
        self.root.mainloop()

    def __build(self) -> None:
        #self.frame.grid()

        self.frame_right = Frame(self.root, width=150, height=100, bg="#ababab")
        self.frame_right.grid(column=1, row=0, sticky="nsew")
        #self.button = Button(self.frame_right, text="Quit", command=self.root.destroy)
        #self.button.pack()

        self.button_ca = Button(self.frame_right, text="Cellular Automaton", command=self.__show_cellular_automaton_menu)
        self.button_ca.pack(fill='x')

        self.button_anim = Button(self.frame_right, text="Start animation", command=self.__draw)
        self.button_anim.pack(fill='x')

        self.button_anim_pause = Button(self.frame_right, text="Pause animation", command=self.pause_animation)
        self.button_anim_pause.pack(fill='x')

        self.button_anim_pause = Button(self.frame_right, text="Continue animation", command=self.continue_animation)
        self.button_anim_pause.pack(fill='x')


        self.frame_canvas = Frame(self.root, bg="#ababab")
        self.frame_canvas.grid(column=0, row=0, sticky="nsew")
        self.frame_canvas.grid_rowconfigure(0, weight=1)
        self.frame_canvas.grid_columnconfigure(0, weight=1)

        self.canvas = Canvas(self.frame_canvas, bg="#fff") # scrollregion=(0,0,500,500)
        self.canvas.grid(column=0, row=0, sticky="nsew")

        # Link a scrollbar to the canvas
        vsb = Scrollbar(self.frame_canvas, orient="vertical", command=self.canvas.yview)
        vsb.grid(row=0, column=1, sticky='ns')
        self.canvas.configure(yscrollcommand=vsb.set)
        """
        #canvas=Canvas(frame,bg='#FFFFFF',width=300,height=300,scrollregion=(0,0,500,500))
        hbar=Scrollbar(self.root,orient=HORIZONTAL)
        hbar.pack(side=BOTTOM,fill=X)
        hbar.config(command=self.canvas.xview)
        vbar=Scrollbar(self.root,orient=VERTICAL)
        vbar.pack(side=RIGHT,fill=Y)
        vbar.config(command=self.canvas.yview)
        self.canvas.config(width=300,height=300)
        self.canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        #canvas.pack(side=LEFT,expand=True,fill=BOTH)
        """

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        """self.label = Label(self.frame, text="Hello World!").grid(column=1, row=1)
        self.button = Button(self.frame, text="Quit", command=self.root.destroy).grid(column=1, row=0)
        self.canvas = Canvas(self.frame).grid(column=0, row=1, sticky="nsew")"""

    def __show_cellular_automaton_menu(self):
        #if self.ca_menu is not None:
        #    if self.ca_menu.winfo_exists():
        #        return

        if self._is_ca_menu_exists:
            return

        self._is_ca_menu_exists = True
        
        self.ca_menu = Toplevel()
        self.ca_menu.title("Cellular Automaton settings")
        self.ca_menu.configure(background='#ababab')
        #self.ca_menu.geometry("200x100")
        self.ca_menu.minsize(500, 400)
        self.ca_menu.maxsize(500, 400)
        self.ca_menu.protocol("WM_DELETE_WINDOW", self.on_closing_ca_menu)
        
        frame = Frame(self.ca_menu, bg="#fff") # width=150, height=100
        #frame.grid(column=0, row=0, sticky="n")
        frame.pack(side=TOP, fill=None, expand=False, padx=10, pady=10)
        
        label_size = Label(frame, text="Size (int)", anchor='w')
        label_size.grid(column=0, row=0, sticky=W)
        self.entry_size = Entry(frame)
        self.entry_size.grid(column=1, row=0, padx=10, pady=5, sticky=W)

        label_rule = Label(frame, text="Rule (int)", anchor='w')
        label_rule.grid(column=0, row=1, sticky=W)
        self.entry_rule = Entry(frame)
        self.entry_rule.grid(column=1, row=1, padx=10, pady=5, sticky=W)

        label_random = Label(frame, text="Random start generation", anchor='w')
        label_random.grid(column=0, row=2, sticky=W)
        self.combobox_random = ttk.Combobox(frame)
        self.combobox_random['values'] = ("True", "False")
        self.combobox_random['state'] = 'readonly'
        self.combobox_random.set("True")
        self.combobox_random.grid(column=1, row=2, padx=10, pady=5, sticky=W)

        label_selection = Label(frame, text="Selection (it is set only, if random is False)", anchor='w')
        label_selection.grid(column=0, row=3, sticky=W)
        self.combobox_selection = ttk.Combobox(frame)
        self.combobox_selection['values'] = ("center", "left", "right")
        self.combobox_selection['state'] = 'readonly'
        self.combobox_selection.set("center")
        self.combobox_selection.grid(column=1, row=3, padx=10, pady=5, sticky=W)

        button_create = Button(frame, text="Create a new Cellular Automaton", command=self.__create_ca)
        button_create.grid(column=0, row=4, columnspan=2, padx=10, pady=5)


        #self.ca_menu.grid_rowconfigure(0, weight=1, minsize=200)
        #self.ca_menu.grid_columnconfigure(0, weight=1, minsize=100)
        

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

        self.continue_draw = True
        self.offsetY = 0
        self.canvas.delete("all")
        self.__draw_ca_step(self.cellularAutomaton.currentState)

        #self.__close_ca_menu()
        #self.ca_menu.quit()
        self.on_closing_ca_menu()

    def __draw_ca_step(self, step):
        offsetX = 0
        for item in step:
            if item == 1:
                self.canvas.create_rectangle(0 + offsetX, 0 + self.offsetY, 10 + offsetX, 10 + self.offsetY, outline="#000", fill="#000")
            offsetX += 10

    def __draw(self) -> None:
        #if self._is_animation_running:
        #    return

        if self.cellularAutomaton is not None:
            step = self.cellularAutomaton.execute()
            self.offsetY += 10
            self.__draw_ca_step(step)
            #self.canvas.yview_scroll(offsetY, 'units')
            #self.canvas.configure(scrollregion=(0,0,500,500))
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            
            if self.continue_draw:
                self.root.after(100, self.__draw)

    def pause_animation(self):
        self.continue_draw = False

    def continue_animation(self):
        self.continue_draw = True
        self.root.after(100, self.__draw)

    def on_closing_root(self):
        #self.__close_ca_menu()
        #self.__close_root()

        #if self.ca_menu is not None:
        if self._is_ca_menu_exists:
            self.ca_menu.quit()
        self.root.quit()

    def on_closing_ca_menu(self):
        if self._is_ca_menu_exists:
            self._is_ca_menu_exists = False
            #self.ca_menu.quit()
            self.ca_menu.destroy()

    """
    def __close_root(self):
        if self.root.winfo_exists():
            self.root.destroy()

    def __close_ca_menu(self):
        if self.ca_menu.winfo_exists():
            self.ca_menu.destroy()
    """