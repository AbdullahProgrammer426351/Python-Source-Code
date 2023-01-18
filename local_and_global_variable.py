a = 4 # global variable
def meth():
    print("Meth called")
    # a = 9#local variable
    # but if we want to change value of global variable then we can do this like:
    global a
    a = 999
print(a)
meth()
print(a)