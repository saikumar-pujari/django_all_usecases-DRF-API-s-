import json
from django.db import transaction
from .models import na
from .redis_client import get_redis_master, get_redis_slave

CACHE_TTL = 60


def get_na(na_id):
    cache_key = f"na:{na_id}"

    redis_slave = get_redis_slave()
    redis_master = get_redis_master()

    # 🔹 1. Try SLAVE (fast read)
    try:
        cached_data = redis_slave.get(cache_key)
        if cached_data:
            print("✅ Cache HIT (slave)")
            return json.loads(cached_data)
    except Exception:
        print("⚠️ Slave read failed, fallback to master")

    # 🔸 2. Fallback to MASTER cache
    try:
        cached_data = redis_master.get(cache_key)
        if cached_data:
            print("✅ Cache HIT (master)")
            return json.loads(cached_data)
    except Exception:
        print("⚠️ Master cache read failed")

    # 🔻 3. Fetch from DB
    print("❌ Cache MISS → DB hit")
    try:
        na = na.objects.get(id=na_id)
    except na.DoesNotExist:
        return None

    data = {
        "id": na.id,
        "name": na.name,
        "price": na.price,
    }

    # 🔹 4. Store in MASTER (important!)
    try:
        redis_master.setex(cache_key, CACHE_TTL, json.dumps(data))
    except Exception:
        print("⚠️ Cache write failed")

    return data


def create_na(name, price):
    redis_master = get_redis_master()

    # Save in DB
    with transaction.atomic():
        na = na.objects.create(name=name, price=price)

    # Cache it immediately
    cache_key = f"na:{na.id}"
    data = {
        "id": na.id,
        "name": na.name,
        "price": na.price,
    }

    try:
        redis_master.setex(cache_key, CACHE_TTL, json.dumps(data))
    except Exception:
        print("⚠️ Cache write failed")

    return na


from django_redis import get_redis_connection

r = get_redis_connection("default")


class WalletService:

    @staticmethod
    def set_balance(user_id, amount):
        """
        Initialize or reset balance
        """
        r.set(f"wallet:{user_id}", amount)

    @staticmethod
    def get_balance(user_id):
        balance = r.get(f"wallet:{user_id}")
        return int(balance) if balance else 0

    @staticmethod
    def deduct_balance(user_id, amount):
        """
        Deduct money safely using Redis transaction
        """
        key = f"wallet:{user_id}"

        with r.pipeline() as pipe:
            while True:
                try:
                    # 1. Watch the key
                    pipe.watch(key)

                    # 2. Read current balance
                    balance = pipe.get(key)
                    balance = int(balance) if balance else 0

                    # 3. Check condition
                    if balance < amount:
                        pipe.unwatch()
                        return {
                            "status": False,
                            "message": "Insufficient balance"
                        }

                    # 4. Start transaction
                    pipe.multi()

                    # 5. Update balance
                    pipe.set(key, balance - amount)

                    # 6. Execute
                    pipe.execute()

                    return {
                        "status": True,
                        "message": "Deducted successfully",
                        "remaining_balance": balance - amount
                    }

                except Exception:
                    # Retry if another request modified the key
                    continue




# from django_redis import get_redis_connection
# r = get_redis_connection("default")


# def deduct_balance(user_id, amount):
#     script = """
#     local key = KEYS[1]
#     local amount = tonumber(ARGV[1])

#     local balance = tonumber(redis.call('GET', key) or "0")

#     if balance < amount then
#         return -1
#     end

#     balance = balance - amount
#     redis.call('SET', key, balance)

#     return balance
#     """

#     result = r.eval(script, 1, f"wallet:{user_id}", amount)
#    #r.eval(script, numkeys, key1, key2, ..., arg1, arg2, ...)

#     if result == -1:
#         return {
#             "status": False,
#             "message": "Insufficient balance"
#         }

#     return {
#         "status": True,
#         "remaining_balance": result
#     }