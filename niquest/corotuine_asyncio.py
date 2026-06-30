# THREADING & MULTITHREADING

# import threading
# import time

# def task():
#     print('fuck you man!!')
# t1 = threading.Thread(target=task)
# t2 = threading.Thread(target=task)
# t2 = threading.Thread(target=task)
# t1.start()
# t2.start()
# def times(n):
#     _time.sleep(n)
#     print(f'slept for {n} seconds')
# sa = []
# for i in range(5):
#     t = threading.Thread(target=times, args=(i,))
#     t.start()
#     sa.append(t)
# for t in sa:
#     t.join()


# def task(x):
#     time.sleep(2)
#     print(f'Task {x} completed by {threading.current_thread().name}')
#     return x * 2
# from concurrent.futures import ThreadPoolExecutor
# executor = ThreadPoolExecutor(max_workers=2)
# future1 = executor.submit(task, 5)
# future2 = executor.submit(task, 5)
# future3 = executor.submit(task, 5)
# print(future1.result())
# print(future2.result())
# print(future2.done())
# print(future1.done())


# COROUTINE

# import asyncio
# import time


# def na() -> None:
#     print("na")
#     time.sleep(3)
#     print("na")

# async def no() -> None:
#     print("no-1")
#     await asyncio.sleep(1)
#     print("no1")
# async def no1() -> None:
#     print("no-2")
#     await asyncio.sleep(4)
#     print("no2")
# async def no3() -> None:
#     print("no-3")
#     await asyncio.sleep(3)
#     print("no3")
# start = time.time()

# async def test():
#     print('now')
#     await asyncio.sleep(3)
#     print('now2')
# # async def test1():
# #     print('now1')
# #     await asyncio.sleep(1)
# #     print('now12')

# async def main():
#     # await asyncio.gather(no(),no1(),no3())
#     # await asyncio.gather(test(), test1())
#     # await asyncio.gather(test(), test())

#  asyncio.run(main())
#  print(time.time()-start)
# # asyncio.run(test()) #it will first run this fun() then next test() not parallely
# # asyncio.run(test())


# # start = time.time()
# # print("na")
# # na()
# # na()
# # print(time.time() - start)

# # async def worker():
# #     print("Worker starts")
# #     await asyncio.sleep(5)
# #     print("Done")
# # async def main():
# #     asyncio.create_task(worker())
# #     print("Main continues")
# #     await asyncio.sleep(6)
# # asyncio.run(main())

# =================================================================================================================================================
# ASYNCIO

# import asyncio
# import time


# async def worker():
#     print('Worker starts')
#     await asyncio.sleep(1) # it tells i am waiting here do other work
# a=worker()
# print(a) #coroutine object so to get the coroutine use the asyncio.run() or await it in another coroutine
# asyncio.run(worker())# creates a event loop and excute the coroutine

# async def work(name, seconds):
#     print(f"{name} started")
#     await asyncio.sleep(seconds)
#     print(f"{name} finished")
#     return f"{name} finished after {seconds} seconds"
# async def main():
#     result = await asyncio.gather(
#         work("A", 3),
#         work("B", 2),
#         work("C", 1),
#     )
#     print(result)
# asyncio.run(main())

# async def square(x):
#     await asyncio.sleep(1)
#     return x * x
# async def main():
#     result = await asyncio.gather(
#         square(2),
#         square(3),
#         square(4)
#     )
#     print(result)
# asyncio.run(main())
# <=>
# async def worker():
#     await asyncio.sleep(3)
#     print("Worker finished")

# without the indepented task all have to wait till all results are ready
# async def main():
#     print("Main continues")
#     await asyncio.sleep(5)
#     p = await asyncio.gather(square(2), square(3), square(4), worker())
#     print(p)
# #asyncio.run(main()) #uncomment when want to test individually

# with the independent task worker() will run in the background and main() will continue without waiting for worker() to finish
# async def main():
#     task = asyncio.create_task(worker())
#     print("Main continues")
#     await asyncio.sleep(5)
#     p = await asyncio.gather(square(2), square(3), square(4))
#     print(p)
# #asyncio.run(main()) #uncomment when want to test individually

# async def last():
#     await asyncio.gather(main(), main1())
# asyncio.run(last())


# async def work(x):
#     await asyncio.sleep(x)
#     return x
# async def main():
#     tasks = [
#         work(3),
#         work(1),
#         work(2)
#     ]
#     for completed in asyncio.as_completed(tasks): #this will return the tasks as they are completed without waiting for all to complete
#         result = await completed
#         print(result)
# <=>
# async def main():
#     result = await asyncio.gather( #this will wait for all tasks to complete and return the results in the order they were called
#         work(3), work(1), work(2)
#     )
#     print(result)
# asyncio.run(main())

# async def worker():
#     try:
#         while True:
#             await asyncio.sleep(2)
#             print("working")
#     except asyncio.CancelledError:
#         print("Cancelled")
# async def main():
#     task = asyncio.create_task(worker())
#     await asyncio.sleep(3)
#     task.cancel()
# asyncio.run(main())

# async def slow():
#     await asyncio.sleep(3.001)
#     print("Slow function finished")
# async def main():
#     try:
#         await asyncio.wait_for(slow(), timeout=3)
#     except asyncio.TimeoutError:
#         print("Timeout!")
# asyncio.run(main())

# RUNNER:= in simple terms its a async but it will wait till the 1st task is completed then it will move to next! else it will run all the tasks parallely without waiting for any task to complete
# async def hello():
#     print("Hello")
#     await asyncio.sleep(2)
#     print("bye")
#     await asyncio.sleep(2)
# async def hello1():
#     print("Hello1")
#     await asyncio.sleep(1)
#     print("bye1")
# with asyncio.Runner() as runner:
#     runner.run(hello())
#     runner.run(hello1())

