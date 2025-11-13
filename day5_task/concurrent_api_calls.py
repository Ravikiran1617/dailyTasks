import asyncio
import aiohttp
import time

#  free fake APIS
APIS = [
    "https://jsonplaceholder.typicode.com/posts/1",
    "https://jsonplaceholder.typicode.com/posts/2",
    "https://jsonplaceholder.typicode.com/posts/3",
    "https://jsonplaceholder.typicode.com/users/1",
    "https://jsonplaceholder.typicode.com/users/2",
]

# Sequential approach - calls one after another
def sequential_calls():
    """Make API calls one at a time (slower)"""
    import requests
    
    print("Starting SEQUENTIAL calls...")
    start = time.time()
    results = []
    
    for url in APIS:
        response = requests.get(url)
        results.append(response.json())
        print(f"Fetched: {url}")
    
    elapsed = time.time() - start
    print(f"Sequential time: {elapsed:.2f} seconds\n")
    return results

# Concurrent approach - calls all at once
async def fetch_url(session, url):
    """Fetch a single URL"""
    async with session.get(url) as response:
        
        data = await response.json()     #here it waits for the data   
        print(f"Fetched: {url}")
        return data

async def concurrent_calls():
    """Make API calls concurrently (faster)"""
    print("Starting CONCURRENT calls...")
    start = time.time()
    
    async with aiohttp.ClientSession() as session:
        # Create tasks for all URLs
        tasks = [fetch_url(session, url) for url in APIS]   #just creates the co-rotine objects
        
        results = await asyncio.gather(*tasks)  #here the fetch_url calls will done 
    
    elapsed = time.time() - start
    print(f"Concurrent time: {elapsed:.2f} seconds\n")
    return results

if __name__ == "__main__":
    print("=" * 60)
    print("COMPARING SEQUENTIAL VS CONCURRENT API CALLS")
    print("=" * 60 + "\n")
    
    sequential_calls()

    asyncio.run(concurrent_calls())
    
    print("=" * 60)
    print("💡 Notice how concurrent calls are much faster!")
    print("=" * 60)

    