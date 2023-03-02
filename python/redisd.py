#!python3
import redis

client = redis.Redis(host="localhost", port=6379, db=0)

key = "/redis"

client.set(key, "<HTML><H1>Hi, Redis!</H1></HTML>")

resp = client.get(key)

print(resp)
