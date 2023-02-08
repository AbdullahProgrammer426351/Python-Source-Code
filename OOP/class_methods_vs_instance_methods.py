class Employee:
    company = "Apple"
    def __init__(self, name):
        self.name = name
    @classmethod
    def changeCompany(self, newCompany):
        # if we want to change class variable not instance variable , then we will add an annotation on it @classmethod
        self.company = newCompany
    
    def show(self):
        print(f"name --> {self.name} and company --> {self.company}")
    


e1 = Employee("Harry")
e1.show()
e1.changeCompany("Tesla")# this will only change company name of this instance check is on line 19 and 20. But if we add @classmethod decorator, we will succeed
e1.show()
print(Employee.company)#class variable
print(e1.company)#instance variable