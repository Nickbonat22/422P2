#!/usr/bin/env python3
'''
April 7
Author: Nicholas Bonat
Created on: Apr 7, 2019
Class to hold and get student information
'''

class Student:
    def __init__(self, firstName, lastName, uoID, email, pSpelling, reveal):
        self.fname = firstName
        self.lname = lastName
        self.id = uoID
        self.email = email
        self.pspell = pSpelling
        self.reveal = reveal

        # each student is initially called on 0 times
        self.calledOnCount = 0
        self.concernCount = 0

    def getName(self):
        return self.fname + " " + self.lname

    def getNameInitial(self):
        try:
            rslt = self.fname[0] + self.lname[0]
            return rslt
        except:
            return ''

    def getFName(self):
        return self.fname

    def getLName(self):
        return self.lname

    def getID(self):
        return self.id

    def getEmail(self):
        return self.email

    def getPSpell(self):
        return self.pspell

    def getReveal(self):
        return self.reveal

    def getCalledOnCount(self):
        return self.calledOnCount

    # used for filling up the queue from a roster file
    def setCalledOnCount(self, called):
        try:
            self.calledOnCount = int(called)
        except:
            pass

    def getConcernCount(self):
        return self.concernCount

    # used for filling up the queue from a roster file
    def setConcernCount(self, concerns):
        try:
            self.concernCount = int(concerns)
        except:
            pass

    # string format
    def __str__(self):
        return self.fname + ' ' + self.lname

    def __eq__(self, other):
        if other == None:
            return False
        return ((self.fname == other.fname) and
            (self.lname == other.lname) and
            (self.id == other.id) and
            (self.email == other.email) and
            (self.pspell == other.pspell) and
            (self.reveal == other.reveal))