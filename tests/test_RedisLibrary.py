# -*- coding: utf-8 -*-

__author__ = 'Traitanit Huangsri'
__email__ = 'traitanit.hua@gmail.com'

from RedisLibrary import RedisLibrary
import unittest, fakeredis, ast


class RedisLibraryTest(unittest.TestCase):
    redis = None
    fake_redis = None

    def setUp(self):
        self.redis = RedisLibrary()
        self.fake_redis = fakeredis.FakeStrictRedis()
        self.fake_redis.set('name', 'nottyo', px=300000)
        self.fake_redis.set('home_address', '1111', ex=600000)

    def test_append_to_redis(self):
        detail_address = {'city': 'Bangkok', 'country': 'Thailand'}
        self.redis.append_to_redis(self.fake_redis, 'detail_address', detail_address)
        data = self.redis.get_from_redis(self.fake_redis, 'detail_address').decode('UTF-8')
        self.assertDictEqual(ast.literal_eval(data), detail_address)

    def test_set_to_redis(self):
        self.redis.set_to_redis(self.fake_redis, 'home_address', '2222')
        data = self.redis.get_from_redis(self.fake_redis, 'home_address').decode('UTF-8')
        self.assertEqual(data, '2222')

    def test_get_ttl(self):
        ttl = self.redis.get_time_to_live_in_redis(self.fake_redis, 'name')
        self.assertEqual(ttl, 5)

    def test_delete_from_redis(self):
        self.redis.delete_from_redis(self.fake_redis, 'home_address')
        home_address = self.redis.get_from_redis(self.fake_redis, 'home_address')
        self.assertIsNone(home_address)

    def test_expire_from_redis(self):
        self.redis.expire_data_from_redis(self.fake_redis, 'home_address', expire_time=0)
        home_address = self.redis.get_from_redis(self.fake_redis, 'home_address')
        self.assertIsNone(home_address)

    def test_check_if_key_not_exists(self):
        with self.assertRaises(AssertionError):
            self.redis.redis_key_should_be_exist(self.fake_redis, 'non_existing_key')

    def test_check_if_key_exists(self):
        self.redis.redis_key_should_be_exist(self.fake_redis, 'name')

    def test_flush_all(self):
        self.redis.flush_all(self.fake_redis)
        home_address = self.redis.get_from_redis(self.fake_redis, 'home_address')
        name = self.redis.get_from_redis(self.fake_redis, 'name')
        self.assertIsNone(home_address)
        self.assertIsNone(name)

    def tearDown(self):
        self.fake_redis.flushall()
