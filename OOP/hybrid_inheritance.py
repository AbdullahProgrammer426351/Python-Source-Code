#combining of two or more inheritances is called hybrid inheritance.like used in Derived3 class.
class BaseClass:
    pass
class Derived1(BaseClass):
    pass
class Derived2(BaseClass):
    pass
class Derived3(Derived1, Derived2):
    pass