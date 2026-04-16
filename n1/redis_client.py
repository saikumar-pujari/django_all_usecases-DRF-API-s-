from redis.sentinel import Sentinel

# Connect to Sentinel
sentinel = Sentinel(
    [('127.0.0.1', 26379),
     #  ('127.0.0.1', 26380),
     #  ('127.0.0.1', 26381)
     ],  # Sentinel address

    socket_timeout=0.5
)


def get_redis_master():
    return sentinel.master_for(
        service_name='mymaster',
        socket_timeout=0.5,
        retry_on_timeout=True
    )


def get_redis_slave():
    return sentinel.slave_for(
        service_name='mymaster',
        socket_timeout=0.5,
        retry_on_timeout=True
    )

# core/redis_client.py(production code)

# from django_redis import get_redis_connection

# def get_redis():
#     return get_redis_connection("default")

# usage file

# from core.redis_client import get_redis
# r = get_redis()
# r.set("hello", "world")
# print(r.get("hello"))
# r.zadd("leaderboard", {"sai": 100})

# r.set("name", "sai")
# print(r.get("name"))

# # left push (latest first)
# r.lpush("recent_users", "sai")
# r.lpush("recent_users", "rahul")
# r.lrange("recent_users", 0, -1)

# r.hset("user:1", mapping={
#     "name": "sai",
#     "age": "22",
#     "city": "davangere"
# })
# r.hgetall("user:1")
# r.delete("user:1")

# r.sadd("tags", "django")
# r.sadd("tags", "redis")
# r.sadd("tags", "django")  # ignored
# r.smembers("tags")

# r.zadd("leaderboard", {
#     "sai": 100,
#     "rahul": 200,
#     "john": 150
# })
# # top users (highest score first)
# r.zrevrange("leaderboard", 0, -1, withscores=True)

# r.incr("page_views")
# r.decr("stock")



