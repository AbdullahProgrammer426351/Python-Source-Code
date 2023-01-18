a = input("Enter the number : ")
print(f"Multiplication table of {a} is : ")

# But what if the user entered a character instead of a number.
# to handle such type of cases, we use try catch
try:
    for i in range(1,11):
        print(f"{int(a)} X {i} = {int(a)*i}")
except Exception as e:
    print("Invalid input")
    print("error --> ",e)

print("Some other imp line of code")
print("End of the program")