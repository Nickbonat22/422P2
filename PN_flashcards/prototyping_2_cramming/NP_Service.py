import re
filename_pattern = r"(?P<name>[a-zA-Z0-9_\s-]+)-(?P<memo>[a-zA-Z0-9_\s-]+).png"
filename_pattern = re.compile(filename_pattern)

import os
from collections import deque
MAX_QUEUE_LEN = 64
from random import shuffle
class Not_a_Dir(Exception):
    pass
class Index_Out_of_Bound(Exception):
    pass
class Unset_Directory(Exception):
    pass
class No_More_Assignment_Left(Exception):
    pass
class NP_Service:

    def __init__(self):
        self._working_path = '.'
        self._directories = []
        self._directory = None
        self._assignments = deque([])
        self._assignments_need_review = deque([])
        self._assignments_done = deque([], MAX_QUEUE_LEN)
    
    def __str__(self):
        rslt = ''
        rslt += "Current working path: " + str(self._working_path) + '\n'
        rslt += "It contains directories: " + str(self._directories) + '\n'
        rslt += "The NP_Service is now reading the directory: " + str(self._directory) + '\n'
        rslt += "The _assignments: " + str(self._assignments) + '\n'
        rslt += "Assignments finished: " + str(self._assignments_done) + '\n'
        rslt += "Assignments need to be reviewed: " + str(self._assignments_need_review) + '\n'
        rslt += "Next assignment: " + str(self.peek_next_assignment())
        return rslt
    
    # Filename and path parser
    def set_working_path(self, working_path):
        if os.path.isdir(working_path):
            self._working_path = working_path
            self._directory = None
            self._get_directories()
        else:
            raise Not_a_Dir()
    def _get_directories(self):
        self._directories = [f.path for f in os.scandir(self._working_path) if f.is_dir()]
    def set_directory(self, to_index_of_directories):
        if to_index_of_directories < 0 or to_index_of_directories >= len(self._directories):
            raise Index_Out_of_Bound()
        else:
            self._directory = self._directories[to_index_of_directories]
    
    # Photo assignments builder
    def assignments_constructor(self, random_order = True):
        if self._directory == None:
            raise Unset_Directory()
        self._assignments = deque([])
        global filename_pattern
        for filename in os.listdir(self._directory):
            t = filename_pattern.match(filename)
            if not t == None:
                self._assignments.append({
                        'filename': filename, 
                        'name': t.group("name"),
                        'memo':t.group("memo"),
                        'remember': False
                    })
        if random_order == True:
            shuffle(self._assignments)
    
    # Scheduler
    def peek_next_assignment(self):
        if len(self._assignments) == 0 and len(self._assignments_need_review) == 0:
            raise No_More_Assignment_Left()
        if len(self._assignments) == 0:
            self._assignments = self._assignments_need_review
            self._assignments_need_review = deque([])
        return self._assignments[0]
    def schedule_next_assignment(self, with_performance_diagnosis, debuging_list_for_appending=None):
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
    test = NP_Service()
    working_path = 'Resources'
    import random
    try:
        test.set_working_path(working_path)
        test.set_directory(1)
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
