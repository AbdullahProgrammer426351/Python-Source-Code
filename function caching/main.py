from functools import lru_cache
import time

@lru_cache(maxsize=None)
def fx(n):
    time.sleep(5)
    return n*5

print(fx(20))
print("Done for 20")

print(fx(2))
print("Done for 2")


print(fx(6))
print("Done for 6")


# when we will repeat it for these values, it will not take time because it has already stored their caalculation

print(fx(20))
print("Done for 20")

print(fx(2))
print("Done for 2")


print(fx(6))
print("Done for 6")