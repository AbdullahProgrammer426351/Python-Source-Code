import threading
import time
# multi threading is a technique used to do some tasks parallelly instead of doing them one by one

# demo function : indicates some task being done
def func(seconds):
    print(f"Sleeping for {seconds} seconds")
    time.sleep(seconds)


# Normal Code
func(4)
func(2)
func(1)

# Parallel code (Multi-threading) using threads
t1 = threading.Thread(target=func, args=[4])
t2 = threading.Thread(target=func, args=[2])
t3 = threading.Thread(target=func, args=[1])

t1.start()
t2.start()
t3.start()


# the above lines will throw task to the background. But if you want to wait for a task to end then to contiue to next lines , then you can use:
t1.join()
t2.join()
t3.join()