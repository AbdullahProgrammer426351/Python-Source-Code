f = open('mf.txt', 'r')
# readline is used to read file line by line
while True:
    line = f.readline()
    if not line:
        #when line will not available(i.e) file will end
        break
    print(line)
f.close()