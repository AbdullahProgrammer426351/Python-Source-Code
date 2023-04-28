from tkinter import *
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfilename, asksaveasfilename
import os


def newFile():
    global file
    root.title("Untitled - Notepad")
    file = None
    textarea.delete(1.0, END)
def openFile():
    global file
    file = askopenfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"),
                                                              ("Text Documents", "*.txt")])
    if file == "":
        file = None
    else:
        root.title(os.path.basename(file) + " - Notepad")
        textarea.delete(1.0, END)
        f = open(file, "r")
        textarea.insert(1.0, f.read())
        f.close()

def saveFile():
    global file
    if file == None:
        file = asksaveasfilename(initialfile= "Untitled.txt", defaultextension=".txt", filetypes=[("All Files", "*.*"),
                                                              ("Text Documents", "*.txt")])
        if file == "":
            file = None
        else:
            # Save as a new file
            f = open(file, "w")
            f.write(textarea.get(1.0, END))
            f.close()

            root.title(os.path.basename(file) + " - Notepad")
            print("File saved")
    else:
        # Save the file
            f = open(file, "w")
            f.write(textarea.get(1.0, END))
            f.close()
def quitApp():
    root.destroy()
def cut():
    textarea.event_generate("<<Cut>>")# this will automatically cut text
def copy():
    textarea.event_generate("<<Copy>>")# this will automatically copy text
def paste():
    textarea.event_generate("<<Paste>>")# this will automatically paste text
    pass
def about():
    showinfo("Notepad", "Notepad by code with harry")



if __name__ == '__main__':
    #Basic tkinter setup
    root = Tk()
    root.title("Untitled - Notepad")
    root.wm_iconbitmap("")
    root.geometry("344x488")
    # Add Text Area
    textarea = Text(root, font="lucida 13")      
    file = None# for file currently opened
    textarea.pack(fill=BOTH, expand=TRUE)

    # Let's create the menubar
    menubar = Menu(root)
    # File menu starts
    filemenu = Menu(menubar, tearoff=0)
    # To open new file
    filemenu.add_command(label="New", command=newFile)

    # To open already existing  file
    filemenu.add_command(label="Open", command=openFile)

    # To save the current file
    filemenu.add_command(label="Save", command=saveFile)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=quitApp)
    menubar.add_cascade(label="File", menu=filemenu)

    # Edit Menu starts
    editmenu = Menu(menubar, tearoff=0)
    # to give a feature of cut, copy and paste
    editmenu.add_command(label="Cut", command=cut)
    editmenu.add_command(label="Copy", command=copy)
    editmenu.add_command(label="Paste", command=paste)

    menubar.add_cascade(label="Edit", menu=editmenu)


    # Help menu starts
    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="About Notepad", command=about)
    menubar.add_cascade(label="Help", menu=helpmenu)




    root.config(menu=menubar)


    # Adding scrollbar 
    scrollbar = Scrollbar(textarea)
    scrollbar.pack(side=RIGHT, fill=Y)
    scrollbar.config(command=textarea.yview)
    textarea.config(yscrollcommand=scrollbar.set)




    root.mainloop()