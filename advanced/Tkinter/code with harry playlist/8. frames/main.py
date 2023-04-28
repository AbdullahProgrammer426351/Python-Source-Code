from tkinter import *
root = Tk()

root.geometry("666x333")

# making frame
f1 = Frame(root, bg="grey", borderwidth=6, relief=SUNKEN)
f1.pack(side=LEFT, fill="y")
f2 = Frame(root, borderwidth=8, bg="grey", relief=SUNKEN)
f2.pack(side=TOP, fill="x")

l1 = Label(f1, text="Project Tkinter - Pycharm")
l1.pack(pady=10)

l2 = Label(f2, text="Welcome to sublime text")
l2.pack(pady=10)

root.mainloop()