# async def setup():
#     print("Step 1: Setting up database...")
#     return "db_connection"
# async def run_app(conn):
#     print(f"Step 2: Running app with {conn}")
# async def cleanup():
#     print("Step 3: Cleaning up!")
# with asyncio.Runner() as r:
#     conn = r.run(setup())
#     r.run(run_app(conn))
#     r.run(cleanup())

# def block():
#     time.sleep(3)
#     print("Blocking function finished")
#     return "Result from blocking function"
# async def rotune():
#     print("Routine starts")
#     pa=await asyncio.to_thread(block) #convert a sync to async function and run it in a separate thread so that it doesn't block the event loop
#     print(f"Routine ends with result: {pa}")
# async def baby():
#     print("Baby starts")
#     await asyncio.sleep(1)
#     print("Baby ends")
# async def main():
#     await asyncio.gather(rotune(), baby())
# asyncio.run(main())

# class DB:
#     async def __aenter__(self):
#         print("connect")
#     async def __aexit__(self, *args):
#         print("disconnect")
# async def main():
#     async with DB():
#         print("working")
# asyncio.run(main()) #content_flow:_aenter->body->aexit so connect->working->disconnect

# async def gen():
#     for i in range(5):
#         await asyncio.sleep(1)
#         yield i
# async def main():
#     async for x in gen():
#         print(x)
# asyncio.run(main())

# queue = asyncio.Queue()
# async def producer():
#     for i in range(5):
#         await queue.put(i)
# async def consumer():
#     while True:
#         item = await queue.get()
#         print(item)
#         queue.task_done()
# async def main():
#     asyncio.create_task(consumer())
#     await producer()
# await queue.join() #only needed where task_done() is used to wait until all items are processed
# asyncio.run(main())
# <=>
# async def cooking(queue):
#     for i in range(5):
#         await asyncio.sleep(1)
#         await queue.put(f"Dish {i}")
#         print(f"Cooked Dish {i}")
# async def serving(queue):
#     while True:
#         dish = await queue.get()
#         print(f"Served {dish}")
#         queue.task_done()
# async def main():
# queue = asyncio.Queue()
# asyncio.create_task(serving(queue))
# await cooking(queue)
# await queue.join()
# await asyncio.gather(serving(queue), cooking(queue))
# asyncio.run(main())
# <=>
# async def mom(queue):
# for i in range(5):
# await asyncio.sleep(1)
# await queue.put(f"food {i}")
# print(f"Mom cooked: food {i} 🍳")
# async def babysitter(name, queue):
# while True:
# food = await queue.get()
# print(f"{name} feeding: {food} 🍼")
# await asyncio.sleep(0.5)       # feeding takes time
# queue.task_done() #wait till all are joined
# async def main():
# queue = asyncio.Queue()
# await asyncio.gather(
# mom(queue),
# babysitter("Sitter 1", queue),
# babysitter("Sitter 2", queue),  # 2 sitters, faster!
# )
# await queue.join()  # wait until all food is fed
# asyncio.run(main())

# balance=100
# lock = asyncio.Lock()
# async def withdraw(name, amount):
#     global balance
#     async with lock:
#         print(f"{name} is trying to withdraw {amount}")
#         await asyncio.sleep(1)  # Simulate processing time
#         if balance >= amount:
#             balance -= amount
#             print(f"{name} successfully withdrew {amount}. Remaining balance: {balance}")
#         else:
#             print(f"{name} failed to withdraw {amount}. Insufficient funds. Remaining balance: {balance}")
#     # print(f"{name} successfully withdrew {amount}. Remaining balance: {balance}")
# async def main():
#     await asyncio.gather(
#         withdraw("Alice", 70),
#         withdraw("Bob", 50)
#     )
# asyncio.run(main())

# server_ready = asyncio.Event()      # alarm not triggered yet
# async def server():
#     print("Server starting up... ⏳")
#     await asyncio.sleep(3)          # booting up
#     print("Server is READY! 🟢")
#     server_ready.set()              # 🚨 FIRE THE ALARM!

# async def worker(name):
#     print(f"{name} waiting for server...")
#     await server_ready.wait()       # blocks until alarm fires!
#     print(f"{name} starting work! 🚀")

# async def main():
#     await asyncio.gather(
#         server(),
#         worker("Worker A"),
#         worker("Worker B"),
#         worker("Worker C"),
#     )
# asyncio.run(main())

# ===================================================================================================================================================
# FILES
# with open("file.txt") as f:
# read=f.read()
# read=f.readline()
# print(read)
# read=f.readline()
# print(read)
# read=f.readline()
# print(read)
# read=f.readlines()
# print(read)
# for line in f:
# print(line.strip())  # for big files memory efficient(\nspaces,tabs)

# with open("file.txt", "w") as f:
#     f.write("Hello, World!\n")
#     f.write("This is a new line.\n")
#     f.write("Goodbye!\n")

# with open("file.txt", "a") as f:
#     f.write("Hello, World!\n")
#     f.write("This is a new line.\n")
#     f.write("Goodbye!\n")

# files=["hello\n","world\n","niquest\n"]
# with open("file.txt", "w") as f:
#     f.writelines(files)

# with open("file.txt") as f:
#     print(f.tell())
#     f.read(5)
#     print(f.tell())
#     f.seek(5)
#     print(f.read())
#     print(f.tell())

# import json
# with open("json.json", "r") as f:
#     data=json.load(f)
# print(data)
# data = {
#     'name': "skipper",
#     'nanana': 20
# }
# with open("json.json", "w") as f:
#     json.dump(data, f)
# print("Done")
# with open("json.json", "r") as f:
#     data=json.load(f)
# print(data)

# ==================================================================================================================================================
