from tkinter import *

def myfunc():
    print("Function trigerred")
root = Tk()

root.geometry("733x566")
root.title("Pycharm")



# # creating non-dropdown menu
# mymenu = Menu(root)
# mymenu.add_command(label="File", command=myfunc)
# mymenu.add_command(label="Exit", command=quit)
# root.config(menu=mymenu)


# creating menu with dropdown
yourmenubar = Menu(root)
m1 = Menu(yourmenubar)
# if you want to remove ----- lines on top of menus, then you can use : m1 = Menu(yourmenubar, tearoff=0)
m1.add_command(label="New Project", command=myfunc)
m1.add_command(label="Save", command=myfunc)
# adding line/separator
m1.add_separator()
m1.add_command(label="Save As", command=myfunc)
m1.add_command(label="Print", command=myfunc)

yourmenubar.add_cascade(label="File", menu=m1)

root.config(menu=yourmenubar)




root.mainloop()