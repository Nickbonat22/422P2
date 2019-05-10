#!/usr/bin/env python3
'''
CIS 422 Project 1
Author: Zach Domke
Created on: Apr 14, 2019
Last modified by: Zach Domke @ Apr 28, 2019
Topic: IO Contoller Class
Effect: Imports a new roster to the system. Exports the current roster to the user. Manages the cache in the system.
'''

import os
import csv
from singleton import Singleton
from student import Student
from student_queue import Student_queue
DELIM = '\t'

# IO class manages any importing, exporting, or rewriting of files in Cold Caller.
@Singleton
class IO:
    curr_queue = None
    def __init__(self):
        self.curr_queue = Student_queue()
        try:
            with open("Resources/Internal Roster.tsv", 'r') as existingRoster:
                self.readFile(self.curr_queue.studentQ, existingRoster, True)
        except:
            print("No internal roster found")
            pass
        

# Helper method for getting the current queue.
    def get_curr_queue(self): 
        return self.curr_queue
    

# Helper method for setting the current queue.
    def set_curr_queue(self, to_queue = None):
        if not to_queue == None:
            self.curr_queue = to_queue
        self.cache(self.curr_queue)


# importRoster() takes in a file path to where we are importing a roster from.
# The method will read the new list of students, read the old list of students, and then merge the 2 once instructed by the user.
# Once the new list of students is compiled, the method overwrites the Internal Roster with the new list.
    def importRoster(self, filePath, user_response = False):
        # Locates the new roster or stops running if there is no new roster.
        newRoster = None
        try:
            newRoster = open(filePath, 'r')
        except FileNotFoundError:
            return (1,)

        # Populates the newStudentQ with the list of students from the new roster.
        newStudentQ = []
        self.readFile(newStudentQ, newRoster, False)

        # Populates the oldStudentQ with the students from the current/existing roster.
        oldStudentQ = []
        try:
            existingRoster = open("Resources/Internal Roster.tsv", 'r')
            self.readFile(oldStudentQ, existingRoster, True)
        except:
            print("No internal roster found")
            pass

        for student in oldStudentQ:
            print(student)
        if not user_response:
            # Checks if the queues are different. If they are different, we confirm with the user. If they are the same, we stop.
            diff = self.importWarning(newStudentQ, oldStudentQ)
            if not diff  == None:
                return (2, diff)
        
        for newStudent in newStudentQ:
            for oldStudent in oldStudentQ:
                if newStudent.getID() == oldStudent.getID():
                    newStudent.setCalledOnCount(oldStudent.getCalledOnCount())
                    newStudent.setConcernCount(oldStudent.getConcernCount())


        # Overwrites the existing internal roster with the new information.
        existingRoster = open("Resources/Internal Roster.tsv", 'w')
        existingRoster.write("<total times called>" + DELIM +
            "<times of concern>" + DELIM +
            "<first name>" + DELIM +
            "<last name>" + DELIM +
            "<UO ID>" + DELIM +
            "<email address>" + DELIM +
            "<phonetic spelling>" + DELIM +
            "<reveal code>\n")
        self.writeToFile(newStudentQ, existingRoster, True)
        existingRoster.close()

        self.curr_queue.studentQ = newStudentQ.copy()
        # if os.path.exists("ImportFolder/New Roster.tsv"):
        #     os.remove("ImportFolder/New Roster.tsv")
        return (0,)


# Helper function importWarning() takes in 2 lists of students.
# The method will compare the 2 lists and return a list of differences.
# The list of differences will also consist of who is added or removed.
    def importWarning(self, newStudentQ, oldStudentQ):
        # Populates the list of differences and tells whether the student will be added or removed.
        diffStudentQ = []
        for newStudent in newStudentQ:
            isIn = False
            for oldStudent in oldStudentQ:
                if newStudent == oldStudent:
                    isIn = True
            if not isIn:
                diffStudentQ.append((newStudent, "added"))
        for oldStudent in oldStudentQ:
            isIn = False
            for newStudent in newStudentQ:
                if oldStudent == newStudent:
                    isIn = True
            if not isIn:
                diffStudentQ.append((oldStudent, "removed"))

        # Stops running if there are no differences. Nothing will change.
        if not diffStudentQ:
            return None

        diff = ""
        for (student, code) in diffStudentQ:
            diff += student.getFName() + ' ' + student.getLName() + ' ' + code
            diff += '\n'        
        return diff
        

