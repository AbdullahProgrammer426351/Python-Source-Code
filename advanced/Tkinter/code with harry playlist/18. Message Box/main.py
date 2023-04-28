from tkinter import *
import tkinter.messagebox as tmsg

def help():
    tmsg.showinfo("Help", "Harry will help you with this gui")

def experience():
    value = tmsg.askquestion(title="Was your experience good?", message="You used this app. Share your experience with us", )
    print(value)
    if value == "yes":
        msg = "Greate... Rate us on appstore please."
    else:
        msg = "Tell us what went wrong.. We will try to resolve it soon..."
    tmsg.showinfo("Experience", msg)

def askpayment():
    ans = tmsg.askretrycancel("Problem Occured : ", "Would you like to retry?")
    if ans:
        print("Retrying... ")
    else:
        print("Retrying canceled")

root = Tk()
root.geometry("333x222")

Button(text="Click for help", command=help).pack()
Button(text="How was your experience", command=experience).pack()
Button(text="Retry", command=askpayment).pack()
root.mainloop()
