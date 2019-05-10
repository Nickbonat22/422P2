#!/usr/bin/env python3
'''
CIS 422 Project 1
Author: Jerry Xie
Created on: Apr 14, 2019
Last modified by: Jerry Xie @ Apr 27, 2019
Effect: Define widgets in the log-tab-view
            i.e. size/style/position/constraints
'''
from tkinter import *
# from tkinter.ttk import *

class LogTabView(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.text = Text(self)
        self.scrollb = Scrollbar(self)
        self.export_summary = Button(self, text="Export Summary")
        self.refresh_log = Button(self, text='Refresh')

        self.scrollb.config(command=self.text.yview)
        self.text.config(yscrollcommand=self.scrollb.set)
        
        # self.scrollb.grid(row=0, column=1, sticky=(N,S,W,E))
        self.export_summary.grid(row = 1, column=0, sticky=(N,S,W,E))
        self.refresh_log.grid(row = 1, column=1, sticky=(N,S,W,E))
        self.text.grid(row=0, column=0, columnspan=2, sticky=(N,S,W,E))

        Grid.rowconfigure(self, 0, weight=1)
        Grid.rowconfigure(self, 1, weight=1)
        Grid.columnconfigure(self, 0, weight=1)
        Grid.columnconfigure(self, 1, weight=1)
        self.text.config(state=DISABLED)
    
    def set_text(self, new_text):
        self.text.config(state=NORMAL)
        self.text.delete(1.0, END)
        self.text.edit_reset()
        self.text.insert(END, new_text)
        self.text.config(state=DISABLED)