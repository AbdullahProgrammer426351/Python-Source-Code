class Person:
    name = "Harry"
    occupation = "Software Develper"
    networth = 10
    # making functions
    def info(self):
        print(f"{self.name} is a {self.occupation}")

#making object of class
a = Person()
print(a.name)

# changing values of variables in class
a.name = "Shubham"
print(a.name)

#calling methods from class
a.info()