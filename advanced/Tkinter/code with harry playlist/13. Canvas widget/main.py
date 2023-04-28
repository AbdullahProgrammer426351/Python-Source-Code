from tkinter import *
root = Tk()

canvas_width = 800
canvas_height = 400

root.geometry(f"{canvas_width}x{canvas_height}")


can_widget = Canvas(root, width=canvas_width, height=canvas_height)
can_widget.pack()


# creating line
# the line goes from the point x1, y1 to x2,y2
can_widget.create_line(0, 200, 800, 0, fill="red")

# creating rectangle
# parameters - top left, bottom right
can_widget.create_rectangle(3,5, 700, 300)


# creating oval
can_widget.create_oval(200,200,400,400)

# creating text
can_widget.create_text(200, 200, text="Text created with canvas")

root.mainloop()