import tornadoredis
from config.appConfig import redisServer

cacheClient=None

if redisServer:
    cacheClient = tornadoredis.Client(host=redisServer.split(":")[-2], port=int(redisServer.split(":")[-1]))
    cacheClient.connect()
