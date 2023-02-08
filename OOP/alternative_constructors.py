class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
    @classmethod
    def fromStr(cls, str):
        #cls --- > is same as self
        return cls(str.split("-")[0],str.split("-")[1])


# using construtor 1
e1 = Employee("Harry", 12000)
print(e1.name)
print(e1.salary)


# using construtor 2
string = "John-9999"
e2 = Employee(string.split("-")[0], string.split("-")[1])
print(e2.name)
print(e2.salary)