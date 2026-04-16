local hello='Hello, Lua!'
print(hello)

script = r.register_script("""
    local key = KEYS[1]
    local amount = tonumber(ARGV[1])

    local balance = tonumber(redis.call('GET', key) or "0")

    if balance < amount then
        return -1
    end

    balance = balance - amount
    redis.call('SET', key, balance)

    return balance
""")
result = script(keys=[f"wallet:{user_id}"], args=[amount])