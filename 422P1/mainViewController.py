#!/usr/bin/env python3
'''
Author: Jerry Xie

Created on: Apr 5, 2019

Last modified by: Jerry Xie @ Apr 27, 2019

Topic: Controller for all Views

Effect: Handle views' intereaction, response logic. 
            i.e. binding functions to buttons

'''
from tkinter import *
import tkinter.filedialog
from MainView import *
from coldCallerTabView import ColdCallerTabView
from coldCallerService import ColdCallerService
from IOService import IO
from student import Student
from logService import getDailyLog, summary

from os import path

# Define keystroke mapping
CONCERN_1A = 'c'
CONCERN_1B = 'v'
CONCERN_2 = 'b'
CONCERN_3 = 'n'
CONCERN_4 = 'm'
REMOVE_1A = '1'
REMOVE_1B = '<space>'
REMOVE_2 = '2'
REMOVE_3 = '3'
# Define Students portrait photos' folder
HOME_PHOTOS_PATH = "Resources/Photos"

class MainViewController():

    def __init__(self):
        # Using num_popup to count how many
        # popup windows do we have
        self.num_popup = 0
        self.aboutme_popup = None
        self.fontsize_popup = None
        self.not_found_popup = None
        self.overwrite_popup = None

        # The root window
        self.root = Tk()
        self.root.title("Cold Caller")
        self.root.geometry("500x500")

        # Adaptive view setting
        rows = 0
        while rows <= 50:
            self.root.rowconfigure(rows, weight=1)
            self.root.columnconfigure(rows, weight=1)
            rows += 1

        # Add MainView Frame into the root window
        self.mainView = MainView(self.root)
        # Let it occupy all the window
        self.mainView.grid(row=0, column=0, columnspan=50, rowspan=50, sticky=(N,W,S,E))
        # Get 2 tab views from the MainView Frame
        self.cold_caller_tab_view = self.mainView.get_cold_caller_tab_view()
        self.log_tab_view = self.mainView.get_log_tab_view()

        # Bind button/keystrokes to Cold Caller Service APIs
        self.cold_caller_tab_view.createWidgets_bottom_Frame()
        self.cold_caller_tab_view.good_btns[1].bind("<Button-1>", lambda e: self.remove(e, 0))
        self.cold_caller_tab_view.concern_btns[1].bind("<Button-1>", lambda e: self.remove(e, 0, True))

        self.cold_caller_tab_view.good_btns[2].bind("<Button-1>", lambda e: self.remove(e, 1))
        self.cold_caller_tab_view.concern_btns[2].bind("<Button-1>", lambda e: self.remove(e, 1, True))

        self.cold_caller_tab_view.good_btns[3].bind("<Button-1>", lambda e: self.remove(e, 2))
        self.cold_caller_tab_view.concern_btns[3].bind("<Button-1>", lambda e: self.remove(e, 2, True))
        # Keystrokes mapping
        global CONCERN_1A, CONCERN_1B, CONCERN_2, CONCERN_3
        global REMOVE_1A, REMOVE_1B, REMOVE_2, REMOVE_3
        self.root.bind(CONCERN_1A, lambda e: self.remove(e, 0, True))
        self.root.bind(CONCERN_1B, lambda e: self.remove(e, 0, True))
        self.root.bind(CONCERN_2, lambda e: self.remove(e, 1, True))
        self.root.bind(CONCERN_3, lambda e: self.remove(e, 2, True))
        self.root.bind(CONCERN_4, lambda e: self.remove(e, 2, True))

        self.root.bind(REMOVE_1A, lambda e: self.remove(e, 0))
        self.root.bind(REMOVE_1B, lambda e: self.remove(e, 0))
        self.root.bind(REMOVE_2, lambda e: self.remove(e, 1))
        self.root.bind(REMOVE_3, lambda e: self.remove(e, 2))

        # Binding buttons in the log-tab-view
        self.log_tab_view.refresh_log.config(command=lambda: self.log_tab_view.set_text(getDailyLog()))
        self.log_tab_view.export_summary.config(command=self.export_summary_file_target_path_with_name)

        # Create the top-bar menu
        self.createMenu()

        # When closing the app, save the queue
        def onclosing():
            IO.instance().set_curr_queue()
            self.root.destroy()
        self.root.protocol('WM_DELETE_WINDOW', onclosing)

        # Call Cold Caller Service to get the first 3 students
        self.update_students_info()
    
    # Update students' portrait photos, names, spelling
    def update_students_info(self):
        f = ColdCallerService.instance()
        for i in range(3):
            new_student = f.get_studnt_at(i)
            if not new_student == None:
                name = ""
                spelling = ""
                photo = None
                # If this student doesn't have privacy protection
                # Show his/her name, photo, spelling
                if new_student.getReveal():
                    global HOME_PHOTOS_PATH
                    name = new_student.getName()
                    spelling = new_student.getPSpell()
                    photo = path.join(HOME_PHOTOS_PATH, new_student.getID() + '.png')
                # Otherwise, only show his/her initials
                else:
                    name = new_student.getNameInitial()
                
                self.cold_caller_tab_view.set_Widgets_top_portrait(i, name=name, spelling=spelling, portrait_path=photo)
    
    # Call cold caller service to remove a student at a certain position
    # and then update the view
    def remove(self, event, pos:int, concern = False):
        if(self.mainView.nb.index("current") == 0 and self.num_popup == 0):
            f = ColdCallerService.instance()
            if(not concern):
                if(f.remove_stuent_at(pos)):
                    self.update_students_info()
            else:
                f.concern_recent_student()
    
    # The following methods are for the use of top-bar menu
    #
    # Destory a popup window after doing a certain job
    def destory_popup_window_after(self, popup, doing_this_before = None):
        if not doing_this_before == None:
            try:
                doing_this_before()
            except Exception as e:
                print(e)
        popup.destroy()
        self.num_popup -= 1
    
    # When importing a roster, if that file is not found
    # fire this window
    def not_found_window(self):
        # If there is an active popup window
        # Foucus on it
        try:
            self.not_found_popup.focus_set()
            return
        except Exception:
            pass
        # Otherwise create a new one
        self.num_popup += 1
        self.not_found_popup = Toplevel(self.root)
        self.not_found_popup.title("File Not Found")
        self.not_found_popup.resizable(0,0)

        explanation = "Unable to open the file you selected"

        onclosing = lambda: self.destory_popup_window_after(self.not_found_popup)
        self.not_found_popup.protocol('WM_DELETE_WINDOW', onclosing)
        Label(self.not_found_popup,text=explanation).grid()
        Button(self.not_found_popup,text='OK',command=onclosing).grid()

        self.not_found_popup.transient(self.root)
        self.mainView.wait_window(self.not_found_popup)
    
    # Call IOService and pass the importing file path to it
    def _import_roster(self, path_with_name):
        IO.instance().importRoster(path_with_name, True)
        self.update_students_info()

    # Display the difference between current roster and the importing roster
    # and ask whether to overwrite the current roster
    def overwrite_window(self, diff, path_with_name):
        try:
            self.overwrite_popup.focus_set()
            return
        except Exception:
            pass
        self.num_popup += 1
        self.overwrite_popup = Toplevel(self.root)
        self.overwrite_popup.title("Overwrite the current roster")
        self.overwrite_popup.resizable(0,0)

        explanation = "Do you want to overwrite the current roster? The difference between the current roster and the importing roster is:\n"
        explanation += diff

        onclosing = lambda: self.destory_popup_window_after(self.overwrite_popup)
        self.overwrite_popup.protocol('WM_DELETE_WINDOW', onclosing)
        Label(self.overwrite_popup,text=explanation).grid()

        Button(self.overwrite_popup,text='Yes',command=lambda: self.destory_popup_window_after(self.overwrite_popup, lambda:self._import_roster(path_with_name))).grid()
        Button(self.overwrite_popup,text='No',command=onclosing).grid()

        self.overwrite_popup.transient(self.root)
        self.mainView.wait_window(self.overwrite_popup)

    # Use a file dialog to let the user choose a roster to import
    def import_roster_file_path_with_name(self):
        if(self.mainView.nb.index("current") == 0 and self.num_popup == 0):
            path_with_file_name = filedialog.askopenfilename(title='Choose your csv/tsv file', filetypes=(('CSV', '*.csv'),('TSV', '*.tsv')))
            rslt = IO.instance().importRoster(path_with_file_name)
            if(rslt[0] == 1):
                self.not_found_window()
            elif(rslt[0] == 2):
                self.overwrite_window(rslt[1], path_with_file_name)
            else:
                self.update_students_info()
    
    # Use a file dialog to let the user choose a directory to export the roster
    def export_roster_file_target_path_with_name(self):
        if(self.mainView.nb.index("current") == 0 and self.num_popup == 0):
            target = filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (('CSV', '*.csv'),('TSV', '*.tsv')))
            IO.instance().exportRoster(target)
    
    # Use a file dialog to let the user choose a directory to export the summary log
    def export_summary_file_target_path_with_name(self):
        if(self.mainView.nb.index("current") == 1 and self.num_popup == 0):
            target = filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (('TXT', '*.txt'),))
            if not target == None and not target == "":
                summary(target)
    
    # User a file dialog to let the user choose a directory to read students' portraits
    def set_photos_folder_path(self):
        if(self.num_popup == 0):
            tmp = filedialog.askdirectory(title='Choose your Photos directory')
            if not tmp == None and not tmp == "":
                global HOME_PHOTOS_PATH
                HOME_PHOTOS_PATH = tmp
                self.update_students_info()
    
    # Let the user select the font size of name label
    def font_size_window(self):
        try:
            self.font_size_window.focus_set()
            return
        except Exception:
            pass
        self.num_popup += 1
        self.fontsize_popup = Toplevel(self.root)
        self.fontsize_popup.title("Set names' font size")
        self.fontsize_popup.resizable(0,0)

        onclosing = lambda: self.destory_popup_window_after(self.fontsize_popup)
        self.fontsize_popup.protocol('WM_DELETE_WINDOW', onclosing)
        Label(self.fontsize_popup,text="Select font size").grid(row=0, column=0)
        
        listbox = Listbox(self.fontsize_popup)
        for i in range(12, 25):listbox.insert(END, i)
        listbox.select_set(int(self.cold_caller_tab_view.label_font['size']) - 12)
        listbox.grid(row=0, column=1)
        
        onOk = lambda: self.destory_popup_window_after(self.fontsize_popup, 
            lambda: self.cold_caller_tab_view.label_font.config(size=listbox.get(ANCHOR)))
        Button(self.fontsize_popup,text='OK',command=onOk).grid(row=1, column=0)
        Button(self.fontsize_popup,text='Cancel',command=onclosing).grid(row=1, column=1)
        self.fontsize_popup.transient(self.root)
        self.mainView.wait_window(self.fontsize_popup)

    # About me
    def aboutme_window(self):
        try:
            self.aboutme_popup.focus_set()
            return
        except Exception:
            pass
        self.num_popup += 1
        self.aboutme_popup = Toplevel(self.root)
        self.aboutme_popup.title("About")
        self.aboutme_popup.resizable(0,0)

        explanation = "This program is built to help in increasing students' participation in classes."

        onclosing = lambda: self.destory_popup_window_after(self.aboutme_popup)
        self.aboutme_popup.protocol('WM_DELETE_WINDOW', onclosing)
        Label(self.aboutme_popup,text=explanation).grid()
        Button(self.aboutme_popup,text='OK',command=onclosing).grid()

        self.aboutme_popup.transient(self.root)
        self.mainView.wait_window(self.aboutme_popup)
    
    def createMenu(self):
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)
        self.submenu= Menu(self.menu)
        self.menu.add_cascade(label="Import/Export",menu=self.submenu)
        self.submenu.add_command(label="Import a Roster", command=self.import_roster_file_path_with_name)
        self.submenu.add_command(label="Export to a Roster", command=self.export_roster_file_target_path_with_name)
        self.submenu.add_separator()
        self.submenu.add_command(label="Exit", command=self.root.quit)

        self.submenu2 = Menu(self.menu)
        self.menu.add_cascade(label="Misc",menu=self.submenu2)
        self.submenu2.add_command(label="Set Photos Folder", command=self.set_photos_folder_path)
        self.submenu2.add_command(label="Font Size", command=self.font_size_window)
        self.submenu2.add_command(label="About", command=self.aboutme_window)
    
    
    # Render the UI
    def show(self):
        self.root.mainloop()

