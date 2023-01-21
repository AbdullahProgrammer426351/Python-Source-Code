# with the use of 'with' keyword. we have not to close the file like : f.close()

with open('myfile.txt', 'a') as f:
    f.write("\ndata added with w")