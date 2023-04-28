from tkinter import *

def harry(event):
    print(f"You clicked on the button at x: {event.x} and y : {event.y}")

root = Tk()
root.title("Events in tkinter")
root.geometry("600x400")

widget = Button(root, text="Click me please")
widget.pack()

# binding events with button
widget.bind('<Button-1>', harry)
widget.bind('<Double-1>', quit)

# first argument is event name like Button-1 for clicking and Double-1 for double click. See documentation for more...

root.mainloop()