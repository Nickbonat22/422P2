#!/usr/bin/env python3
'''
CIS 422 Project 1
Author: Jerry Xie
Created on: Apr 14, 2019
Last modified by: Jerry Xie @ Apr 27, 2019
Effect: Provide easy access to remove or concern a student at a cerntain position in the student queue
'''
from time import time
from singleton import Singleton
from student_queue import Student_queue
from student import Student
from logService import dailyRemove, dailyConcern
from IOService import IO

@Singleton
class ColdCallerService:
    # For implementation of "...press the concern button within 1 second..."
    last_remove_time = time()

    def get_queue_length(self):
        return IO.instance().get_curr_queue().length()
    
    # Remove a student at a certain position and reinsert him/her to the back of the queue randomly
    def remove_stuent_at(self, position : int) -> bool:
        curr_queue = IO.instance().get_curr_queue()
        if(curr_queue.isEmpty() or position >= curr_queue.length()):
            return False
        the_student = curr_queue.popfrom(position)
        the_student.calledOnCount += 1
        curr_queue.pushRandom(the_student)
        dailyRemove(the_student)
        IO.instance().set_curr_queue(curr_queue)
        self.last_remove_time = time()
        return True

    # Concern the last remove student if it is called within 1 second of calling the remove function
    def concern_recent_student(self) -> bool:
        now = time()
        if now - self.last_remove_time <= 2:
            curr_queue = IO.instance().get_curr_queue()
            if(not curr_queue.has_recent_student_on_deck() or curr_queue.isEmpty()):
                return False
            the_student = curr_queue.lastRemove()
            the_student.concernCount += 1
            dailyConcern(the_student)
            return True
        return False
    
    # Return a student at the certain position
    def get_studnt_at(self, position : int) -> Student:
        curr_queue = IO.instance().get_curr_queue()
        if(curr_queue.isEmpty() or position >= curr_queue.length()):
            return None
        return curr_queue.get_student_at(position)

if __name__ == '__main__':
    f = ColdCallerService.instance() # Good. Being explicit is in line with the Python Zen
    g = ColdCallerService.instance() # Returns already created instance

    assert(f is g) # True
    