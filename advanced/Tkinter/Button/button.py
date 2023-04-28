from tkinter import *

from tkinter.ttk import *

# create root window
root = Tk()		

btn = Button(root, text="Click me !",
              command=root.destroy);

root.geometry('400x400')

btn.pack(side='left')

# Tkinter event loop
root.mainloop()		