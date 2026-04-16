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
