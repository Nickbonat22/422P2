#!/usr/bin/env python3
'''
Author: Nicholas Bonat
Created on: 4-7-2019
Create daily log file and write to it
'''

from student import Student
import datetime
import sys
import csv
import os
HOME_PATH = os.getenv('HOME')
sys.path.append('../Resources/')

#open file, the current date to the daily log, then close it so it can be read in full
now = datetime.datetime.now()
with open(os.path.join(HOME_PATH, 'dailylog.txt'), 'w+') as file:
	file.write('Cold Caller Daily Log\n')
	file.write(now.strftime("%m-%d-%Y\n\n"))

#open file, add first/last/email, close file
def dailyRemove(name):
	with open(os.path.join(HOME_PATH, 'dailylog.txt'), 'a') as file:
		string = name.getFName() + ' ' + name.getLName() + ' ' + name.getEmail()+ "\n"
		file.write(string)

#open file, go to last line and add X, close file
def dailyConcern(name):
	t = open(os.path.join(HOME_PATH, 'dailylog.txt'), 'r+')
	last_line = t.readlines()
	last_line[-1] = "X " + name.getFName() + ' ' + name.getLName() + ' ' + name.getEmail() + "\n"
	final_log = open(os.path.join(HOME_PATH, 'dailylog.txt'), 'w')
	final_log.writelines(last_line)
	final_log.close()

#create the summary file
def summary(path = 'summary.txt'):
	with open("Resources/Internal Roster.tsv", 'r') as roster_file:
		with open(path, 'w+') as sum_file:
			reader = csv.reader(roster_file, delimiter='\t')
			sum_file.write("Summary Performace\n\n")
			for row in reader:
				string = '	'.join(row[0:8]) +"\n"
				sum_file.writelines(string)
	
def getDailyLog():
	with open(os.path.join(HOME_PATH, 'dailylog.txt'), 'r') as file:
		data = file.read()
		return data

