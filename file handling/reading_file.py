# to open file
f = open('myfile.txt', 'r')
#                       |_________________ 
# means file is opening for reading     <_|

# print(f)

# reading file
text = f.read()
print(text)
# closing file
f.close()