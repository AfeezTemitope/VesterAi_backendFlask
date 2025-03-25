import redis
from config import Config

cache = redis.Redis.from_url(Config.REDIS_URL, decode_responses=True)


redis_client = redis.Redis.from_url(Config.REDIS_URL, decode_responses=True)


"""
so this should save new one to cache and always delete after 1hr also if the doc is not there it shoudl try and add it as we did it with the get fuction for playersViews
"""