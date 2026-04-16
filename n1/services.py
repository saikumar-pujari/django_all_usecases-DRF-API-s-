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