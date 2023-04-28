from tkinter import *

root = Tk()
root.geometry("655x333")

def hellow():
    print("Hellow tkinter buttons")

def name():
    print("My name is Harry")

frame = Frame(root, borderwidth=6, bg="green", relief="groove")
frame.pack(side=LEFT, anchor="nw")

b1 = Button(frame, fg="red", text="Print Now", command=hellow)
b1.pack(side=LEFT, padx=23)
b2 = Button(frame, fg="red", text="Tell name", command=name)
b2.pack(side=LEFT, padx=23)
b3 = Button(frame, fg="red", text="Print Now")
b3.pack(side=LEFT, padx=23)
b4 = Button(frame, fg="red", text="Print Now")
b4.pack(side=LEFT, padx=23)

root.mainloop()