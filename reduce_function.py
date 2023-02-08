# REDUCE : function is used to apply a function on two values in a list or some other collection datatype. Then it will apply same operation on result and value on next index. We have to import it to use.
from functools import reduce

numbers = [1,2,3,4,5]
# ------------ dry run -------------------
# [1,2,3,4,5]
# 1+2
# [3,3,4,5]
# 3+3
# [6,4,5]
# 6+4
# [10,5]
# 10+5
# [15]

sum = reduce(lambda x, y:x+y, numbers)

print(sum)