import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

r.set("session:123", "user=alice")
r.expire("session:123", 60)

print(r.get("session:123"))

r.hset("user:alice", mapping={"age": 30, "country": "IL"})
print(r.hgetall("user:alice"))
