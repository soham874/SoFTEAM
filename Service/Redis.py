import redis, json

redis_client = redis.Redis(host='redis-server', port=6379, db=0, decode_responses=True)

def store_dict(key, my_dict):
    # Serialize dictionary to JSON and store in Redis
    redis_client.set(key, json.dumps(my_dict)) 

def get_dict(key):
    # Retrieve and deserialize the dictionary
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None

def get_list(key):
    # Retrieve and deserialize the dictionary
    return redis_client.lrange(key, 0, -1)

def increment_with_lock(key, field):
    # Acquire a lock
    lock = redis_client.lock(f"{key}_lock", timeout=5)  # Set a timeout to avoid deadlocks
    try:
        if lock.acquire(blocking=True):
            # Perform your thread-safe operation here
            redis_client.hincrby(key, field, 1)
    finally:
        # Release the lock
        lock.release()

def modify_with_lock(key, new_value):
    # Acquire a lock
    lock = redis_client.lock(f"{key}_lock", timeout=5)  # Set a timeout to avoid deadlocks
    try:
        if lock.acquire(blocking=True):
            # Perform your thread-safe operation here
            store_dict(key, new_value)
    finally:
        # Release the lock
        lock.release()
    
def append_to_list(key, new_object_to_append):
    redis_client.rpush(key, json.dumps(new_object_to_append))