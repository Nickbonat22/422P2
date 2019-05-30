'''
    Author: Nicholas Bonat
    Created on: May 25th, 2019
    Purpose: display all the file names and corresponding image
    '''
import os
from PIL import ImageTk, Image
import tkinter as tk

#This creates the main window of an application
window = tk.Tk()
window.title("Gallery Test")
window.geometry("600x500")

people = []
arr = os.listdir("Resources/CS Faculty")
for x in arr:
    if x[-4:] == ".png":
        people.append(x)

def displayImage():
    selected = listbox.curselection()
    if selected: # only do stuff if user made a selection
        for index in selected:
            pass
        #print(listbox.get(index))
        img = ImageTk.PhotoImage(Image.open("Resources/CS Faculty/"+listbox.get(index)))
        panel.configure(image=img)
        panel.image = img

def populateListBox():
    count = 1
    for item in people: #people has to be a list already defined
        listbox.insert(count,item)
        count +=1

def editImage():

	getEntry = tk.Label(window, text="type new name:")
	getEntry.grid(row=2, column=1)
	entry = tk.Entry(window, text="type new name:")
	entry.grid(row=3, column=1)

	selected = listbox.curselection()
	if selected: # only do stuff if user made a selection
		for index in selected:
			pass
	os.getcwd()
	collection = "Resources/CS Faculty/"
	# for i, filename in enumerate(os.listdir(collection)):
	#     pass
	#os.rename("Resources/CS Faculty/" + listbox.get(index), "Resources/CS Faculty/" + entry.get() + ".png")


img = ImageTk.PhotoImage(Image.open("Resources/CS Faculty/"+people[0]))
#Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
#The Label widget is a standard Tkinter widget used to display a text or image on the screen.
panel = tk.Label(window, image = img)
panel.grid(row=1,column=0,sticky='W'+'E'+'N'+'S')

listbox = tk.Listbox(window,height=15, width=40)
listbox.grid(row=0,column=0)

populateListBox()

displayButton = tk.Button(window, text="Display Image", command=displayImage)
displayButton.grid(row=0,column=1)

editButton = tk.Button(window, text="Edit Entry", command=editImage)
editButton.grid(row=1,column=1)

#Start the GUI
window.mainloop()
