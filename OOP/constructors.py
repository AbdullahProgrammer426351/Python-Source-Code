class Person:
    # making constructor
    def __init__(self, n, o):
        print("Hey I am a person")
        self.name = n
        self.occ = o
    # making functions
    def info(self):
        print(f"{self.name} is a {self.occ}")

#making object of class
a = Person("Harry", "Developer")
b = Person("Subham", "HR")

a.info()
b.info()