x = int(input("Enter the value of x : "))
# it is like switch case in other languages like c, c++, java etc
match x:
    case 0:
        print("X is zero")
    case 4:
        print("X is 4")
    case _:
        print("Drfault case--- ")
        print(x)