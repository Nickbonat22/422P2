#!/usr/bin/env python3
'''
Author: Jerry Xie

Created on: May 16, 2019

Last modified by: Jerry Xie @ May 16, 2019

Effect: Flashcard prototype

'''
from tkinter import *
from NPService import get_names_memos_for
import sys
import os
Waiting_For_Response = False
Resources_Directory = 'Resources'
# Event_Directory = 'CAS Diversity Heads'
Event_Directory = 'CS Faculty'
Target_Directory = os.path.join(Resources_Directory, Event_Directory)
Photos_Queue = [s.strip() for s in os.listdir(Target_Directory) if s.endswith('.png')]
Memos_Path = os.path.join(Target_Directory, 'memos.ini')
Records_Container = get_names_memos_for(Memos_Path)
print(Photos_Queue)
print(Records_Container)
next_photo = None
curr_name = None

def update_card(image_label, name_label, memo_label, btn_frame):
    global next_photo
    global curr_name
    global Waiting_For_Response
    global Records_Container
    global Photos_Queue

    if Waiting_For_Response:
        try:
            assert not curr_name == None
            btns_frame.pack(fill=BOTH, expand=YES)
            name_label.config(text=curr_name)
            memo_label.config(text=Records_Container[curr_name])
            Waiting_For_Response = False
        except Exception as e:
            if len(Photos_Queue) == 0:
                name_label.config(text="You are all set.")
                memo_label.config(text="")
            else:
                name_label.config(text="Internal error when answering" + str(e))
                memo_label.config(text="Internal error when answering" + str(e))
        curr_name = None
        return
    
    try:
        next_photo_filename = Photos_Queue.pop()
        curr_name = next_photo_filename.split('.')[0]
        try:
            next_photo = PhotoImage(file=os.path.join(Target_Directory, next_photo_filename))
            scale_w = next_photo.width() // 194 + 1
            scale_h = next_photo.height() // 194 + 1
            next_photo = next_photo.subsample(scale_w, scale_h)
        except Exception as e:
            print(e)
            next_photo = PhotoImage(file='Resources/default.png')
        finally:
            image_label.config(image=next_photo)
            name_label.config(text="")
            memo_label.config(text="")
    except Exception as e:
        next_photo = PhotoImage(file='Resources/default.png')
        image_label.config(image=next_photo)
        if len(Photos_Queue) == 0:
            name_label.config(text="You are all set.")
            memo_label.config(text="")
        else:
            name_label.config(text="Internal error" + str(e))
            memo_label.config(text="Internal error" + str(e))
    finally:
        btn_frame.pack_forget()
        Waiting_For_Response = True


root = Tk()
root.geometry("500x500")
rows = 0
while rows <= 50:
    root.rowconfigure(rows, weight=1)
    root.columnconfigure(rows, weight=1)
    rows += 1
frame = Frame(root)
frame.pack(fill=BOTH, expand=YES)

title_label = Label(frame, text="Currently reviewing " + Event_Directory)
image_label = Label(frame)
name_label = Label(frame)
memo_label = Label(frame)
title_label.pack(fill=BOTH, expand=YES, anchor=CENTER)
image_label.pack(fill=BOTH, expand=YES)
name_label.pack(fill=BOTH, expand=YES)
memo_label.pack(fill=BOTH, expand=YES)

btns_frame = Frame(frame)
btns_frame.pack(fill=BOTH, expand=YES)
forgot_btn = Button(btns_frame, text='Forgot', bg='red', highlightbackground='red')
hard_btn = Button(btns_frame, text="It's hard", bg='yellow', highlightbackground='yellow')
good_btn = Button(btns_frame, text="Good", bg='green', highlightbackground='green')
too_easy_btn = Button(btns_frame, text="Too easy", bg='blue', highlightbackground='blue')
forgot_btn.pack(fill=BOTH, expand=YES, side=LEFT)
hard_btn.pack(fill=BOTH, expand=YES, side=LEFT)
good_btn.pack(fill=BOTH, expand=YES, side=LEFT)
too_easy_btn.pack(fill=BOTH, expand=YES, side=LEFT)

update_card(image_label, name_label, memo_label, btns_frame)
root.bind('<space>', lambda e: update_card(image_label, name_label, memo_label, btns_frame))
root.mainloop()