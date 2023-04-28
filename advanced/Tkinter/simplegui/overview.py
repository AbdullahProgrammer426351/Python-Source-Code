import tkinter as tk
from tkinter import *


# 1. making the main window
m = tk.Tk(screenName="My screen name",  baseName=None,  className='My Class Name',  useTk=1)
# className-->window name


# TODO: widgets are added here
# making button
button = tk.Button(m, text='Stop', width=25, command=m.destroy, bg="#ae0b19")
button.grid()
m.mainloop()


# 2. mainloop (infinite loop untile user closes the application to show UI)
m.mainloop()