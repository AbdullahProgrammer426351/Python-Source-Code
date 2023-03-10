import asyncio
import time
#asyncIO is a module used to run functions parallelly instead of executing them one by one

async def fun1():
    time.sleep(2)
    print("Fun 1")

async def fun2():
    time.sleep(2)
    print("Fun 2")

async def fun3():
    time.sleep(2)
    print("Fun 3")
async def main():
    L = await asyncio.gather(
        fun1(), fun2(), fun3(),
    )
    print(L)

asyncio.run(main())
