#!python3
from pymemcache.client.base import Client

client = Client('localhost')

memKey = '/memcached'

client.set(memKey, '<HTML><H1>Hi, Memcached!</H1></HTML>')

result = client.get(memKey)

print(result)