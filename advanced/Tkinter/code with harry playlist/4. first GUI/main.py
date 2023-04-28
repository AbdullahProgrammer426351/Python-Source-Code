from tkinter import *

root = Tk()

# Adjusting size of window (format : widhtxheight)
root.geometry("444x444")

# adjusting min size(format : width, height)
root.minsize(200,100)

# adjusting max size(format : width, height)
root.maxsize(800,500)


# making label (like TextView)(it is that view with which user does't interact)
label = Label(text="This is basic label")

# it is neccessary to pack widgets that you want to show on screen like below. Otherwise it will not visible
label.pack()

root.mainloop()