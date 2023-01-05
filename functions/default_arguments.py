def average(a=9, b=1):#default arguments
    print("The average is ", (a+b)/2)

print("============= Default arguments ==================")
# average(2,3)
average() # for default arguments,  but if we give values, then it will ignore default values of arguments and will execute it according to give values like bellow : 
average(3,8)
# if I want to give only value of 'a' and not 'b' then:
average(3) # it will give 3 to 'a' and 'b' will by default
# if I want to give only value of 'b' and not 'a' then:
average(b=3) # it will give 3 to 'b' and 'a' will by default