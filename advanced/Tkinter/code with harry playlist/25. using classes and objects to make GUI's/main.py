from tkinter import *

class GUI(Tk):
    def __init__(self):
        # root is replaced by self
        
        # calling constructor of super class
        super.__init__()
        self.geometry("744x377")
    def status(self):
        self.var = StringVar()
        self.var.set("Ready")
        self.statusbar = Label(self, textvariable=self.var, relief=SUNKEN, anchor='w')
        self.statusbar.pack(side=BOTTOM, fill=X)
    def createButton(self, inptext):
        Button(text=inptext, command=self.click).pack()
    
    def click(self):
        print("Button Clicked")

if __name__ == '__main__':
    # root is replaced by window
    window = GUI()
    window.status()
    window.createButton("Click Me")
    window.mainloop

# root = Tk()
# root.geometry("555x33")
# root.title("Using classes and obj's")
# root.mainloop()