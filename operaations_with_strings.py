names = "Harry, Shubham"
#1. strings slicing
print(names[0:6])# it will print 'Harry'. including 0 but not 6
# it will slice string from 0th index to exclusive 6th (inclusive 5th) index


# if we don't write '0' as starter index of slicing, then python will automatically write zero
print(names[:5])
# if we don't write ender index of slicing, python will automatically write length of string there
print(names[3:])

# if we give ender index in negative then,
print(names[0:-4])
# it will deal it as : names[0:len(names)-4]


#2. length of string
print(len(names))
