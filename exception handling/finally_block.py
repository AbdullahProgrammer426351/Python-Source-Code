def getVal():
    l = [1,2,3,4]
    try:
        a = int(input("Enter index number : "))
        return l[a]
    except:
        return 0
    finally:
        # this block will be executed irrespective of return statement
        print("I am always executed")

x = getVal()
print(x)