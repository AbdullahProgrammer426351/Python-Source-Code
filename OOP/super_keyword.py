# super kkeyword is used to run methods of parent class in a child class
class Employee:
    def __init__(self, name, id):
        self.name = name
        self.id = id

class Programmer(Employee):
    def __init__(self, name, id, lang):
        self.lang = lang
        # self.name = name
        # self.id = id
        # instead of doing this, we can use constructor of super class
        super().__init__(name, id)
    
rohan = Employee("Rohan", "420")
harry = Programmer("Harry", "2222", "Python")