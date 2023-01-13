l = [1,2,3,4]

# 1. append method (to insert element at the end of list)
l.append(6)

# 2. sotring list in forward order
l.sort()
# 3. sorting list in reverse order
l.sort(reverse=True)

#4. reverse the original list
l.reverse()

#5. count the occurence of a value in list
print(l.count(1))

# 6. adding another list at the end of one list
newList = [222,333,444]
l.extend(newList)

# 7. concatinating two lists
k = l + newList
print("Concatenated list --> ", k)
print(l)