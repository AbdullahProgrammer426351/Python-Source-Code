from tkinter import *

def getVals():
    print("Submiting form")


    print(f"{nameValue.get()}, {phoneValue.get()}, {genderValue.get()}, {emergencyValue.get()}, {payomentmodeValue.get()}, {foodServiceValue.get()},")


    with open("records.txt","a") as f:
        f.write(f"{nameValue.get()}, {phoneValue.get()}, {genderValue.get()}, {emergencyValue.get()}, {payomentmodeValue.get()}, {foodServiceValue.get()}\n")

root = Tk()
root.geometry("644x344")
Label(root, text="Welcome to Harry Travels", font="comicsansms 13 bold"
      , pady=5).grid(row=0, column=3)
name = Label(root, text="Name")
phone = Label(root, text="Phone")
gender = Label(root, text="Gender")
emergency = Label(root, text="Emergency Contact")
paymentmode = Label(root, text="Payment Mode")


name.grid(row=1, column=2)
phone.grid(row=2, column=2)
emergency.grid(row=3, column=2)
gender.grid(row=4, column=2)
paymentmode.grid(row=5, column=2)


nameValue = StringVar()
phoneValue = StringVar()
genderValue = StringVar()
emergencyValue = StringVar()
payomentmodeValue = StringVar()
foodServiceValue = IntVar()


nameentry = Entry(root, textvariable=nameValue)
phoneentry = Entry(root, textvariable=phoneValue)
genderentry = Entry(root, textvariable=genderValue)
emergencyentry = Entry(root, textvariable=emergencyValue)
paymentmethodentry = Entry(root, textvariable=payomentmodeValue)


nameentry.grid(row=1, column=3)
phoneentry.grid(row=2, column=3)
genderentry.grid(row=3, column=3)
emergencyentry.grid(row=4, column=3)
paymentmethodentry.grid(row=5, column=3)

# making checkbox and packing it
foodService = Checkbutton(text="Want to prebook your meals?", variable=foodServiceValue)
foodService.grid(row=6, column=3)

# making button, packing it and assigning it a command
Button(text="Submit To Harry Travels", command=getVals).grid(row=7, column=3)
root.mainloop()