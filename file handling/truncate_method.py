with open('mf.txt', 'w') as f:
    f.write('Hellow world!')
    # truncate function is used to write to a file according to a specific limit. You can specify limit in bytes like:
    f.truncate(3)#this will allow only 3 bytes.
    # 'Hel' will be written in file instead of whole 'Hellow world!'