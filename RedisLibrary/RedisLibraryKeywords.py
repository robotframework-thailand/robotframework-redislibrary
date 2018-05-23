# -*- coding: utf-8 -*-
from robot.api import logger
from robot.api.deco import keyword
from .version import VERSION
import redis

__author__ = 'Traitanit Huangsri'
__email__ = 'traitanit.hua@gmail.com'
__version__ = VERSION


class RedisLibraryKeywords(object):

    @keyword('Connect To Redis')
    def connect_to_redis(self, redis_host, redis_port=6379, db=0): # pragma: no cover
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
            redis_conn = redis.StrictRedis(host=redis_host, port=redis_port, db=db)
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

    @keyword('Get Dictionary From Redis Hash')
    def get_dict_from_redis_hash(self, redis_conn, name):
        """ Get cached data from Redis hashes

        Arguments:
            - redis_conn: Redis connection object
            - name: Hash name.

        Examples:
        | ${data}=   | Get From Redis Hash |  ${redis_conn} | HASHNAME |
        """
        return redis_conn.hgetall(name)

    @keyword('Get From Redis Hash')
    def get_from_redis_hash(self, redis_conn, name, key):
        """ Get cached data from Redis hashes by key

        Arguments:
            - redis_conn: Redis connection object
            - name: Hash name.
            - key: String keyword to find.

        Examples:
        | ${data}=   | Get From Redis Hash |  ${redis_conn} | HASHNAME | BARCODE|1234567890 |
        """
        return redis_conn.hget(name, key)

    @keyword('Set To Redis')
    def set_to_redis(self, redis_conn, key, data):
        """ Set data to Redis

        Arguments:
            - redis_conn: Redis connection object
            - key: String keyword to find.
            - data: String data

        Examples:
        | ${data}=   | Set To Redis |  ${redis_conn} | BARCODE|1234567890 | ${data}  |
        """
        return redis_conn.set(key, data)

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

    @keyword('Redis Key Should Be Exist')
    def check_if_key_exits(self, redis_conn, key):
        """ Keyword will fail if specify key doesn't exist in Redis

        Arguments:
            - redis_conn: Redis connection object
            - key: String keyword to find.

        Examples:
        | ${is_exist}= | Check If Key Exists | ${redis_conn} | BARCODE|1234567890 |
        """
        if redis_conn.exists(key) is False:
            logger.error("Key " + key +" doesn't exist in Redis.")
            raise AssertionError


