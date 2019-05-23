#!/usr/bin/env python3
'''
CIS 422 Project 1
Author: Jerry Xie
Created on: Apr 14, 2019
Last modified by: Jerry Xie @ Apr 27, 2019
Effect: Define widgets in the main window
            i.e. tab/size/style/position/constraints
'''
from tkinter import *
from tkinter.ttk import *
from flashcardTabView import FlashcardTabView
class MainView(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        self.nb = Notebook(self)
        Grid.rowconfigure(self, 0, weight=1)
        Grid.columnconfigure(self, 0, weight=1)
        self.nb.grid(row=0, column=0, sticky=(N,W,S,E))
        
        self.tab1 = FlashcardTabView(self.nb)
        self.nb.add(self.tab1, text="FlashCards")
    
    def get_flashcard_tab_view(self):
        return self.tab1
