from tkinter import *
import tkinter.messagebox as msbx
def claimDollars():
    print(f"We have sent {slider.get()} dollars to your bank account")
    msbx.showinfo("Amount Sent : ", f"We have sent {slider.get()} dollars to your bank account")
root = Tk()
root.geometry("444x333")
Label(root,text="How many dollars do you want?").pack()
Button(root, text="Get Dollars!", command=claimDollars).pack()
slider = Scale(from_=0, to=100, orient=HORIZONTAL, tickinterval=50)
# set initial value
slider.set(33)

# if you want to set intervals

slider.pack()
root.mainloop()