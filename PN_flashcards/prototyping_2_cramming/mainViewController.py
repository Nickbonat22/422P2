from mainView import *
from NP_Service import NP_Service
from NPexception import *
import os
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
        
        self.isFront = False
        self.CrammingTabViewControllerDelegate = None
        self.mainView = MainView(self.root, self)
        assert(not self.CrammingTabViewControllerDelegate == None)
        self.mainView.grid(row=0, column=0, columnspan=50, rowspan=50, sticky=(N,W,S,E))
        try:
            self.update_info()
            self.root.bind('<space>', self.switch_side)
            self.CrammingTabViewControllerDelegate.bind_good_btn_to(lambda e: self.perform_and_update_info(1))
            self.CrammingTabViewControllerDelegate.bind_forgot_btn_to(lambda e: self.perform_and_update_info(0))
            self.CrammingTabViewControllerDelegate.bind_reset_btn_to(self.reset)
            self.root.bind('1', lambda e: self.perform_and_update_info(1))
            self.root.bind('2', lambda e: self.perform_and_update_info(0))
        except Exception as e:
            raise(e)
    def show(self):
        self.root.mainloop()
    
    def switch_side(self, event):
        self.isFront = self.CrammingTabViewControllerDelegate.switch_flashcard_side()
    
    def reset(self, event):
        self.CrammingTabViewControllerDelegate.reset()
        try:
            NP_Service.instance().assignments_constructor()
            self.update_info()
        except Exception as e:
            raise(e)
    
    def update_info(self):
        try:
            next_assignment = NP_Service.instance().peek_next_assignment()
            self.CrammingTabViewControllerDelegate.update_portrait(
                os.path.join(
                    NP_Service.instance()._working_path, 
                    next_assignment['filename']
                )
            )
            self.CrammingTabViewControllerDelegate.update_name(next_assignment['name'])
            self.CrammingTabViewControllerDelegate.update_memo(next_assignment['memo'])
            self.isFront = self.CrammingTabViewControllerDelegate.switch_flashcard_side()
        except No_More_Assignment_Left as e:
            print("No more assignment")
            self.CrammingTabViewControllerDelegate.all_set()
        except Exception as e:
            raise e
    
    def perform_and_update_info(self, performance_diagnosis:int):
        if not self.isFront == True:
            try:
                NP_Service.instance().schedule_next_assignment(performance_diagnosis)
                self.update_info()
            except No_More_Assignment_Left as e:
                print("No more assignment")
                self.CrammingTabViewControllerDelegate.all_set()
            except Exception as e:
                raise e
            