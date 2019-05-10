#!/usr/bin/env python3
'''
Author: Jerry Xie

Created on: Apr 5, 2019

Last modified by: Jerry Xie @ Apr 27, 2019

Effect: Set environment variables; start the app's GUI

'''
from tkinter import *
from mainViewController import MainViewController
import student_queue
import IOService
from os import getenv, path
student_queue.REINSERTION_AFTER_FIRST_N_PERCENT = 50
IOService.DELIM = '\t'

MainViewController.CONCERN_1A = 'c'
MainViewController.CONCERN_1B = 'v'
MainViewController.CONCERN_2 = 'b'
MainViewController.CONCERN_3 = 'n'
MainViewController.CONCERN_4 = 'm'
MainViewController.REMOVE_1A = '1'
MainViewController.REMOVE_1B = '<space>'
MainViewController.REMOVE_2 = '2'
MainViewController.REMOVE_3 = '3'

app = MainViewController()
app.show()

