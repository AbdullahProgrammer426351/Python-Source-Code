from tkinter import *

root = Tk()

root.geometry("500x500")

photo = PhotoImage(file="1.png") # NOTE : PhotoImage does't support jpg or other image formats. for using jpg, visit:
# https://stackoverflow.com/questions/62926147/error-in-displaying-an-image-using-tkinter


# we have to load this image into a label. then we can show it. So

label = Label(image = photo)
label.pack()

root.mainloop()