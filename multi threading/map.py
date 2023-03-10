from concurrent.futures  import ThreadPoolExecutor
import time

def func(seconds):
    print(f"Sleeping for {seconds} seconds")
    time.sleep(seconds)
    return seconds


def poolingDemo():
    with ThreadPoolExecutor() as executor:
        # future1 = executor.submit(func, 3)
        # future2 = executor.submit(func, 1)
        # future3 = executor.submit(func, 4)
        # print(future1.result())
        # print(future2.result())
        # print(future3.result())
        l = [3, 5, 1, 2]
        results = executor.map(func, l)
        for result in results:
            print(result)

poolingDemo()