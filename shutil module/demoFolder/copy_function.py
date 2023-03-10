import shutil as sh

# this will copy content file from first argument file name and then will create copy of this file into new file of which name we have to give as second argument
sh.copy("copy_function.py", "copied.py")



# like this, there is also a method of name : copy2. This is also same like copy method but it also sends meta data about time of creation of file etc.