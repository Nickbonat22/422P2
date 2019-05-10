#!/usr/bin/env python3
'''
CIS 422 Project 1
Contributors: Jerry Xie, Vu Vo, Qi Han
Created on: Apr 14, 2019
Last modified by: Qi Han @ Apr 28, 2019 
Effect: This is an implementation of the data structure used to store students
'''
from collections import deque
import random
import math
import functools
REINSERTION_AFTER_FIRST_N_PERCENT = 30

class Student_queue:
    #studentQ = [] # [Student]
    def __init__(self):
        self.studentQ = []
        self.recent = None
    
    # get students' first and last name
    def __str__(self):
        rslt = ''
        for student in self.studentQ:
            rslt += str(student)
            rslt += '->'
        return rslt
   
    # check if recent student variable is empty
    def has_recent_student_on_deck(self):
        return not self.recent == None

    # check if the student queue is empty
    def isEmpty(self):
        return self.studentQ == []

    # return the length of the students queue
    def length(self):
        return len(self.studentQ)
    
    # reset recent stduent variable
    def clear_last_rencent(self):
        self.recent = None

    def popfrom(self,location):
        # this function will remove a student from a specified location
        # and call IOService to save the queue
        #self.studentQ.pop(location)
        self.recent = self.studentQ.pop(location)
        return self.recent

    # return the last removed student
    def lastRemove(self):
        return self.recent

    def pushRandom(self,student):
        # dont forget to use the reinsertion_after_first_n_percent info
        # we can set this up in the main.py as an environment variable
        #this function will randomly reinsert a student back into queue
        global REINSERTION_AFTER_FIRST_N_PERCENT
        lower_bound = math.floor(len(self.studentQ) * REINSERTION_AFTER_FIRST_N_PERCENT / 100)
        value = random.randint(lower_bound, len(self.studentQ))
        self.studentQ.insert(value,student)
   
    # peek from the certain position 
    def get_student_at(self, position):
        return self.studentQ[position]

    # set student queue
    def setQueue(self, studentList):
        self.studentQ = studentList

    # return student queue
    def getQueue(self):
        return self.studentQ
