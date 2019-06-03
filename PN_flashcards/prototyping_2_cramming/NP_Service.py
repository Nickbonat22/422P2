from singleton import Singleton
import re
filename_pattern = r"(?P<name>[a-zA-Z0-9*!+_\s-]+)-(?P<memo>[a-zA-Z0-9*!+_\s-]+).(?:gif|jpg|jpeg|tiff|png)"
filename_pattern = re.compile(filename_pattern)

import os
from collections import deque
MAX_QUEUE_LEN = 64
from random import shuffle
from NPexception import *
import imghdr

@Singleton
class NP_Service:

    def __init__(self):
        self._working_path = 'Resources'
        self._targets = []
        self._assignments = deque([])
        self._assignments_need_review = deque([])
        self._assignments_done = deque([], MAX_QUEUE_LEN)
        
        self._old_files = set()
        self.removed = set()
        self.added = set()
    
    def __str__(self):
        rslt = ''
        rslt += "Current working path: " + str(self._working_path) + '\n'
        rslt += "The _assignments: " + str(self._assignments) + '\n'
        rslt += "Assignments finished: " + str(self._assignments_done) + '\n'
        rslt += "Assignments need to be reviewed: " + str(self._assignments_need_review) + '\n'
        rslt += "Next assignment: " + str(self.peek_next_assignment())
        return rslt
    
    # Difference detection
    def directory_is_changed(self):
        new = set()
        for filename in os.listdir(self._working_path):
            t = filename_pattern.match(filename)
            if not t == None:
                path = os.path.join(self._working_path, filename)
                if not imghdr.what(path) == None:
                    new.add(filename)
        if new == self._old_files:
            return False
        self.added = (new - self._old_files)
        self.removed = (self._old_files - new)
        self._old_files = new.copy()
        return True
    def change_handler(self):
        # handle removal
        if len(self.removed) > 0:
            i = 0
            while i < len(self._assignments):
                if(self._assignments[i]['filename'] in self.removed):
                    del self._assignments[i]
                else:
                    i += 1
            i = 0
            while i < len(self._assignments_need_review):
                if(self._assignments_need_review[i]['filename'] in self.removed):
                    del self._assignments_need_review[i]
                else:
                    i += 1
            i = 0
            while i < len(self._assignments_done):
                if(self._assignments_done[i]['filename'] in self.removed):
                    del self._assignments_done[i]
                else:
                    i += 1
            self.removed = set()
        
        if len(self.added) > 0:
            for filename in self.added:
                t = filename_pattern.match(filename)
                if not t == None:
                    file_entity = {
                        'filename': filename,
                        'name': t.group("name"),
                        'memo': t.group("memo"),
                    }
                    self._assignments.append(file_entity)
            self.added = set()

    # Filename and path parser
    def set_working_path(self, working_path):
        if os.path.isdir(working_path):
            self._working_path = working_path
            global filename_pattern
            for filename in os.listdir(self._working_path):
                t = filename_pattern.match(filename)
                if not t == None:
                    path = os.path.join(self._working_path, filename)
                    if not imghdr.what(path) == None:
                        file_entity = {
                            'filename': filename,
                            'name': t.group("name"),
                            'memo': t.group("memo"),
                        }
                        self._targets.append(file_entity)
        else:
            raise Not_a_Dir()
    
    # Photo assignments builder
    def assignments_constructor(self, random_order = True):
        self._assignments = deque([])
        for file_entity in self._targets:
            file_entity['remember'] = False
            self._assignments.append(file_entity)
            self._old_files.add(file_entity['filename'])
        if random_order == True:
            shuffle(self._assignments)
    
    # Scheduler
    def peek_next_assignment(self):
        if self.directory_is_changed():
            self.change_handler()
        if len(self._assignments) == 0 and len(self._assignments_need_review) == 0:
            raise No_More_Assignment_Left()
        if len(self._assignments) == 0:
            self._assignments = self._assignments_need_review
            self._assignments_need_review = deque([])
        return self._assignments[0]
    def schedule_next_assignment(self, with_performance_diagnosis, debuging_list_for_appending=None):
        if self.directory_is_changed():
            self.change_handler()
        # with_performance_diagnosis should be in [0, 1]
        if len(self._assignments) == 0 and len(self._assignments_need_review) == 0:
            raise No_More_Assignment_Left()
        if len(self._assignments) == 0:
            self._assignments = self._assignments_need_review
            self._assignments_need_review = deque([])
        tmp = self._assignments.popleft()
        if with_performance_diagnosis == 0:
            tmp['remember'] = True
            if not debuging_list_for_appending == None:
                debuging_list_for_appending.append(tmp)
        elif with_performance_diagnosis == 1:
            self._assignments_need_review.append(tmp)
        self._assignments_done.append(tmp)

if __name__ == '__main__':
    import random
    from tkinter import filedialog
    test = NP_Service.instance()
    working_path = filedialog.askdirectory(title='Choose a directory where you put your photos into')
    try:
        test.set_working_path(working_path)
        test.assignments_constructor()

        init_len = len(test._assignments)
        debuging_list_for_appending = []
        times = 10000
        while(times > 0):
            print(test.peek_next_assignment())
            performance = random.randint(0,1)
            print("Performance:", performance, '\n')
            test.schedule_next_assignment(performance, debuging_list_for_appending)
            times -= 1
        assert(len(debuging_list_for_appending) == init_len)
        print("THeir lengths are the same")
        
    except Not_a_Dir as e:
        print("The working path provided is not a directory")
    except Index_Out_of_Bound as e:
        print("Assigned index for the directory is out of bound")
    except Unset_Directory as e:
        print("Assignment's directory is unset")
    except No_More_Assignment_Left as e:
        print("No more assignments can be found")
        assert(len(debuging_list_for_appending) == init_len)
        print("THeir lengths are the same")
    except Exception as e:
        print("Unhandled exceptions caught " + str(e))
