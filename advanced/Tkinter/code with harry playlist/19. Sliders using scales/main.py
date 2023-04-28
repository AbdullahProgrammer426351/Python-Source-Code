from tkinter import *

root = Tk()
root.geometry("333x222")
root.title("Slider tutorial")


# creating vertical slider
myslider = Scale(root, from_=0, to=100)
myslider.pack()


# creating horizontal slider
myslider2 = Scale(root, from_=0, to=100, orient=HORIZONTAL)
myslider2.pack()

root.mainloop()