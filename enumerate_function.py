marks = [11,22,33,44,55]



#  old method for performing sepecific task for specific index
# index = 0
# for mark in marks:
#     print(mark)
#     if (index == 3):
#         print("Harry awesome")
#     index += 1



for index,mark in enumerate(marks):
    # you can also give specific value to index variable like below, then:
#for index,mark in enumerate(marks, start=1):
    print(mark)
    if (index == 3):
        print("Harry awesome")