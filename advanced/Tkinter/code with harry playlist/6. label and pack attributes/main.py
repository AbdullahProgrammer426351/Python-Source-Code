from tkinter import *
root = Tk()
root.geometry("444x233")
root.title("My GUI with Harry bhai")

# Important label options (attributes)
# text - adds the text
# bd - background
# fg - foreground
# font - sets the font (
# 1. font=("commicsansms", 19, "bold")
# 2. font="commicsansms 19 bold")
# padx - x axis padding
# pady - y axis padding
# relief - border styling - SUNKEN, RAISED, GROOVE, RIDGE

title_label = Label(text="this is text", bg="red", fg="white", padx=23, pady=44, font="commicsansms 19 bold", borderwidth=3, relief=RIDGE)



# Important pack options (attributes)
# anchor = nw(north to west), se(south to east) etc
# side = top, bottom, left, right
# fill - in which direction, it width will match_parent
# padx
# pady
# title_label.pack(anchor="nw", side=BOTTOM, fill=X)
title_label.pack(anchor="nw", side=LEFT, fill=Y, padx=22, pady=33)

root.mainloop()