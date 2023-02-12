#magic or dunder methods have special purposes and they are started and ended with double underscores like __init__() , __len__() etc.

class Employee:
    name = "Harry"
    def __len__(self):# method to return length of object
        i = 0
        for c in self.name:
            i = i+1
        return i
    def __str__(self):
        return f"The name of employee is {self.name}. \nAnd this is str method"
    def __repr__(self):
        return f"The name of employee is {self.name}. \nAnd this is repr method"
    def __call__(self):
        print("Hey this is call method")

e = Employee()
print(e.name)

print(len(e))# if we have not defined __len__() method in class, it will give error

print(e)#<__main__.Employee object at 0x000002257BB6BFA0> will print if we have not defined __str__() method in python. But if we have defined this method in class, returned string of this method will be printed. And If we have not defined __str__() it will search for __repr__() method and if both methods are not given, it will print value like above

# You can also call above two mentioned methods like this:
print(str(e))
print(repr(e))
e()# this will search for __call__() method, if there will be not , it will give error