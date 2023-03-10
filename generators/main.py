#generator is like a list.But a list contains values and generator contains information about generating values and it generates value on the fly using information in it.
def my_generator():
    for i in range(5):
        # it will not use return statement but will use 'yield' keyword. This will return only current value not all values which is good for performance
        yield i

gen = my_generator()


# generating next value
print(next(gen))


#printing all values
for j in gen:
    print(j)