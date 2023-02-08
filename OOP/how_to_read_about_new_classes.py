class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.version = 1
#1. to see all methods a class contains(dir)
x = [1,2,3]
print(dir(x))
#2. to find help about a function
print(x.__add__)

#3. to get all variables in constructors in form of dictionary(that are used with self keyword)(dict)
p = Person("John", 78)
print(p.__dict__)

#4. to get complete help about a class
print(help(Person))