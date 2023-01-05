# strings are immutable
a = "!!!Harry!!!!!!Harry"
print(a.upper())# to convert string to uppercase
# NOTE : As strings are immutable, so upper() will not change string but it will return a new string

print(a.lower()) # to convert string to lower case
print(a.rstrip("!"))# it will ignore/strip 'r' in string. But this character should be on last. Will not work for 'Harry!!!!!w'
# but will work for 'Harry!!!!!'


print(a.replace("Harry", "John"))
