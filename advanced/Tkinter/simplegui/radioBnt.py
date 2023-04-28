from tkinter import *
root = Tk()
v = IntVar()
v2 = IntVar()
Radiobutton(root, text='GfG', variable=v, value=1).pack(anchor=W)
Radiobutton(root, text='GfG', variable=v, value=2).pack(anchor=W)
Radiobutton(root, text='Separte', variable=v2, value=2).pack(anchor=W)
mainloop()
