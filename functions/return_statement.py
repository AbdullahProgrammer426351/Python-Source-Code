def average(*numbers):
    print(type(numbers))
    sum = 0
    for i in numbers:
        sum = sum + i
    return sum/len(numbers)

    # if we use more than one return statements, first will be executed and others will be ignored

c = average(2, 3)
print(c)