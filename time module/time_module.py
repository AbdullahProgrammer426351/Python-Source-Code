import time

def usingWhile():
    i = 0
    while i< 500:
        i = i+1
        print("while -- ", i)
def usingFor():
    for i in range(500):
        print("for --- ", i)

# our objective is to find the times taken by for and while loops during execution
init = time.time()

usingWhile()

print(time.time() - init)# subtracting total time with old time to find difference


usingFor()
print(time.time() - init)# subtracting total time with old time to find difference