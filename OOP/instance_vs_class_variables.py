class Employee:
    def __init__(self, name):
        self.name = name
    def showDetails(self):
        print(f"The name of the employee is : {self.name}")

emp1 = Employee("Harry")
emp1.showDetails()

# same goal we can achieve also by doing this : 
Employee.showDetails(emp1)