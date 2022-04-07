import os
import tkinter as tk
from pyparsing import col
from ttkthemes import ThemedTk
from tkinter import DISABLED, ttk, LEFT, Button, NORMAL
from model.agent import Agent
import platform

WIDTH = 230
HEIGHT = 220
class MainFrame():

    def __init__(self, agent: Agent) -> None:
        self.__agent = agent
        
        self.__root = ThemedTk(theme='breeze')
        self.__root.title("Connect 4 | Control Panel")
        self.__root.geometry(str(WIDTH)+'x'+str(HEIGHT))
        
        # set driver for pygame
        self.__embed = tk.Frame(self.__root,width= WIDTH, height= HEIGHT)
        self.__embed.pack(side = LEFT) #packs window to the left

        os.environ['SDL_WINDOWID'] = str(self.__embed.winfo_id())
        if platform.system == "Windows":
            os.environ['SDL_VIDEODRIVER'] = str(self.__embed.winfo_id())
        self.__embed.grid(columnspan = (600), rowspan = 600) # Adds grid

        self.setup()

    def update(self):
        self.__root.update()

    def alpha_beta_pruning(self):
        return self.__alpha_beta_var.get() == '1'

    def show_tree(self):
        self.__show_tree_btn['text'] = "Loading Tree..."
        self.__show_tree_btn['state'] = DISABLED
        self.__agent.tree_to_svg()
        self.__show_tree_btn['state'] = NORMAL
        self.__show_tree_btn['text'] = "Export Tree SVG"

    def print_tree(self):
        self.__print_tree_btn['text'] = "Loading Tree..."
        self.__print_tree_btn['state'] = DISABLED
        self.__agent.print_tree()
        self.__print_tree_btn['state'] = NORMAL
        self.__print_tree_btn['text'] = "Print Tree"


    def setup(self):

        # Creating the widgets
        input_frame = ttk.LabelFrame(self.__root, text="Control", padding=20)

        # alpha beta
        self.__alpha_beta_var = tk.StringVar()
        self.__alpha_beta_check = ttk.Checkbutton(
            input_frame,
            text="Alpha-Beta Pruning",
            variable=self.__alpha_beta_var
        )
        # showing the tree
        self.__show_tree_btn = ttk.Button(
            input_frame,
            text="Export Tree SVG",
            command=self.show_tree
        )
        # print the tree in the console
        self.__print_tree_btn = ttk.Button(
            input_frame,
            text="Print Tree",
            command=self.print_tree
        )

        # time 
        self.__time_lbl = ttk.Label(input_frame, text="")
        self.__score_lbl = ttk.Label(input_frame, text="")

        # Displaying the widgets
        input_frame.grid(column=0, row=0, padx=20, pady=20)

        self.__alpha_beta_check.grid(column=0, row=1, sticky=tk.W)
        self.__show_tree_btn.grid(column=0, row=2,sticky=tk.W)
        self.__print_tree_btn.grid(column=0, row=3,sticky=tk.W)

        self.__time_lbl.grid(column=0, row=4,sticky=tk.W)
        self.__score_lbl.grid(column=0,row = 5, sticky=tk.W)


        self.__root.update()

    def show_time(self):
        self.__time_lbl['text'] = "Time = " + str(round(self.__agent.get_time(),3)) + " second(s)."

    def show_score(self, score):
        self.__score_lbl['text'] = "score = " + str(-1 * score)