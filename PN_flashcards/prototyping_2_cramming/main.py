#!/usr/bin/env python3
'''
Author: Jerry Xie

Created on: May 16, 2019

Last modified by: Jerry Xie @ May 30, 2019

Effect: Set environment variables; start the app's GUI

'''
from mainViewController import *
import tkinter.filedialog
from tkinter import *
from NP_Service import *
from NPexception import *
try:
    root_window = Tk()
    root_window.title("NP Trainer")
    root_window.geometry("500x500")
    Got_a_path = False
    while True:
        root_window.update()
        working_path = filedialog.askdirectory(
            parent=root_window, 
            initialdir=os.getcwd(), 
            title='Choose a directory where you put your photos into')
        if working_path:
            try:
                NP_Service.instance().set_working_path(working_path)
                Got_a_path = True
                break
            except Not_a_Dir as e:
                print("The working path provided is not a directory")
            except Exception as e:
                print(e)
        else:
            break
    if Got_a_path:
        NP_Service.instance().assignments_constructor()
        app = MainViewController(root_window)
        app.show()
except Not_a_Dir as e:
    print("The working path provided is not a directory")
except Index_Out_of_Bound as e:
    print("Assigned index for the directory is out of bound")
except Unset_Directory as e:
    print("Assignment's directory is unset")
except No_More_Assignment_Left as e:
    print("No more assignments can be found")
except Exception as e:
    print("Unhandled exceptions caught " + str(e))
