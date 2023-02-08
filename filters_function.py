# FILTER: is used to filter elements from a list or some other collection datatype based upon some condition

def filter_function(a):
    return a>4


# filter
l = [1,2,3,4,5]
newl = list(filter(filter_function, l))
# we can also use lambda function here
print(newl)
