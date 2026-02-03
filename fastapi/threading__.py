import time
import requests
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import asyncio
# import aiohttp
from tqdm import tqdm

def download_content(url: str) -> bool:
    """Blocking version of download_content, get response, then return."""
    try:
        _ = requests.get(url)
        return True
    except Exception:
        return False
async def adownload_content(session, url: str) -> bool:
    """Non-blocking version of download_content, return while waiting for response."""
    try:
        async with session.get(url) as response:
            _ = await response.read()
            return True
    except Exception:
        return False
def generate_urls(base_url: str, count: int) -> list:
    """Generate a list of URLs for testing."""
    return [f"{base_url}/delay/1" for _ in range(count)]

def run_single_threaded(urls: list) -> None:
    """Single-threaded version of download_content."""
    count = 0
    print("---- Starting single-threaded download ----")
    start_time = time.time()
    for url in tqdm(urls, desc="Single-threaded"):
        if download_content(url):
            count += 1
    time_diff = time.time() - start_time
    print(f"Single-threaded: {count} requests done in {time_diff:.2f} seconds")

def run_process_pool(task_ids, max_workers=4):
    start = time.time()
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        list(executor.map(pure_python_task, task_ids))
    end = time.time()
    print(f"ProcessPoolExecutor: {len(task_ids)} tasks in {end-start:.2f}s")
    return end - start

run_single_threaded(["https://jsonplaceholder.typicode.com/todos/1","https://api.restful-api.dev/objects","https://api.restful-api.dev/objects?id=3&id=5&id=10"])
t_process = run_process_pool(list(range(100)), max_workers=4)
