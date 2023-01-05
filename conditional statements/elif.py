num = int(input("Enter your age : "))
if(num < 0):
    print("Number is negative")
elif(num == 0):
    print("Number is zero")
elif(num == 999):
    print("Number is special")
else:
    print("Number is positive")