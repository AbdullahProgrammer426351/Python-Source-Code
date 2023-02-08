def greet(fx):
    def mfx(*args, **kwargs):
        #*args --> taking arguments as a tupel
        #**kwargs --> taking arguments as a dictionary
        print("Good Morning")
        fx(*args, **kwargs)
        print("Thanks for using this function")
    return mfx

def add(a, b):
    print(a+b)

greet(add)(1,2)


# other way if you use @greet annotation --> add(1,2)