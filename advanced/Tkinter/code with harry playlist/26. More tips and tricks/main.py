from tkinter import *
root = Tk()
root.geometry("555x333")
root.title("Amazing tricks")

# changing icon located on left of title
root.wm_iconbitmap("desktop.ico")

# configuration of root window
root.configure(background="grey")


# getting laptop/PC screen height and width
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

print(f"{width}x{height}")


# destroying window
Button(text="Close", command=root.destroy).pack()

root.mainloop()