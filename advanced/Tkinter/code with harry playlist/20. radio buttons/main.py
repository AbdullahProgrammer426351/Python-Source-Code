from tkinter import *

def orderNow():
    print("you selected : " + var.get())

root = Tk()
root.geometry("444x222")
root.title("Radiobutton tutorial")

# var = IntVar() --- for giving integer values
# var.set(1) --> if you want to set it by default
var = StringVar()
var.set("kkk")
Label(root, text="What would you like to have sir?").pack()


# for giving integer values
# radio = Radiobutton(root, text="Dosa", variable=var, value=1, anchor="w").pack()
# radio = Radiobutton(root, text="Idly", variable=var, value=2, anchor="w").pack()
# radio = Radiobutton(root, text="Paratha", variable=var, value=3, anchor="w").pack()
# radio = Radiobutton(root, text="Samosa", variable=var, value=4, anchor="w").pack()


# for giving string values
radio = Radiobutton(root, text="Dosa", variable=var, value="Dosa", anchor="w").pack()
radio = Radiobutton(root, text="Idly", variable=var, value="Idly", anchor="w").pack()
radio = Radiobutton(root, text="Paratha", variable=var, value="Paratha", anchor="w").pack()
radio = Radiobutton(root, text="Samosa", variable=var, value="Samosa", anchor="w").pack()

Button(text="Order Now!", command=orderNow).pack()
root.mainloop()