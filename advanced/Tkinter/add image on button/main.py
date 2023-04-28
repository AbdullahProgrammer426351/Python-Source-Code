# importing only those functions
# which are needed
from tkinter import *
from tkinter.ttk import *

# creating tkinter window
root = Tk()

# Adding widgets to the root window
Label(root, text = 'GeeksforGeeks', font =(
'Verdana', 15)).pack(side = TOP, pady = 10)

# Creating a photoimage object to use image
photo = PhotoImage(file = "E:\\Programing(Documents)\\deep python\\Python-Source-Code\\advanced\\Tkinter\\img.jpeg")

# here, image option is used to
# set image on button
Button(root, text = 'Click Me !', image = photo).pack(side = TOP)

mainloop()
