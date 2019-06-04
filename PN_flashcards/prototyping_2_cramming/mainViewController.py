#!/usr/bin/env python3
'''
Contributors: Nicholas Bonat, Jerry Xie

Created on: May 16, 2019

Last modified by: Nicholas Bonat @ June 1, 2019

Effect: Binded global keystrokes and handled tab views' transition logic.

'''
from mainView import *
from NPexception import *
from crammingTabView import CrammingTabView

class MainViewController():
    def __init__(self, root_window):
        # The root window
        self.root = root_window
        self.root.geometry("500x500")
        self.root.title("Photo-Name Trainer")
        self.num_popup = 0
        self.aboutme_popup = None
        self.fontsize_popup = None
        self.howto_popup = None


        # Adaptive view setting
        rows = 0
        while rows < 50:
            self.root.rowconfigure(rows, weight=1)
            self.root.columnconfigure(rows, weight=1)
            rows += 1
        
        self.CrammingTabViewControllerDelegate = None
        self.mainView = MainView(self.root)
        self.CrammingTabViewControllerDelegate = CrammingTabViewController(self.mainView.tab1)
        self.mainView.grid(row=0, column=0, columnspan=50, rowspan=50, sticky=(N,W,S,E))
        self.root.bind('<space>', lambda e: self.CrammingTabViewControllerDelegate.switch_flashcard_side())
        self.root.bind('1', lambda e: self.CrammingTabViewControllerDelegate.perform_and_update_info(1))
        self.root.bind('2', lambda e: self.CrammingTabViewControllerDelegate.perform_and_update_info(0))

        self.cramming_tab_view = self.mainView.get_cramming_tab_view()

        self.createMenu()

    # top bar menu methods - Nicholas Bonat

    # Destory a popup window after doing a certain job
    def destory_popup_window_after(self, popup, doing_this_before = None):
        if not doing_this_before == None:
            try:
                doing_this_before()
            except Exception as e:
                print(e)
        popup.destroy()
        self.num_popup -= 1

    # change font size
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
        listbox.select_set(int(self.cramming_tab_view.label_font['size']) - 12)
        listbox.grid(row=0, column=1)
        
        onOk = lambda: self.destory_popup_window_after(self.fontsize_popup, 
            lambda: self.cramming_tab_view.label_font.config(size=listbox.get(ANCHOR)))
        Button(self.fontsize_popup,text='OK',command=onOk).grid(row=1, column=0)
        Button(self.fontsize_popup,text='Cancel',command=onclosing).grid(row=1, column=1)
        self.fontsize_popup.transient(self.root)
        self.mainView.wait_window(self.fontsize_popup)

    # about the app
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

        explanation = "This program is built to help users learn people's names based off their images."

        onclosing = lambda: self.destory_popup_window_after(self.aboutme_popup)
        self.aboutme_popup.protocol('WM_DELETE_WINDOW', onclosing)
        Label(self.aboutme_popup,text=explanation).grid()
        Button(self.aboutme_popup,text='OK',command=onclosing).grid()

        self.aboutme_popup.transient(self.root)
        self.mainView.wait_window(self.aboutme_popup)

    # how to use the app
    def howto_window(self):
        try:
            self.aboutme_popup.focus_set()
            return
        except Exception:
            pass
        self.num_popup += 1
        self.howto_popup = Toplevel(self.root)
        self.howto_popup.title("Using the Photo-Name Trainer Application")
        self.howto_popup.resizable(0,0)

        setup = "Setting up image files and a working directory:"
        setup_1 = "1. Select images of people you would like to remember"
        setup_2 = "2. Edit the file name to *person(s) name-memo* format"
        setup_3 = "3. Create a directory and drag and drop the images into it\n"

        using_app = "Using the application:"
        using_app_1 = "1. Click the space-bar to reveal the name and memo corresponding to the shown image"
        using_app_2 = "2. Click the key `1` or select `Forgot` to indicate you would like to see the card again"
        using_app_3 = "3. Click the key `2` or select `Good` to indicate you are familiar with the person and their name"

        onclosing = lambda: self.destory_popup_window_after(self.howto_popup)
        self.howto_popup.protocol('WM_DELETE_WINDOW', onclosing)
        Label(self.howto_popup,text=setup).grid()
        Label(self.howto_popup,text=setup_1).grid()
        Label(self.howto_popup,text=setup_2).grid()
        Label(self.howto_popup,text=setup_3).grid()
        Label(self.howto_popup,text=using_app).grid()
        Label(self.howto_popup,text=using_app_1).grid()
        Label(self.howto_popup,text=using_app_2).grid()
        Label(self.howto_popup,text=using_app_3).grid()
        Button(self.howto_popup,text='OK',command=onclosing).grid()

        self.howto_popup.transient(self.root)
        self.mainView.wait_window(self.howto_popup)
    
    # build the top bar menu
    def createMenu(self):
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)
        self.submenu2 = Menu(self.menu)
        self.menu.add_cascade(label="Help",menu=self.submenu2)
        self.submenu2.add_command(label="Font Size", command=self.font_size_window)
        self.submenu2.add_command(label="Using the Photo-Name Trainer Application ", command=self.howto_window)
        self.submenu2.add_command(label="About", command=self.aboutme_window)
        self.submenu2.add_separator()
        self.submenu2.add_command(label="Exit", command=self.root.quit)

    def show(self):
        self.root.mainloop()