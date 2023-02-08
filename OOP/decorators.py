# decorators are used to modify functions. Consider you have to 
# inlcude a functionality to all functions, there you can use decorators. like:

def greet(fx):
    def mfx():
        print("Good maorning")
        fx()
        print("Thanks for using this function")
    return mfx

# adding decorator 'greet' to this method
@greet
def hellow():
    print("Hellow world")


hellow()


# if I will not mention @greet on top of 'hellow' method, 
#then there is a second way to do this:
greet(hellow)()