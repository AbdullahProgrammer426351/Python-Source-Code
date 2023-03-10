import re

# regular expressions are made for complex matching purposes. For general and simple matchings, in , is etc keywords should be used. This is only for complex matchings.

# pattern = "in"
pattern = r"[A-Z]+cyclone"# for finding all regular words which start from capital letters

text = '''
regular expressions are made for complex matching purposes. For general and simple matchings, in , is etc keywords should be used. This is only for complex matchings. Regular
'''

# suppose that I want to search a word (value of pattern variable)
# in a given paragraph (value of text variable). We have to write like:
match = re.search(pattern, text)#search for only first occurence
matches = re.finditer(pattern, text)#find all occurences
print(match)

for match in matches:
    print(match)