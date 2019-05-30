#!/usr/bin/env python3
'''
Author: Jerry Xie

Created on: May 16, 2019

Last modified by: Jerry Xie @ May 30, 2019

Effect: Handled widgets' transition logic.

'''
import os
from NPexception import *
from tkinter import *
from NP_Service import NP_Service
from NPexception import *
from PIL import Image, ImageTk
class CrammingTabViewController:
    def __init__(self, manage_view):
        self.isFront = False
        self.isFinished = False
        self.CrammingTabView_delegate = manage_view
        self.CrammingTabView_delegate.good_btn.bind('<Button-1>', lambda e: self.perform_and_update_info(1))
        self.CrammingTabView_delegate.forgot_btn.bind('<Button-1>', lambda e: self.perform_and_update_info(0))
        self.CrammingTabView_delegate.reset_btn.bind('<Button-1>', lambda e: self.reset())
        self.update_info()

    def update_info(self):
        try:
            next_assignment = NP_Service.instance().peek_next_assignment()
            self.update_portrait(
                os.path.join(
                    NP_Service.instance()._working_path, 
                    next_assignment['filename']
                )
            )
            self.update_name(next_assignment['name'])
            self.update_memo(next_assignment['memo'])
            self.isFront = self.switch_flashcard_side()
        except No_More_Assignment_Left as e:
            print("No more assignment")
            self.all_set()
        except Exception as e:
            raise e

    def perform_and_update_info(self, performance_diagnosis:int):
        if not self.isFront == True:
            try:
                NP_Service.instance().schedule_next_assignment(performance_diagnosis)
                self.update_info()
            except No_More_Assignment_Left as e:
                print("No more assignment")
                self.all_set()
            except Exception as e:
                raise e
    
    def update_portrait(self, with_image_file_path):
        try:
            self.CrammingTabView_delegate.curr_portrait_im = Image.open(with_image_file_path)
            (imageSizeWidth, imageSizeHeight) = self.CrammingTabView_delegate.curr_portrait_im.size
            longest = max(imageSizeWidth, imageSizeHeight)
            ratio = longest / 320
            self.CrammingTabView_delegate.curr_portrait_im = self.CrammingTabView_delegate.curr_portrait_im.resize(
                (int(imageSizeWidth//ratio), int(imageSizeHeight//ratio)), 
                Image.ANTIALIAS)
            self.CrammingTabView_delegate.curr_portrait = ImageTk.PhotoImage(self.CrammingTabView_delegate.curr_portrait_im)
            self.CrammingTabView_delegate.portrait_label.config(text="", image=self.CrammingTabView_delegate.curr_portrait)
        except Exception as e:
            print(e)
            self.CrammingTabView_delegate.portrait_label.config(
                image = '', 
                text = "Having troubles loading this image file at path " + with_image_file_path
                )
    
    def update_name(self, new_name):
        self.CrammingTabView_delegate.name_label.config(text=new_name)
    def update_memo(self, new_memo):
        self.CrammingTabView_delegate.memo_label.config(text=new_memo)
    
    def all_set(self):
        self.update_name("Well done!!! You are all set!!! For now.")
        self.update_memo("Well done!!! You are all set!!! For now.")
        self.CrammingTabView_delegate.portrait_label.config(
                image = '', 
                text = "Well done!!! You are all set!!! For now."
        )
        self.isFinished = True
        self.switch_flashcard_side()
    
    def reset(self):
        self.isFinished = False
        self.CrammingTabView_delegate.reset_btn.grid_remove()
        self.CrammingTabView_delegate.good_btn.grid()
        self.CrammingTabView_delegate.forgot_btn.grid()
        self.switch_flashcard_side()

        try:
            NP_Service.instance().assignments_constructor()
            self.update_info()
        except Exception as e:
            raise(e)

    def switch_flashcard_side(self):
        if self.isFinished:
            self.isFront = True
            self._show_labels()
            self._show_btns()
            self.CrammingTabView_delegate.reset_btn.grid()
            self.CrammingTabView_delegate.good_btn.grid_remove()
            self.CrammingTabView_delegate.forgot_btn.grid_remove()
        elif self.isFront:
            self.isFront = False
            self._show_labels()
            self._show_btns()
        else:
            self.isFront = True
            self._hide_labels()
            self._hide_btns()
        return self.isFront
    
    def _show_labels(self):
        self.CrammingTabView_delegate.name_label.grid()
        self.CrammingTabView_delegate.memo_label.grid()
    def _hide_labels(self):
        self.CrammingTabView_delegate.name_label.grid_remove()
        self.CrammingTabView_delegate.memo_label.grid_remove()
    def _show_btns(self):
        self.CrammingTabView_delegate.btns_frame.grid()
    def _hide_btns(self):
        self.CrammingTabView_delegate.btns_frame.grid_remove()