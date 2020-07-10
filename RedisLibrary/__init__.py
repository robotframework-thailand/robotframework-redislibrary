# -*- coding: utf-8 -*-
from .RedisLibraryKeywords import RedisLibraryKeywords
from .version import VERSION

__author__ = 'Traitanit Huangsri'
__email__ = 'traitanit.hua@gmail.com'


class RedisLibrary(RedisLibraryKeywords):
    """
    `RedisLibrary` is a [http://www.robotframework.org|Robot Framework] test library which provides keywords for manipulating in-memory data stores in [https://redis.io/|Redis]

    Redis is an open-source software project that implements data structure servers. It is networked, in-memory, and stores keys with optional durability.

    You can add, get, update and delete your data from Redis. The keywords are implemented using [https://github.com/andymccurdy/redis-py|redis-py]

    *Usage*

    Install `robotframework-redislibrary` via `pip` command

    ``pip install -U robotframework-redislibrary``

    Here is a sample

        | ***** Settings ***** |
        | Library | RedisLibrary |
        | ***** Test Cases ***** |
        | Get Requests |
        | | ${redis_conn} | Connect To Redis | ${redis_host} | ${redis_port} | db=${0} |
        | | Set Test Variable | ${redis_key} | 1234567890 |
        | | Set Test Variable | ${redis_data} | {"data":{"message":"Hello Worlds!!!"}} |
        | | Append To Redis | ${redis_conn} | ${redis_key} | ${redis_data} |
        | | ${response_data} | Get From Redis | ${redis_conn} | ${redis_key} |
        | | Should Be Equal as Strings | ${response_data} | ${redis_data} |
        | | Redis Key Should Be Exist | ${redis_conn} | ${redis_key} |
        | | Delete From Redis | ${redis_conn} | ${redis_key} |
        | | Redis Key Should Not Be Exist | ${redis_conn} | ${redis_key} |
        | | @{key_list}= | Get All Match Keys | ${redis_conn} | BARCODE* | 1000 |

    References:

     + Redis-Py Documentation - https://redis-py.readthedocs.io/en/latest/
    """
    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LIBRARY_DOC_FORMAT = "ROBOT"
    ROBOT_LIBRARY_VERSION = VERSION
