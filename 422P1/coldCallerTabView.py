#!/usr/bin/env python3
'''
CIS 422 Project 1
Author: Jerry Xie
Created on: Apr 14, 2019
Last modified by: Jerry Xie @ Apr 27, 2019
Effect: Define widgets in the coldCaller-tab-view
            i.e. size/style/position/constraints
'''
from tkinter import *
from tkinter.font import Font
# from tkinter.ttk import *

class ColdCallerTabView(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.label_font = Font(self.master, family='Arial', size=12, weight='bold')
        self.grid(row=0, column=0, sticky=(N,S,E,W))
        self.top_frames = {}
        self.name_labels = {}
        self.portraits_labels = {}
        self.spellings_labels = {}
        self.portraits = {}
        self.good_btns = {}
        self.concern_btns = {}
        self.btns_group = {}

    def _make_portrait_with_name_label(self, parent, rownum, colnum, name, number, portrait_path, spelling):
        Grid.rowconfigure(parent, rownum, weight=1)
        Grid.columnconfigure(parent, colnum, weight=1)

        id = str(rownum) + str(colnum)
        self.top_frames[id] = Frame(parent)
        frame = self.top_frames[id]
        frame.grid(row=rownum, column=colnum, sticky=(N,S,E,W))

        Grid.rowconfigure(frame, 0, weight=1)
        Grid.columnconfigure(frame, 0, weight=1)
        try:
            self.portraits[colnum] = PhotoImage(file=portrait_path)
        except:
            self.portraits[colnum] = PhotoImage(file='Resources/default.png')
        scale_w = 200//self.portraits[colnum].width()
        scale_h = 200//self.portraits[colnum].height()
        self.portraits[colnum].zoom(scale_w, scale_h)
        self.portraits_labels[colnum] = Label(frame, image=self.portraits[colnum])
        self.portraits_labels[colnum].grid(row=0, column=0, sticky=(N, S, E, W), columnspan=2)

        Grid.rowconfigure(frame, 1, weight=1)
        Grid.columnconfigure(frame, 0, weight=1)
        numlabel = Label(frame, text=number)
        numlabel.grid(row=1, column=0, sticky=(N, S, E))
            
        Grid.rowconfigure(frame, 1, weight=1)
        Grid.columnconfigure(frame, 1, weight=1)
        self.name_labels[colnum] = Label(frame, text=name, font=self.label_font)
        self.name_labels[colnum].grid(row=1, column=1, sticky=(N, S, W))

        Grid.rowconfigure(frame, 2, weight=1)
        Grid.columnconfigure(frame, 0, weight=1)
        self.spellings_labels[colnum] = Label(frame, text=spelling, font=self.label_font)
        self.spellings_labels[colnum].grid(row=2, column=0, sticky=(N, E, S, W), columnspan=2)

    
    def _update_portrait_with_name_label(self, rownum, colnum, new_portrait_path = None, new_name = None, new_spelling = None):
        # Could throw, use with try...except
        target_portrait_label = self.portraits_labels[colnum]
        try:
            self.portraits[colnum] = PhotoImage(file=new_portrait_path)
        except:
            self.portraits[colnum] = PhotoImage(file='Resources/default.png')
        target_portrait_label.config(image=self.portraits[colnum])
        if not new_spelling == None:
            target_splling_label = self.spellings_labels[colnum]
            target_splling_label.config(text=new_spelling)
        if not new_name == None:
            target_name_label = self.name_labels[colnum]
            target_name_label.config(text=new_name)
    
    def set_Widgets_top_portrait(self, pos:int, portrait_path = None, name = None, spelling = None):
        # pos should be 0,1,2
        try:
            self._update_portrait_with_name_label(0, pos, portrait_path, name, spelling)
        except KeyError:
            self._make_portrait_with_name_label(self, 0, pos, name, str(pos + 1) + ': ', portrait_path, spelling)

    def _create_btns_group_to(self, parent, groupnum, rownum, colnum):
        self.btns_group[groupnum] = Frame(self)
        self.btns_group[groupnum].grid(row=rownum, column=colnum, sticky=(N,S,E,W))
        self.good_btns[groupnum] = Button(self.btns_group[groupnum], text="Remove")
        self.concern_btns[groupnum] = Button(self.btns_group[groupnum], text="Concern")

        self.good_btns[groupnum].grid(row=0, column=0, sticky=(N,S,E,W))
        self.concern_btns[groupnum].grid(row=0, column=1, sticky=(N,S,E,W))
        Grid.rowconfigure(self.btns_group[groupnum], 0, weight=1)
        Grid.columnconfigure(self.btns_group[groupnum], 0, weight=1)
        Grid.columnconfigure(self.btns_group[groupnum], 1, weight=1)
    
    def createWidgets_bottom_Frame(self):
        Grid.rowconfigure(self, 1, weight=1)
        Grid.columnconfigure(self, 0, weight=1)
        Grid.columnconfigure(self, 2, weight=1)

        # First student
        self._create_btns_group_to(self, 1, 1, 0)
        # Second student
        self._create_btns_group_to(self, 2, 1, 1)
        # Third student
        self._create_btns_group_to(self, 3, 1, 2)