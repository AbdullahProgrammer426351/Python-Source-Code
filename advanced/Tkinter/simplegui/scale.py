from tkinter import *
master = Tk()
# vertical scale
w = Scale(master, from_=0, to=42, orient=VERTICAL)
w.pack()
#horizontal scale
w = Scale(master, from_=0, to=200, orient=HORIZONTAL)
w.pack()
mainloop()
