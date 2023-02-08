class MyClass:
    def __init__(self, value):
        self._value = value
    def show(self):
        print(f"Value is {self._value}")
    # getter
    @property
    def ten_value(self):
        return 10*self._value

    # setter 
    @ten_value.setter
    def ten_value(self, new_value):
        self._value = new_value/10


obj = MyClass(10)
#using setter
obj.ten_value = 67
#using getter
print(obj.ten_value)
obj.show()