from tkinter import *
def click(event):
    global scvalue
    text = event.widget.cget("text")
    # print(text)
    if text == "=":
        if scvalue.get().isdigit():
            value = int(scvalue.get())
        else:
            value = eval(screen.get())
        scvalue.set(value)
    elif text == "C":
        scvalue.set("")
    else:
        scvalue.set(scvalue.get() + text)
    screen.update()
root = Tk()
root.geometry("644x900")
root.title("Calculator By Code With Harry")
root.wm_iconbitmap("dragon.ico")


scvalue = StringVar()
scvalue.set("")
screen = Entry(root, textvariable=scvalue, font="lucida 40 bold")
screen.pack(fill=X, ipadx=8, padx=10, pady=10)


f = Frame(root, bg="grey")
b = Button(f, text="9",padx=20,pady=20, font="lucida 35 bold")
b.pack(side=LEFT)
b.bind("<Button-1>", click)

b = Button(f, text="8",padx=20,pady=20, font="lucida 35 bold")
b.pack(side=LEFT)
b.bind("<Button-1>", click)

b = Button(f, text="7",padx=20,pady=20, font="lucida 35 bold")
b.pack(side=LEFT)
b.bind("<Button-1>", click)

f.pack()


f = Frame(root, bg="grey")
b = Button(f, text="6",padx=20,pady=20, font="lucida 35 bold")
b.pack(side=LEFT)
b.bind("<Button-1>", click)

b = Button(f, text="5",padx=20,pady=20, font="lucida 35 bold")
b.pack(side=LEFT)
b.bind("<Button-1>", click)

b = Button(f, text="4",padx=20,pady=20, font="lucida 35 bold")
b.pack(side=LEFT)
b.bind("<Button-1>", click)

f.pack()


f = Frame(root, bg="grey")
b = Button(f, text="3",padx=20,pady=20, font="lucida 35 bold")
b.pack(side=LEFT)
b.bind("<Button-1>", click)

b = Button(f, text="2",padx=20,pady=20, font="lucida 35 bold")
b.pack(side=LEFT)
b.bind("<Button-1>", click)

b = Button(f, text="1",padx=20,pady=20, font="lucida 35 bold")
b.pack(side=LEFT)
b.bind("<Button-1>", click)

f.pack()

f = Frame(root, bg="grey")
b = Button(f, text="0",padx=20,pady=20, font="lucida 35 bold")
b.pack(side=LEFT)
b.bind("<Button-1>", click)

b = Button(f, text="-",padx=20,pady=20, font="lucida 35 bold")
b.pack(side=LEFT)
b.bind("<Button-1>", click)

b = Button(f, text="x",padx=20,pady=20, font="lucida 35 bold")
b.pack(side=LEFT)
b.bind("<Button-1>", click)

f.pack()

f = Frame(root, bg="grey")
b = Button(f, text="/",padx=20,pady=20, font="lucida 35 bold")
b.pack(side=LEFT)
b.bind("<Button-1>", click)

b = Button(f, text="%",padx=20,pady=20, font="lucida 35 bold")
b.pack(side=LEFT)
b.bind("<Button-1>", click)

b = Button(f, text="=",padx=20,pady=20, font="lucida 35 bold")
b.pack(side=LEFT)
b.bind("<Button-1>", click)

f.pack()

f = Frame(root, bg="grey")
b = Button(f, text="C",padx=20,pady=20, font="lucida 35 bold")
b.pack(side=LEFT)
b.bind("<Button-1>", click)

b = Button(f, text=".",padx=20,pady=20, font="lucida 35 bold")
b.pack(side=LEFT)
b.bind("<Button-1>", click)

b = Button(f, text="00",padx=20,pady=20, font="lucida 35 bold")
b.pack(side=LEFT)
b.bind("<Button-1>", click)

f.pack()


root.mainloop()