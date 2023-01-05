def average(*numbers):
    #like varargs in java
    # it will take 'numbers' like tupel. check it like below:
    print(type(numbers))
    sum = 0
    for i in numbers:
        sum = sum + i
    print("Average is : ", sum/len(numbers))

average(2, 3)