[![StackShare](https://img.shields.io/badge/tech-stack-0690fa.svg?style=flat)](https://stackshare.io/nottyo/robotframework-redislibrary)
[![Build Status](https://travis-ci.org/robotframework-thailand/robotframework-redislibrary.svg?branch=master)](https://travis-ci.org/robotframework-thailand/robotframework-redislibrary)
# RedisLibrary

`RedisLibrary` is a [Robot Framework](http://www.robotframework.org) test library which provides keywords for manipulating in-memory data stores in [Redis](https://redis.io/)

[Redis](https://redis.io/) is an open-source software project that implements data structure servers. It is networked, in-memory, and stores keys with optional durability.

You can add, get, update and delete your data from Redis. The keywords are implemented using [redis-py](https://github.com/andymccurdy/redis-py)

# Usage

Install `robotframework-redislibrary` via `pip` command

```bash
pip install -U robotframework-redislibrary
```

# Example Test Case
| *** Settings ***   |                     |                   |                 |                 |
| ------------------ | ------------------- | ----------------- | --------------- | --------------- |
| Library            |  RedisLibrary       |                   |                 |                 |
| *** Test Cases *** |                     |                   |                 |                 |
| TestRedisSample    |                     |                   |                 |                 |
| ${redis_conn}=     | Connect To Redis    | myredis-dev.com   | port=6379       |                 |
| ${data}=           | Get From Redis      | ${redis_conn}     | BARCODE\|1234567|                 |
| Should Be Equal As Strings | ${data}     | TestExpectedData  |                 |                 |
| ${obj_to_add}=     | Create Dictionary   | name=testFullName |                 |                 |
| Append To Redis    | ${redis_conn}       | BARCOE\|1234567   | ${object_to_add}|                 |
| @{key_list}=       | Get All Match Keys  | ${redis_conn}     | BARCODE*        | 1000            |

# Documentation
For the detail keyword documentation. Go to this following link:

https://robotframework-thailand.github.io/robotframework-redislibrary/RedisLibrary.html

# Help & Issues
Mention me on Twitter [@nottyo](https://twitter.com/nottyo)
