import redis
import json

def initiate_redis(decode=True):
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=decode)
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

def add_open_position(uuid, symbol, quantity, entry_time):
    r = initiate_redis()
    r.hset("open_positions",uuid,json.dumps({"symbol":symbol, "quantity":quantity,"entry_time":entry_time}))

def get_open_positions():
    r = initiate_redis()
    return r.hgetall("open_positions")
