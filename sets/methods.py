s1 = {1,2,5,6}
s2 = {3,6,7}

# union operation
print(s1.union(s2))# but it will not change values of s1 and s2
# if we want to update the value, then we can use update method
print(s1.update(s2))# it will add all elements of s2 to s1


# intersection
print(s1.intersection(s2))# it will not change value of s1. 
# if we want it to also update value, then:
s1.intersection_update(s2)


# symetric difference --- get elements that are not common(reverse to intersectoin)
