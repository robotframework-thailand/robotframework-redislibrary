# -*- coding: utf-8 -*-
from robot.api import logger
from robot.api.deco import keyword
import redis
from redis.sentinel import Sentinel
from redis.cluster import RedisCluster as RedisCluster
from redis.cluster import ClusterNode
__author__ = 'Traitanit Huangsri'
__email__ = 'traitanit.hua@gmail.com'


class RedisLibraryKeywords(object):

    @keyword('Get Redis Cluster')
    def get_redis_cluster(self, redis_host, redis_port=6379):
        """Get from the Redis master's address corresponding.

                Arguments:
                    - redis_host: hostname or IP address of the Redis server.
                    - redis_port: Redis port number (default=6379)

                Return cluster detail

                Examples:
                | @{cluster_detail}=   | Get Redis Cluster |  'redis-dev.com' | 6379 |
                """
        try:

            nodes = [ClusterNode(redis_host, redis_port)]
            redis_cluster = RedisCluster(startup_nodes=nodes)

        except Exception as ex:
            logger.error(str(ex))
            raise Exception(str(ex))
        return redis_cluster

    @keyword('Get Redis Master')
    def get_redis_master(self, redis_host, redis_port=26379, service_name=None):
        """Get from the Redis master's address corresponding.

                Arguments:
                    - redis_host: hostname or IP address of the Redis server.
                    - redis_port: Redis port number (default=6379)
                    - service_name: Redis master's address corresponding

                Return sentinel detail lists

                Examples:
                | @{sentinel_detail}=   | Get Redis Master |  'redis-dev.com' | 6379 | 'service-name' |
                """
        try:
            sentinel = Sentinel([(redis_host, redis_port)], socket_timeout=0.1)
            sentinel_detail = sentinel.discover_master(service_name)

        except Exception as ex:
            logger.error(str(ex))
            raise Exception(str(ex))
        return sentinel_detail

    @keyword('Connect To Redis')
    def connect_to_redis(self, redis_host, redis_port=6379, db=0, redis_password=None, ssl=False, ssl_ca_certs=None):
        """Connect to the Redis server.

        Arguments:
            - redis_host: hostname or IP address of the Redis server.
            - redis_port: Redis port number (default=6379)
            - db: Redis keyspace number (default=0)
            - redis_password: password for Redis authentication
            - ssl: Connect Redis with SSL or not (default is False)
            - ssl_ca_certs: CA Certification when connect Redis with SSL

        Return redis connection object

        Examples:
        | ${redis_conn}=   | Connect To Redis |  redis-dev.com | 6379 | redis_password=password |
        """
        try:
            redis_conn = redis.StrictRedis(host=redis_host, port=redis_port, db=db,
                                           password=redis_password, ssl=ssl, ssl_ca_certs=ssl_ca_certs)
        except Exception as ex:
            logger.error(str(ex))
            raise Exception(str(ex))
        return redis_conn

    @keyword('Connect To Redis From URL')
    def connect_to_redis_from_url(self, redis_url, db=0):
        """Connect to the Redis server.

        Arguments:
            - redis_url: URL for connect to Redis. (redis://<username>:<password>@<host>:<port>)
            - db: Redis keyspace number (default=0)

        Return redis connection object

        Examples:
        | ${redis_conn}=   | Connect To Redis From URL | redis://admin:adminpassword@redis-dev.com:6379 |
        """
        try:
            logger.info("Creating Redis Connection using : url=%s " % redis_url)
            redis_conn = redis.from_url(redis_url, db)
        except Exception as ex:
            logger.error(str(ex))
            raise Exception(str(ex))
        return redis_conn

    @keyword('Flush All')
    def flush_all(self, redis_conn):
        """ Delete all keys from Redis

        Arguments:
            - redis_conn: Redis connection object

        Examples:
        | Flush All |  ${redis_conn} |
        """
        return redis_conn.flushall()

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

    @keyword('Append To Redis')
    def append_to_redis(self, redis_conn, key, value):
        """ Append data to Redis. If key doesn't exist, create it with value.
            Return the new length of the value at key.

        Arguments:
            - redis_conn: Redis connection object.
            - key: String key.
            - value: String value.

        Examples:
        | Append To Redis |  ${redis_conn} | BARCODE|1234567890 | ${data} |

        """
        return redis_conn.append(key, value)

    @keyword('Set To Redis')
    def set_to_redis(self, redis_conn, key, data, expire_time=3600):
        """ Set data to Redis

        Arguments:
            - redis_conn: Redis connection object
            - key: String keyword to find.
            - data: String data
            - expire_time: TTL default value is 3600s

        Examples:
        | Set To Redis |  ${redis_conn} | BARCODE|0000000011 | ${data}  |
        | Set To Redis |  ${redis_conn} | BARCODE|1234567890 | ${data}  | expire_time=600 |
        """
        return redis_conn.set(key, data, expire_time)

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
        | Get Time To Live In Redis |  ${redis_conn} | BARCODE|1234567890 |
        """
        ttl = redis_conn.ttl(key)
        if ttl > 0:
            return redis_conn.ttl(key) / 60
        else:
            return redis_conn.ttl(key)

    @keyword('Get Time To Live In Redis Second')
    def get_time_to_live_in_redis_second(self, redis_conn, key):
        """ Return time to live in Redis (seconds)

        Arguments:
            - redis_conn: Redis connection object
            - key: String keyword to find.

        Examples:
        | Get Time To Live In Redis Second |  ${redis_conn} | BARCODE|1234567890 |
        """
        return redis_conn.ttl(key)

    @keyword('Redis Key Should Be Exist')
    def redis_key_should_be_exist(self, redis_conn, key):
        """ Keyword will fail if specify key doesn't exist in Redis

        Arguments:
            - redis_conn: Redis connection object
            - key: String keyword to find.

        Examples:
        | Redis Key Should Be Exist | ${redis_conn} | BARCODE|1234567890 |
        """
        if not redis_conn.exists(key):
            logger.error("Key: " + key + " doesn't exist in Redis.")
            raise AssertionError

    @keyword('Redis Key Should Not Be Exist')
    def redis_key_should_not_be_exist(self, redis_conn, key):
        """ Keyword will fail if specify key exist in Redis

        Arguments:
            - redis_conn: Redis connection object
            - key: String keyword to find.

        Examples:
        | Redis Key Should Not Be Exist | ${redis_conn} | BARCODE|1234567890 |
        """
        if redis_conn.exists(key):
            logger.error("Key: " + key + " exists in Redis.")
            raise AssertionError

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

    @keyword('Set To Redis Hash')
    def set_to_redis_hash(self, redis_conn, hash_name, key, data):
        """ Set data to Redis within Hash

        Arguments:
            - redis_conn: Redis connection object
            - hash_name: String hash
            - key: String keyword to find.
            - data: String data

        Examples:
        | Set To Redis Hash |  ${redis_conn} | HASHNAME | key | value |
        """
        return redis_conn.hset(hash_name, key, data)

    @keyword('Add Hash Map To Redis')
    def add_hash_map_to_redis(self, redis_conn, hash_name, dict_data):
        """ Set data to Redis within Hash

        Arguments:
            - redis_conn: Redis connection object
            - hash_name: String hash
            - dict_data: data as dict

        Examples:
        | Add Hash Map To Redis |  ${redis_conn} | HASHNAME | {"name":"Fred","age":25} |
        """
        return redis_conn.hmset(hash_name, dict_data)

    @keyword('Delete From Redis Hash')
    def delete_from_redis_hash(self, redis_conn, hash_name, key):
        """Delete ``key`` from hash ``name``

        Arguments:
            - redis_conn: Redis connection object.
            - hash_name: Hash keyword to find.
            - key: String keyword to find.

        Examples:
        | Delete From Redis Hash |  ${redis_conn} | HASHNAME |  KEY |
        """
        return redis_conn.hdel(hash_name, key)

    @keyword('Redis Hash Key Should Be Exist')
    def redis_hash_key_should_be_exist(self, redis_conn, hash_name, key):
        """ Keyword will fail if specify hash key doesn't exist in Redis

        Arguments:
            - redis_conn: Redis connection object
            - hash_name: Hash name.
            - key: String keyword to find.

        Examples:
        | Redis Hash Key Should Be Exist | ${redis_conn} | BARCODE|1234567890 |
        """
        if not redis_conn.hexists(hash_name, key):
            logger.error("Hash: " + hash_name + " and Key: " +
                         key + " doesn't exist in Redis.")
            raise AssertionError

    @keyword('Redis Hash Key Should Not Be Exist')
    def redis_hash_key_should_not_be_exist(self, redis_conn, hash_name, key):
        """ Keyword will fail if specify hash key exist in Redis

        Arguments:
            - redis_conn: Redis connection object
            - hash_name: Hash name.
            - key: String keyword to find.
        Examples:
        | Redis Hash Key Should Not Be Exist | ${redis_conn} | BARCODE|1234567890 |
        """
        if redis_conn.hexists(hash_name, key):
            logger.error("Hash: " + hash_name + " and Key: " +
                         key + " exists in Redis.")
            raise AssertionError

    @keyword('Get Set From Redis Set')
    def get_set_from_redis_set(self, redis_conn, set_name):
        """ Get cached members from Redis sets.

        Arguments:
            - redis_conn: Redis connection object
            - set_name: Set name to find.

        Examples:
        | ${data}=   | Get Set From Redis Set |  ${redis_conn} | Fruit |
        """
        return redis_conn.smembers(set_name)

    @keyword('Add Set Data To Redis Set')
    def add_set_data_to_redis_set(self, redis_conn, set_name, *args):
        """ Add set data into Redis.

        Arguments:
            - redis_conn: Redis connection object
            - set_name: Set name as key in redis
            - *args: Item that you need to put in set

        Examples:
        | Add Set Data To Redis Set |  ${redis_conn} | Fruit | Banana | Apple | Orage |
        """
        return redis_conn.sadd(set_name, *args)

    @keyword('Item Should Exist In Redis Set')
    def item_should_exist_in_redis_set(self, redis_conn, set_name, item):
        """ Check item should exist in set.

        Arguments:
            - redis_conn: Redis connection object
            - set_name: Set name as key in redis
            - Item: Item that you need check

        Examples:
        | Item Should Exist In Redis Set |  ${redis_conn} | Fruit | Apple |
        """
        if not redis_conn.sismember(set_name, item):
            logger.error("Item: " + item + " doesn't exist in Redis.")
            raise AssertionError

    @keyword('Item Should Not Exist In Redis Set')
    def item_should_not_exist_in_redis_set(self, redis_conn, set_name, item):
        """ Check item should not exist in set.

        Arguments:
            - redis_conn: Redis connection object
            - set_name: Set name as key in redis
            - Item: Item that you need check

        Examples:
        | Item Should Not Exist In Redis Set |  ${redis_conn} | Fruit | Mongo |
        """
        if redis_conn.sismember(set_name, item):
            logger.error("Item: " + item + " exists in Redis.")
            raise AssertionError

    @keyword('Get Length of Redis Set')
    def get_length_of_redis_set(self, redis_conn, set_name):
        """ Get length of set.

        Arguments:
            - redis_conn: Redis connection object
            - set_name: Set name as key in redis

        Examples:
        | ${set_length} | Get Length of Redis Set |  ${redis_conn} | Fruit |
        """
        return redis_conn.scard(set_name)

    @keyword('Delete Set Data In Redis Set')
    def delete_set_data_in_redis_set(self, redis_conn, set_name, *args):
        """ Delete set of item from set.

            If you need to delete set from redis use 'Delete From Redis' keyword.

        Arguments:
            - redis_conn: Redis connection object
            - set_name: Set name as key in redis
            - *args: Item that you need to delete from set

        Examples:
        | Delete Set Data In Redis Set |  ${redis_conn} | Fruit | Banana | Orage |
        """
        return redis_conn.srem(set_name, *args)

    @keyword('Push Item To First Index In List Redis')
    def push_item_to_first_index_in_list_redis(self, redis_conn, list_name, *args):
        """ Push item to first index in list. If you many arguments, last arguments will be the first item.

        Arguments:
            - redis_conn: Redis connection object
            - list_name: List name as key in redis
            - *args: Item that you need to put in set

        Examples:
        | Push Item To First Index In List Redis | ${redis_conn} | Country | Germany | Italy | France | Spain |
        | ${list_items} | Get All Item From List Redis | ${redis_conn} | Country |

        Result from ``Get All Item From List Redis``: [b'Spain', b'France', b'Italy', b'Germany']
        """
        return redis_conn.lpush(list_name, *args)

    @keyword('Push Item To Last Index In List Redis')
    def push_item_to_last_index_in_list_redis(self, redis_conn, list_name, *args):
        """ Push item to last index in list. If you many arguments, last arguments will be the last item.

        Arguments:
            - redis_conn: Redis connection object
            - list_name: List name as key in redis
            - *args: Item that you need to put in set

        Examples:
        | Push Item To Last Index In List Redis | ${redis_conn} | Country | Germany | Italy | France | Spain |
        | ${list_items} | Get All Item From List Redis | ${redis_conn} | Country |

        Result from ``Get All Item From List Redis``: [b'Germany', b'Italy', b'France', b'Spain']
        """
        return redis_conn.rpush(list_name, *args)

    @keyword('Update Item In List Redis')
    def update_item_in_list_redis(self, redis_conn, list_name, index, item):
        """Update item in list by specific index.

        Arguments:
            - redis_conn: Redis connection object
            - list_name: List name as key in redis
            - index: Index in list that you need to update
            - item: New item

        Examples:
        | Update Item In List Redis | ${redis_conn} | Country | 1 | England |
        """
        return redis_conn.lset(list_name, index, item)

    @keyword('Get Item From List Redis')
    def get_item_from_list_redis(self, redis_conn, list_name, index):
        """Get item in list by specific index.

        Arguments:
            - redis_conn: Redis connection object
            - list_name: List name as key in redis
            - index: Index in list that you need to update

        Examples:
        | ${item_data} | Get Item From List Redis | ${redis_conn} | Country | 1 |
        """
        return redis_conn.lindex(list_name, index)

    @keyword('Get All Item From List Redis')
    def get_all_item_from_list_redis(self, redis_conn, list_name):
        """Get all items in list.

        Arguments:
            - redis_conn: Redis connection object
            - list_name: List name as key in redis

        Examples:
        | ${list_items} | Get All Item From List Redis | ${redis_conn} | Country |
        """
        return redis_conn.lrange(list_name, 0, -1)

    @keyword('Get Length From List Redis')
    def get_length_from_list_redis(self, redis_conn, list_name):
        """Get length of list.

        Arguments:
            - redis_conn: Redis connection object
            - list_name: List name as key in redis

        Examples:
        | ${list_length} | Get Length From List Redis | ${redis_conn} | Country |
        """
        return redis_conn.llen(list_name)

    @keyword('Get Index of Item From List Redis')
    def get_index_of_item_from_list_redis(self, redis_conn, list_name, item):
        """Get indexs of item that metched in list.

        Arguments:
            - redis_conn: Redis connection object
            - list_name: List name as key in redis
            - item: Search item

        Examples:
        | ${list_index} | Get Index of Item From List Redis | ${redis_conn} | Country | Germany |

        Keyword will return result as list of index: [0, 1, 5]
        """
        return [i for i, j in enumerate(redis_conn.lrange(list_name, 0, -1)) if j == str.encode(item)]

    @keyword('Get All Match Keys')
    def get_all_match_keys(self, redis_conn, key, count=100):
        """ Get all key that matches with specific keyword

        Arguments:
            - redis_conn: Redis connection object
            - key: String keyword to find may contain wildcard.
            - count: Element number of returns

        Examples:
        | @{key_list}=   | Get All Match Keys | ${redis_conn} | BARCODE* | 1000 |
        """
        return redis_conn.scan(0, key, count)[1]

    @keyword('Delete Item From List Redis')
    def delete_item_from_list_redis(self, redis_conn, list_name, index, item=None):
        """Delete data from list by specific index.

        Arguments:
            - redis_conn: Redis connection object
            - list_name: List name as key in redis
            - index: Index in list that you need to delete
            - item: Compare item. If it is None, keyword will not compare with item in index.
                But if is not None, keyword will compare it with item in index before delete.
                If not matched keyword will failed.

        Examples 1:
        | Delete Item From List Redis | ${redis_conn} | Country | 2 |

        Examples 2: keyword will compare it with item in index before delete.
            If not matched keyword will failed
        | Delete Item From List Redis | ${redis_conn} | Country | 2 | Spain |
        """
        if item is not None:
            if not redis_conn.lindex(list_name, index) == str.encode(item):
                logger.error("Item: " + item + " not matched with index item in list.")
                raise AssertionError
        redis_conn.lset(list_name, index, 'DELETE_ITEM')
        redis_conn.lrem(list_name, 1, 'DELETE_ITEM')
