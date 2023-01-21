# appending file
f = open('myfile.txt', 'a')
f.write("Appended data")
f.close()
# this will not remove previous data but will add data after previous/existing data