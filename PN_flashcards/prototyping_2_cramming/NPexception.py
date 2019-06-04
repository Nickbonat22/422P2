#!/usr/bin/env python3
'''
Author: Jerry Xie
Created on: May 16, 2019
Last modified by: Jerry Xie @ May 30, 2019
Effect: Helping the app distinguish special exception from each other.
'''
class Not_a_Dir(Exception):
    pass
class Index_Out_of_Bound(Exception):
    pass
class Unset_Directory(Exception):
    pass
class No_More_Assignment_Left(Exception):
    pass
class Not_A_Valid_Image(Exception):
    pass