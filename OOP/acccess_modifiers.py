class Parent:
    def __init__(self):
        self.__name = "Harry"#private due to __
        self._job = "Programmer"#protected due to _
        self.id = 22#public by default