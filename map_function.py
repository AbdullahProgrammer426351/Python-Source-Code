# MAP: is used to apply some method to all elements of a list or some other collection datatype and return 'map' datatype. It takes two parameters first : method that we want to apply and second : list on the elements of which we want to apply some function
def cube(x):
    return x*x*x

print(cube(2))

# but it we want to take cube o all items in a list, then:

l = [1,2,3,4,5]

# --- old way ---
# newl = []
# for item in l:
#     newl.append(cube(item))



# ---- smart way (with maps) ------

newl = list(map(cube, l))
# we can also use lambda function here
print(newl)