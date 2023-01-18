import abd
# we can use variables and methods of abd.py file in this file using import . import helpsus to use methods and variables of other files of python.
# if we want to import libraries and use it as short named variables, then we use 'as' keyword.
import my_abd as m


abd.welcome()
print(abd.a)

m.welcome()
print(m.a)