class Employee:
    def __init__(self, name, id):
        self.name = name
        self.id = id

    def showDetails(self):
        print(f"The name of Employee:{self.id} is {self.name}")


# Programmer class inheriting Employee
class Programmer(Employee):
    def showLanguage(self):
        print("The default language is Python")

e1 = Employee("Rohan", 420)
e1.showDetails()
e2 = Programmer("Harry", 333)
e2.showLanguage()