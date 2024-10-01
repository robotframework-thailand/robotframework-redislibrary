Change Log: `robotframework-redislibrary`
================================

## Version 1.2.6
**Date:** 01-Oct-2024
- Update connect_to_redis_from_url https://github.com/robotframework-thailand/robotframework-redislibrary/pull/38

## Version 1.2.4
**Date:** 04-Mar-2022
- add keywords Get Redis Master (Redis Cluster)

## Version 1.2.3
**Date:** 18-Aug-2021
- add keywords Get Redis Master (Redis sentinel)

## Version 1.0.0
**Date:** 27-Dec-2019
- Fixed import of redis in setup.py
- Fixed keyword 'Get Time To Live In Redis' to handle when get TTL as minus value.
- Remove keyword 'Check If Key Not Exists', please use 'Redis Key Should Not Be Exist'
- Change default expire_time of 'Set To Redis' keyword to 3600 seconds
- Keyword 'Connect To Redis' will support password and SSL
- Add keywords for operate with set in redis
- Add keywords for operate with set in redis
- Add more unit test and now it cover all keywords.
- Add keywords 'Connect To Redis From URL'

## Version 0.3

**Date:** 31-July-2018

1. Add new keyword
	- get_time_to_live_in_redis_second
	- set_to_redis_hash
	- delete_from_redis_hash
	- redis_key_should_not_be_exist
	- redis_hash_key_should_be_exist
	- redis_hash_key_should_not_be_exist
2. Change function name of 'check_if_key_exits' to 'redis_key_should_be_exist'