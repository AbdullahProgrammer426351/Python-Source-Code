def calculateGmean(a, b):
    mean = (a*b)/(a+b)
    print(mean)

#if you want to only declare the function not to write its body, you can ye 'pass' keyword

def thisMeth():
    pass#python will generate error if we will not write this line

a = 9
b = 90
calculateGmean(a, b)