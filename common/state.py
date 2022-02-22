import redis

def initiate_redis():
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    return r

def set_position_open(position_open: bool):
    r = initiate_redis()
    r.set("position_open", str(position_open))

def set_entry_price(entry_price):
    r = initiate_redis()
    r.set("entry_price", entry_price)

def get_position_open():
    r= initiate_redis()
    return r.get("position_open")

def get_entry_price():
    r = initiate_redis()
    r.get("entry_price")