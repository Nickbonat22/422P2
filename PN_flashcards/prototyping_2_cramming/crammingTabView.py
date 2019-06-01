#!/usr/bin/env python3
'''
Authors: Nicholas Bonat, Jerry Xie

Created on: May 16, 2019

Last modified by: Jerry Xie @ May 30, 2019

Effect: Defined the widgets' position and other view properties

'''
from tkinter import *
from tkinter.font import Font

class CrammingTabView(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid(row=0, column=0, sticky=(N,S,E,W))
        
        self.label_font = Font(self.master, family='Arial', size=12)
        self.btns_frame = Frame(self)
        self.good_btn = Button(self.btns_frame, text="Good", bg='green', highlightbackground='green')
        self.reset_btn = Button(self.btns_frame, text="Try again", bg='blue', highlightbackground='blue')
        self.forgot_btn = Button(self.btns_frame, text="Forgot", bg='red', highlightbackground='red')
        
        self.label_frame = Frame(self)
        self.portrait_label = Label(self.label_frame, wraplengt=200)
        self.name_label = Label(self.label_frame, text="Name's Label", font=self.label_font, wraplengt=200)
        self.memo_label = Label(self.label_frame, text="Memo's Label", font=self.label_font, wraplengt=200)

        self._config_btns()
        self._config_portrait_with_label()

    def _config_btns(self):
        Grid.rowconfigure(self, 1, weight=1)
        Grid.columnconfigure(self, 0, weight=1)
        self.btns_frame.grid(row=2, column=0, sticky=(N,S,E,W))
        
        Grid.rowconfigure(self.btns_frame, 0, weight=1)
        Grid.columnconfigure(self.btns_frame, 0, weight=1)
        Grid.columnconfigure(self.btns_frame, 1, weight=1)
        Grid.columnconfigure(self.btns_frame, 2, weight=1)
        self.forgot_btn.grid(row=0, column=0,sticky=(N,S,E,W))
        self.reset_btn.grid(row=0, column=1, sticky=(N,S,E,W))
        self.good_btn.grid(row=0, column=2,sticky=(N,S,E,W))
        
        self.reset_btn.grid_remove()
        self.btns_frame.grid_remove()


    def _config_portrait_with_label(self):
        Grid.rowconfigure(self, 0, weight=1)
        Grid.rowconfigure(self, 1, weight=1)
        Grid.columnconfigure(self, 0, weight=1)
        self.label_frame.grid(row=0, column=0, rowspan=2, sticky=(N,S,E,W))
        
        Grid.rowconfigure(self.label_frame, 0, weight=1)
        Grid.rowconfigure(self.label_frame, 1, weight=1)
        Grid.rowconfigure(self.label_frame, 2, weight=1)
        Grid.columnconfigure(self.label_frame, 1, weight=1)
        self.portrait_label.grid(row=0, column=1,sticky=(N,S,E,W))
        self.name_label.grid(row=1, column=1,sticky=(N,S,E,W))
        self.memo_label.grid(row=2, column=1,sticky=(N,S,E,W))

        self.name_label.grid_remove()
        self.memo_label.grid_remove()