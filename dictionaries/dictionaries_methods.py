ep1 = {122:45, 123:89, 567:69, 670:69}
ep2 = {222:67, 566:90}

#1. update 
ep1.update(ep2)

#2. clear
# ep1.clear()
#3. pop -- to remove value with key
ep1.pop(122)
#4. popitem -- to remove last value
ep1.popitem()
#5. del --- to delete dictionary
# del ep1
print(ep1)
