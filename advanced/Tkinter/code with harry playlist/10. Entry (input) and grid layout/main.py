from tkinter import *

def getVals():
    print(f"User name is : {userValue.get()}")
    print(f"Password is : {passValue.get()}")


root = Tk()
root.geometry("600x400")

user = Label(root, text="Username")
password = Label(root, text="Password")


# instead of pack method. we will user grid method in this tutorial to pack widgets in a grid
user.grid()
password.grid(row=1)


# Variable classes in tkinter
# BooleanVar, DoubleVar, IntVar, StringVar - we will use StringVar in this case

userValue = StringVar()
passValue = StringVar()

userEntry = Entry(root, textvariable=userValue)
passEntry = Entry(root, textvariable=passValue)

userEntry.grid(row=0, column=1)
passEntry.grid(row=1, column=1)


# making button in one line
Button(text="Submit", command=getVals).grid()
root.mainloop()