# exportRoster() will take in a path to where the current roster will be exported.
# It will copy the internal Roster to the provided path.
    def exportRoster(self, filePath):
        studentQ = []
        existingRoster = open("Resources/Internal Roster.tsv", 'r')
        self.readFile(studentQ, existingRoster, True)

        output = open(filePath, 'w')
        output.write("<first name>" + DELIM + 
            "<last name>" + DELIM + 
            "<UO ID>" + DELIM + 
            "<email address>" + DELIM + 
            "<phonetic spelling>" + DELIM + 
            "<reveal code>\n")
        self.writeToFile(studentQ, output, False)


# cache() takes in a list of students and will overwrite the Internal Roster with the current list of students.
# The Internal Roster is used to manage and save the queue.
    def cache(self, studentQueue):
        DELIM = '\t'
        existingRoster = open("Resources/Internal Roster.tsv", 'w')
        existingRoster.write("<total times called>" + DELIM +
            "<times of concern>" + DELIM + 
            "<first name>"+ DELIM +
            "<last name>"+ DELIM +
            "<UO ID>"+ DELIM +
            "<email address>"+ DELIM +
            "<phonetic spelling>"+ DELIM +
            "<reveal code>\n")
        self.writeToFile(studentQueue.getQueue(), existingRoster, True)
        existingRoster.close()


# createFile() will an output file that will not override any other file.
# The method checks if another file by that name already exists, and if it does, it increments a number in the file name.
    def createFile(self, fileName):
        try:
            output = open(fileName + ".tsv", 'x')
        except FileExistsError:
            counter = 1
            while True:
                try:
                    output = open(fileName + "(" + str(counter) + ").tsv", 'x')
                    break;
                except FileExistsError:
                    counter += 1

        return output


# The readFile() method will take in a list to populate with students and a file to read from.
# The method stars by checking if the file is a tsv or csv, then reads each row of the file.
# For each row, the method will create a student and append that to the list.
    def readFile(self, studentQ, input, importCodes):
        # sys.path = currentSys
        if not self.is_tsv(input):
            return studentQ

        reader = csv.reader(input, delimiter=DELIM)
        for row in reader:
            if row[-1] == 'X' or row[-1] == "False":
                reveal = False
            else:
                reveal = True
            if importCodes:
                tempStudent = Student(row[2], row[3], row[4], row[5], row[6], reveal)
                tempStudent.setCalledOnCount(row[0])
                tempStudent.setConcernCount(row[1])
            else:
                tempStudent = Student(row[0], row[1], row[2], row[3], row[4], reveal)

            studentQ.append(tempStudent)
        input.close()
        del studentQ[0]
        return studentQ


# A helper function, is_tsv() takes in a file and checks if the file is a csv or a tsv file.
# Once the format is determined, the global variable DELIM is altered to match the format.
    def is_tsv(self, infile):
        try:
            DELIM = '\t'
            dialect = csv.Sniffer().sniff(infile.read(1024), delimiters=DELIM)
            infile.seek(0)
            return True
        except csv.Error:
            try:
                DELIM = ', '
                dialect = csv.Sniffer().sniff(infile.read(1024))
                infile.seek(0)
                return True
            except csv.Error:
                DELIM = '\t'
                return False


# writeToFile() will take in a list of students and which file to write them to.
# The method runs through each student in the list and writes the required information to the output file.
    def writeToFile(self, studentQ, output, printCodes):
        if printCodes:
            for student in studentQ:
                output.write(str(student.getCalledOnCount()) + DELIM)
                output.write(str(student.getConcernCount()) + DELIM)
                output.write(student.getFName() + DELIM)
                output.write(student.getLName() + DELIM)
                output.write(student.getID() + DELIM)
                output.write(student.getEmail() + DELIM)
                output.write(student.getPSpell() + DELIM)
                output.write(str(student.getReveal()) + '\n')
        else:
            for student in studentQ:
                output.write(student.getFName() + DELIM)
                output.write(student.getLName() + DELIM)
                output.write(student.getID() + DELIM)
                output.write(student.getEmail() + DELIM)
                output.write(student.getPSpell() + DELIM)
                output.write(str(student.getReveal()) + '\n')
