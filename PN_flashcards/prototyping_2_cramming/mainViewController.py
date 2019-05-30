#!/usr/bin/env python3
'''
Author: Jerry Xie

Created on: May 16, 2019

Last modified by: Jerry Xie @ May 30, 2019

Effect: Binded global keystrokes and handled tab views' transition logic.

'''
from mainView import *
from NPexception import *
class MainViewController():
    def __init__(self, root_window):
        # The root window
        self.root = root_window
        # Adaptive view setting
        rows = 0
        while rows < 50:
            self.root.rowconfigure(rows, weight=1)
            self.root.columnconfigure(rows, weight=1)
            rows += 1
        
        self.CrammingTabViewControllerDelegate = None
        self.mainView = MainView(self.root, self)
        assert(not self.CrammingTabViewControllerDelegate == None)
        self.mainView.grid(row=0, column=0, columnspan=50, rowspan=50, sticky=(N,W,S,E))
        self.root.bind('<space>', lambda e: self.CrammingTabViewControllerDelegate.switch_flashcard_side())
        self.root.bind('1', lambda e: self.CrammingTabViewControllerDelegate.perform_and_update_info(1))
        self.root.bind('2', lambda e: self.CrammingTabViewControllerDelegate.perform_and_update_info(0))
    def show(self):
        self.root.mainloop()