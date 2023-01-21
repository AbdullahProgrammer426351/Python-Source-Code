with open('mf.txt', 'r') as f:
    print(type(f))
    # seek method helps us to directly jump to the nth byte in a file. like:
    # we move to the 10th byte in the file
    f.seek(10)


    # if we want to check that from where we have adjusted seek , 
    # we can use tell() method to check it
    print("current position --> ", f.tell())
    # read the next 5 bytes
    data = f.read(5)
    print(data)