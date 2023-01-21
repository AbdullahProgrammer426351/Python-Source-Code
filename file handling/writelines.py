# writelines is used to write lines to a file
f = open('mf.txt', 'w')
lines = ['line1\n', 'line2\n', 'line3\n','line4\n']
f.writelines(lines)
f.close()