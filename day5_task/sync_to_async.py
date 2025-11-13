# sync code
import time

def fetch_data():
    time.sleep(2)
    return "Data fetched!"

def main():
    print(fetch_data())
    print("Done")

main()

#async code
# import asyncio

# async def fetch_data():
#     await asyncio.sleep(2)
#     return "Data fetched!"

# async def main():
#     print(await fetch_data())
#     print("Done")

# asyncio.run(main())
