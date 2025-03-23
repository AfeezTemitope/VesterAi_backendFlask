import redis
from config import Config

cache = redis.Redis.from_url(Config.REDIS_URL)