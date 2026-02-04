import time
from functools import lru_cache,wraps
import requests
from collections import Counter
import json
from random import randint
from collections import deque
class RateLimitError(Exception):
    """Rate limit exceeded."""
class MAXretry(Exception):
    "max retry"

class APIClient:
    def __init__(self):
        self.req_count = 0

    def rate_limiter(self,max_call: int, period: int):
        def decorator(func):
            calls = deque()

            @wraps(func)
            def wrapper(*args, **kwargs):
                self.timer = time.time()

                while calls and calls[0] <= self.timer - period:
                    calls.popleft()
                if len(calls) >= max_call:
                    metrics.rate_limit_violations += 1
                    metrics.total_requests += 1
                    print("Limitt exceeded")
                    return
                print(len(calls))
                calls.append(self.timer)
                result = func(*args, **kwargs)
                print("Request executed...",result)
                return result

            return wrapper

        return decorator


    def backoff(self,delay=2, retries=5):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                current_retry_count = 0
                current_delay = delay
                start= time.time()
                metrics.total_requests += 1
                while current_retry_count < retries:
                    try:
                        result = func(*args, **kwargs)
                        metrics.response_times.append(time.time() - start)
                        metrics.successful_requests += 1
                        return  result

                    except Exception as e:
                        current_retry_count += 1
                        if current_retry_count >= retries:
                            print("error and break")
                            metrics.response_times.append(time.time() - start)
                            metrics.failed_requests+=1
                            raise MAXretry
                        print(f"Failed to execute function '{func.__name__}'. Retrying in {current_delay} seconds...")
                        time.sleep(current_delay)
                        current_delay *= 2


            return wrapper
        return decorator

    def lru_with_ttl( self,ttl_seconds, maxsize=128):
        def decor(fun):
            @lru_cache(maxsize=maxsize)
            def cached_with_ttl(*args, ttl_hash, **kwargs):
                return fun(*args, **kwargs)

            def inner(*args, **kwargs):

                return cached_with_ttl(*args, ttl_hash=round(time.time() / ttl_seconds), **kwargs)

            inner.cache_info = cached_with_ttl.cache_info
            print("cahe:",inner.cache_info)
            inner.cache_clear = cached_with_ttl.cache_clear
            return inner
        return decor


class APIMetrics:
    def __init__(self):
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.rate_limit_violations = 0
        self.response_times = []
        self.errors = Counter()
        self.cache_hits = 0
        self.cache_misses = 0

    @property
    def avg_response_time(self):
        if not self.response_times:
            return 0
        return sum(self.response_times) / len(self.response_times)

    @property
    def cache_hit_ratio(self):
        self.cachedata=api.fetch_data.cache_info()
        self.hits =self.cachedata.hits
        self.missed = self.cachedata.misses
        self.total = self.hits + self.missed
        return (self.hits / self.total) * 100 if self.total > 0 else 0

    def generate_report(self):
        return {
            "Traffic": {
                "Total": self.total_requests,
                "Success": self.successful_requests,
                "Failed": self.failed_requests
            },
            "Performance": {
                "Avg Latency": f"{self.avg_response_time:.4f}s",
                "Cache Hit Ratio": f"{self.cache_hit_ratio:.2f}%"
            },
            "Issues": {
                "Rate Limit Violations": self.rate_limit_violations,
                "Error Breakdown": dict(self.errors)
            },
            "response times":{
                'time:' :self.response_times
            }
        }


metrics = APIMetrics()
client = APIClient()

class MyAPI:

    @client.rate_limiter(max_call=5, period=60)
    @client.backoff(delay=2, retries=5)
    @client.lru_with_ttl(ttl_seconds=60)
    def fetch_data(self, user_id):
        print(f"Fetching data for {user_id}...")
        time.sleep(1)
        if(randint(1,10)<6):
            raise
        return {"id": user_id, "data": "sample"}

# Test Execution
api = MyAPI()
for i in range(0,6):
    # print(api.fetch_data(user_id=i))

    print(api.fetch_data(user_id=i))
    print(api.fetch_data(user_id=0))
    # api.fetch_data.cache_info()
    # time.sleep(randint(1,2))
    # print(api.fetch_data(user_id=3))
    # time.sleep(randint(1, 3))
print(api.fetch_data.cache_info())

print(json.dumps(metrics.generate_report(), indent=4))
