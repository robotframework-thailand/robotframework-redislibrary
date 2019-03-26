# -*- coding: utf-8 -*-
from robot.api import logger
from robot.api.deco import keyword
import redis

__author__ = 'Traitanit Huangsri'
__email__ = 'traitanit.hua@gmail.com'


class RedisLibraryKeywords(object):

    @keyword('Connect To Redis')
    def connect_to_redis(self, redis_host=None, redis_port=None, redis_db=None,redis_url=None):  # pragma: no cover
        """Connect to the Redis server.

        Arguments:
            - redis_host: hostname or IP address of the Redis server.
            - redis_port: Redis port number (default=6379)
            - db: Redis keyspace number (default=0)

        Return redis connection object

        Examples:
        | ${redis_conn}=   | Connect To Redis |  redis-dev.com | 6379 |
        """
        try:

            if not (redis_url is None):
                logger.info ("Creating Redis Connection using : url=%s " % redis_url)
                redis_conn = redis.from_url(redis_url,redis_db)
            else:
                logger.info ("Creating Redis Connection using : Host=%s Port=%s db=%s" % (redis_host,redis_port,redis_db))
                redis_conn = redis.StrictRedis(redis_host,redis_port, redis_db)
            
            
        except Exception as ex:
            logger.error(str(ex))
            raise Exception(str(ex))
        return redis_conn

    @keyword('Append To Redis')
    def append_to_redis(self, redis_conn, key, value):
        """ Append data to Redis. If key doesn't exist, create it with value.
            Return the new length of the value at key.

        Arguments:
            - redis_conn: Redis connection object.
            - key: String key.
            - value: String value.

        Examples:
        | ${data}=   | Append To Redis |  ${redis_conn} | BARCODE|1234567890 | ${data} |

        """
        return redis_conn.append(key, value)

    @keyword('Get From Redis')
    def get_from_redis(self, redis_conn, key):
        """ Get cached data from Redis

        Arguments:
            - redis_conn: Redis connection object
            - key: String keyword to find.

        Examples:
        | ${data}=   | Get From Redis |  ${redis_conn} | BARCODE|1234567890 |
        """
        return redis_conn.get(key)

    @keyword('Get Set From Redis Set')
    def get_set_from_redis_set(self, redis_conn, key):
        """ Get cached members from Redis sets

        Arguments:
            - redis_conn: Redis connection object
            - key: Set keyword to find.

        Examples:
        | ${data}=   | Get Set From Redis Set |  ${redis_conn} | BARCODE:12345:67890 |
        """
        return redis_conn.smembers(key)

    @keyword('Get Dictionary From Redis Hash')
    def get_dict_from_redis_hash(self, redis_conn, hash_name):
        """ Get cached data from Redis hashes

        Arguments:
            - redis_conn: Redis connection object
            - hash_name: Hash name.

        Examples:
        | ${data}=   | Get Dictionary From Redis Hash |  ${redis_conn} | HASHNAME |
        """
        return redis_conn.hgetall(hash_name)

    @keyword('Get From Redis Hash')
    def get_from_redis_hash(self, redis_conn, hash_name, key):
        """ Get cached data from Redis hashes by key

        Arguments:
            - redis_conn: Redis connection object
            - hash_name: Hash name.
            - key: String keyword to find.

        Examples:
        | ${data}=   | Get From Redis Hash |  ${redis_conn} | HASHNAME | BARCODE|1234567890 |
        """
        return redis_conn.hget(hash_name, key)

    @keyword('Set To Redis')
    def set_to_redis(self, redis_conn, key, data, expire_time=0):
        """ Set data to Redis

        Arguments:
            - redis_conn: Redis connection object
            - key: String keyword to find.
            - data: String data

        Examples:
        | ${data}=   | Set To Redis |  ${redis_conn} | BARCODE|1234567890 | ${data}  |
        """
        return redis_conn.set(key, data, expire_time)

    @keyword('Set To Redis Hash')
    def set_to_redis_hash(self, redis_conn, hash_name, key, data):
        """ Set data to Redis within Hash

        Arguments:
            - redis_conn: Redis connection object
            - key: String keyword to find.
            - data: String data

        Examples:
        | ${data}=   | Set To Redis Hash |  ${redis_conn} | HASHNAME | key | {"name":"Fred","age":25}
        """
        return redis_conn.hset(hash_name, key, data)

    @keyword('Flush All')
    def flush_all(self, redis_conn):
        """ Delete all keys from Redis

        Arguments:
            - redis_conn: Redis connection object

        Examples:
        | ${data}=   | Flush All |  ${redis_conn} |
        """
        return redis_conn.flushall()

    @keyword('Expire Data From Redis')
    def expire_data_from_redis(self, redis_conn, key, expire_time=0):
        """ Expire items from Redis

        Arguments:
            - redis_conn: Redis connection object
            - key: String keyword to find.
            - expire_time: waiting time to expire data (Default = expire now)

        Examples:
        | Expire Data From Redis |  ${redis_conn} | BARCODE|1234567890 |
        """
        redis_conn.expire(key, expire_time)

    @keyword('Get Time To Live In Redis')
    def get_time_to_live_in_redis(self, redis_conn, key):
        """ Return time to live in Redis (minutes)

        Arguments:
            - redis_conn: Redis connection object
            - key: String keyword to find.

        Examples:
        | Expire Data From Redis |  ${redis_conn} | BARCODE|1234567890 |
        """
        return redis_conn.ttl(key) / 60

    @keyword('Get Time To Live In Redis Second')
    def get_time_to_live_in_redis_second(self, redis_conn, key):
        """ Return time to live in Redis (seconds)

        Arguments:
            - redis_conn: Redis connection object
            - key: String keyword to find.

        Examples:
        | Expire Data From Redis |  ${redis_conn} | BARCODE|1234567890 |
        """
        return redis_conn.ttl(key)

    @keyword('Delete From Redis')
    def delete_from_redis(self, redis_conn, key):
        """ Delete data from Redis

        Arguments:
            - redis_conn: Redis connection object
            - key: String keyword to find.

        Examples:
        | Delete From Redis |  ${redis_conn} | BARCODE|1234567890 |
        """
        return redis_conn.delete(key)

    @keyword('Delete From Redis Hash')
    def delete_from_redis_hash(self,redis_conn, hash_name, key):
        """Delete ``key`` from hash ``name``

        Arguments:
            - redis_conn: Redis connection object.
            - hash_name: Hash keyword to find.
            - key: String keyword to find.

        Examples:
        | Delete From Redis Hash |  ${redis_conn} | HASHNAME |  KEY |
        """
        return redis_conn.hdel(hash_name, key)

    @keyword('Redis Key Should Be Exist')
    def redis_key_should_be_exist(self, redis_conn, key):
        """ Keyword will fail if specify key doesn't exist in Redis

        Arguments:
            - redis_conn: Redis connection object
            - key: String keyword to find.

        Examples:
        | ${is_exist}= | Redis Key Should Be Exist | ${redis_conn} | BARCODE|1234567890 |
        """
        if redis_conn.exists(key) is False:
            logger.error("Key: " + key +" doesn't exist in Redis.")
            raise AssertionError

    @keyword('Redis Key Should Not Be Exist')
    def redis_key_should_not_be_exist(self, redis_conn, key):
        """ Keyword will fail if specify key exist in Redis

        Arguments:
            - redis_conn: Redis connection object
            - key: String keyword to find.

        Examples:
        | ${is_exist}= | Redis Key Should Not Be Exist | ${redis_conn} | BARCODE|1234567890 |
        """
        if redis_conn.exists(key) is True:
            logger.error("Key: " + key +" exist in Redis.")
            raise AssertionError

    @keyword('Redis Hash Key Should Be Exist')
    def redis_hash_key_should_be_exist(self, redis_conn, hash_name, key):
        """ Keyword will fail if specify hash key doesn't exist in Redis

        Arguments:
            - redis_conn: Redis connection object
            - hash_name: Hash name.
            - key: String keyword to find.

        Examples:
        | ${is_exist}= | Redis Hash Key Should Be Exist | ${redis_conn} | BARCODE|1234567890 |
        """
        if redis_conn.hexists(hash_name, key) is False:
            logger.error("Hash: " + hash_name + " and Key: " + key +" doesn't exist in Redis.")
            raise AssertionError

    @keyword('Redis Hash Key Should Not Be Exist')
    def redis_hash_key_should_not_be_exist(self, redis_conn, hash_name, key):
        """ Keyword will fail if specify hash key exist in Redis

        Arguments:
            - redis_conn: Redis connection object
            - hash_name: Hash name.
            - key: String keyword to find.
        Examples:
        | ${is_exist}= | Redis Hash Key Should Not Be Exist | ${redis_conn} | BARCODE|1234567890 |
        """
        if redis_conn.hexists(hash_name, key) is True:
            logger.error("Hash: " + hash_name + " and Key: " + key +" exist in Redis.")
            raise AssertionError
