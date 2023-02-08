import os
def renameMethod(folderPath, extension):
    files = os.listdir(folderPath)
    for i in range(len(files)):
        if (str(files[i]).endswith(extension)):
            os.rename(folderPath+files[i],folderPath+str(i)+extension)
        print(f"{files[i]} --> {str(i)+extension}")
folderPath = 'pics/'
fileName = ".jpg"
renameMethod(folderPath, ".jpg")