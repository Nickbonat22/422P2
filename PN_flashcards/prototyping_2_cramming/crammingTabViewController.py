from NPexception import *
from tkinter import *
from PIL import Image, ImageTk
class CrammingTabViewController:
    def __init__(self, manage_view):
        self.isFront = False
        self.isFinished = False
        self.CrammingTabView_delegate = manage_view
    
    def bind_good_btn_to(self, func):
        try:
            self.CrammingTabView_delegate.good_btn.bind('<Button-1>', func)
        except Exception as e:
            print(e)
    
    def bind_reset_btn_to(self, func):
        try:
            self.CrammingTabView_delegate.reset_btn.bind('<Button-1>', func)
        except Exception as e:
            print(e)

    def bind_forgot_btn_to(self, func):
        try:
            self.CrammingTabView_delegate.forgot_btn.bind('<Button-1>', func)
        except Exception as e:
            print(e)
    
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
            self.CrammingTabView_delegate.portrait_label.config(text=None)
            self.CrammingTabView_delegate.portrait_label.config(image=self.CrammingTabView_delegate.curr_portrait)
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