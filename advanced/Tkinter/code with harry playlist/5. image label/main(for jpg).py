from tkinter import *
from PIL import Image, ImageTk

root = Tk()

root.geometry("500x500")

# photo = PhotoImage(file="1.png") Not working for jpg image


# For jpg images

image = Image.open("1.jpeg")
photo = ImageTk.PhotoImage(image)




# we have to load this image into a label. then we can show it. So

label = Label(image = photo)
label.pack()

root.mainloop()