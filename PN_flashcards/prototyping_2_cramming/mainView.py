#!/usr/bin/env python3
'''
Author: Jerry Xie
Created on: May 16, 2019
Last modified by: Jerry Xie @ May 30, 2019
Effect: Define tab views in the main window
            i.e. tab/size/style/position/constraints
'''
from tkinter import *
from tkinter.ttk import *
from crammingTabView import *
from crammingTabViewController import *
class MainView(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        self.nb = Notebook(self)
        Grid.rowconfigure(self, 0, weight=1)
        Grid.columnconfigure(self, 0, weight=1)
        self.nb.grid(row=0, column=0, sticky=(N,W,S,E))
        
        self.tab1 = CrammingTabView(self.nb)
        self.nb.add(self.tab1, text="Cram")

    def get_cramming_tab_view(self):
    	return self.tab1
