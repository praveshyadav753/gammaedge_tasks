import datetime
import json
import requests

def generate_key(endpoint):
    # key = endpoint +"/"+ parameters
    key=endpoint
    return key


def save_response( endpoint,response):
    cache = {}
    timestamp = datetime.datetime.now().isoformat()
    key = generate_key(endpoint)
    cache = load_cache_res(key)

    if cache:
        if key not in cache and response:

            data = {
                "timestamp": timestamp,
                "response": response.json()
            }
            print(data)

            cache[key] = data
            print(cache)

            with open("cache.json", "w") as f:
                json.dump(cache, f, indent=2)
            # print(data)




def load_cache_res(endpoint):
    with open("cache.json", "r") as f:
        cached = json.load(f)
        print()
    if generate_key(endpoint) in cached:
        # to add timestamp
        response_data = cached[generate_key(endpoint)]
        print(response_data.get("timestamp"))
        return response_data
    else:
        return None

def check_expiry(endpoint):
    key = generate_key(endpoint)
    with open("cache.json", "r") as f:
        cached = json.load(f)
    if key not in cached:
        return True

    timestamp_str = cached[key].get("timestamp")
    if not timestamp_str:
        return True

    timestamp = datetime.datetime.strptime(timestamp_str,"%Y-%m-%dT%H:%M:%S.%f")
    expiry = timestamp + datetime.timedelta(minutes=5)

    return datetime.datetime.now() > expiry

def clean_cache():
    with open("cache.json", "w+") as f:
        cached = json.load(f)
        for key ,value  in cached.items():
            if check_expiry(key):
                del cached[key]
        f.write(cached)
def load_all_cache():
    with open("cache.json", "r") as f:
        cached = json.load(f)
        return cached

def run_cache_manager(endpoint=None,get_response=None):
    if not endpoint and get_response:
        pass
    else:
        is_expired = check_expiry(endpoint)
        if is_expired:
            return None
        else:
            response = load_cache_res(endpoint)
            if not response:
               save_response(endpoint,get_response)
               return None
            else:
                return response


# if "__main__" == __name__:
#     url = "https://jsonplaceholder.typicode.com/todos"
#     run_cache_manager()





# genrate_key("https://google.com","fetch")
# response = requests.get("https://jsonplaceholder.typicode.com/todos/1")

url="https://jsonplaceholder.typicode.com/todos/1"
response = requests.get("https://api.restful-api.dev/objects?id=3&id=5&id=10")
# print(response.json())
save_response("https://api.restful-api.dev/objects?id=3&id=5&id=10" , response)
# value=load_cache_res(url)
# print(value)
# print(check_expiry(url))