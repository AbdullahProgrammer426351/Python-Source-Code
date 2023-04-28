from tkinter import *

root = Tk()
root.geometry("555x333")
root.title("Scrollbars")

# For connecting a (vertical)scrollbar to a widget
#1. widget(yscrollbarcommand = scrollbar.set)
#2. scrollbar.config(command=widget.yview)


scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)
lisbox = Listbox(root, yscrollcommand=scrollbar.set)
for i in range(344):
    lisbox.insert(END, f"item : {i}")

lisbox.pack(fill="both")
scrollbar.config(command=lisbox.yview)

root.mainloop()