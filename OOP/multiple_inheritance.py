class Employee:
    def __init__(self, name):
        self.name = name
    def show(self):
        print(f"The name is {self.name}")
class Dancer:
    def __init__(self, dance):
        self.dance = dance
    def show(self):
        print(f"The dance is {self.dance}")

#class doing multiple inheritance. i.e inheriting more than one classes
class EmployeeDancer(Employee, Dancer):
    def __init__(self, name, dance):
        self.name = name
        self.dance = dance

o = EmployeeDancer("Harry", "Break Dance")

print(o.name)
print(o.dance)


# if we use below method, this method is present in both Employee and Dancer classes. Then method will called from first inherited class. If :
#EmployeeDancer(Employee, Dancer):
#then method will be called from Employee. But if :
#EmployeeDancer(Dancer, Employee):
#then method will be called from Dancer
o.show()



# if we want to check sequence of searching method. you can:
print(EmployeeDancer.mro())