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

    def test_flush_all(self):
        self.redis.flush_all(self.fake_redis)
        home_address = self.redis.get_from_redis(self.fake_redis, 'home_address')
        name = self.redis.get_from_redis(self.fake_redis, 'name')
        self.assertIsNone(home_address)
        self.assertIsNone(name)

    def test_delete_from_redis(self):
        self.redis.delete_from_redis(self.fake_redis, 'home_address')
        home_address = self.redis.get_from_redis(self.fake_redis, 'home_address')
        self.assertIsNone(home_address)

    def test_append_to_redis(self):
        detail_address = {'city': 'Bangkok', 'country': 'Thailand'}
        self.redis.append_to_redis(self.fake_redis, 'detail_address', str(detail_address))
        data = self.redis.get_from_redis(self.fake_redis, 'detail_address').decode('UTF-8')
        self.assertDictEqual(ast.literal_eval(data), detail_address)

    def test_set_to_redis(self):
        self.redis.set_to_redis(self.fake_redis, 'home_address', '2222')
        data = self.redis.get_from_redis(self.fake_redis, 'home_address').decode('UTF-8')
        self.assertEqual(data, '2222')

    def test_expire_data_from_redis(self):
        self.redis.expire_data_from_redis(self.fake_redis, 'home_address', expire_time=0)
        home_address = self.redis.get_from_redis(self.fake_redis, 'home_address')
        self.assertIsNone(home_address)

    def test_get_time_to_live_in_redis(self):
        ttl = self.redis.get_time_to_live_in_redis(self.fake_redis, 'name')
        self.assertEqual(ttl, 5)

    def test_get_time_to_live_in_redis_second(self):
        self.fake_redis.set('year', '2020', 3600)
        ttl = self.redis.get_time_to_live_in_redis_second(self.fake_redis, 'name')
        self.assertEqual(ttl, 300)

    def test_redis_key_should_be_exist_success(self):
        self.redis.redis_key_should_be_exist(self.fake_redis, 'name')

    def test_redis_key_should_be_exist_failed(self):
        with self.assertRaises(AssertionError):
            self.redis.redis_key_should_be_exist(self.fake_redis, 'non_existing_key')

    def test_redis_key_should_not_be_exist_success(self):
        self.redis.redis_key_should_not_be_exist(self.fake_redis, 'non_existing_key')

    def test_redis_key_should_not_be_exist_failed(self):
        with self.assertRaises(AssertionError):
            self.redis.redis_key_should_not_be_exist(self.fake_redis, 'name')

    def test_get_dict_from_redis_hash(self):
        self.redis.set_to_redis_hash(self.fake_redis, '7498d0b2', 'star_01', 'Pluto')
        self.redis.set_to_redis_hash(self.fake_redis, '7498d0b2', 'star_02', 'Mars')
        self.assertEqual(self.redis.get_dict_from_redis_hash(self.fake_redis, '7498d0b2'), {b'star_01': b'Pluto', b'star_02': b'Mars'})

    def test_set_to_redis_hash(self):
        self.redis.set_to_redis_hash(self.fake_redis, '7498d0b2', 'star_01', 'Pluto')
        self.assertEqual(self.redis.get_from_redis_hash(self.fake_redis, '7498d0b2', 'star_01'), b'Pluto')

    def test_add_hash_map_to_redis(self):
        self.redis.add_hash_map_to_redis(self.fake_redis, '7498d0b1', {'star_01':'Saturn','star_02':'Jupiter'})
        self.assertEqual(self.redis.get_dict_from_redis_hash(self.fake_redis, '7498d0b1'), {b'star_01': b'Saturn', b'star_02': b'Jupiter'})

    def test_delete_from_redis_hash(self):
        self.redis.set_to_redis_hash(self.fake_redis, '7498d0b2', 'star_01', 'Pluto')
        self.redis.delete_from_redis_hash(self.fake_redis, '7498d0b2', 'star_01')
        home_address = self.redis.get_from_redis_hash(self.fake_redis, '7498d0b2', 'star_01')
        self.assertIsNone(home_address)

    def test_redis_hash_key_should_be_exist_success(self):
        self.redis.set_to_redis_hash(self.fake_redis, '7498d0b2', 'star_01', 'Pluto')
        self.redis.redis_hash_key_should_be_exist(self.fake_redis, '7498d0b2', 'star_01')

    def test_redis_hash_key_should_be_exist_failed_no_key(self):
        with self.assertRaises(AssertionError):
            self.redis.redis_hash_key_should_be_exist(self.fake_redis, '7498d0b2', 'non_existing_key')

    def test_redis_hash_key_should_be_exist_failed_no_hash(self):
        with self.assertRaises(AssertionError):
            self.redis.redis_hash_key_should_be_exist(self.fake_redis, 'non_hash', 'star_01')

    def test_redis_hash_key_should_not_be_exist_success_no_key(self):
        self.redis.redis_hash_key_should_not_be_exist(self.fake_redis, '7498d0b2', 'non_existing_key')

    def test_redis_hash_key_should_not_be_exist_success_no_hash(self):
        self.redis.redis_hash_key_should_not_be_exist(self.fake_redis, 'non_hash', 'star_01')

    def test_redis_hash_key_should_not_be_exist_failed(self):
        self.redis.set_to_redis_hash(self.fake_redis, '7498d0b2', 'star_01', 'Pluto')
        with self.assertRaises(AssertionError):
            self.redis.redis_hash_key_should_not_be_exist(self.fake_redis, '7498d0b2', 'star_01')

    def test_get_set_from_redis_set(self):
        self.redis.add_set_data_to_redis_set(self.fake_redis, "fruit", "banana", "apple", "orage")
        self.assertEqual(self.redis.get_set_from_redis_set(self.fake_redis, 'fruit'), {b'banana', b'apple', b"orage"})

    def test_item_should_exist_in_redis_set_success(self):
        self.redis.add_set_data_to_redis_set(self.fake_redis, "fruit", "banana", "apple", "orage")
        self.redis.item_should_exist_in_redis_set(self.fake_redis, "fruit", "apple")

    def test_item_should_exist_in_redis_set_failed(self):
        self.redis.add_set_data_to_redis_set(self.fake_redis, "fruit", "banana", "apple", "orage")
        with self.assertRaises(AssertionError):
            self.redis.item_should_exist_in_redis_set(self.fake_redis, "fruit", "mongo")

    def test_item_should_not_exist_in_redis_set_success(self):
        self.redis.add_set_data_to_redis_set(self.fake_redis, "fruit", "banana", "apple", "orage")
        with self.assertRaises(AssertionError):
            self.redis.item_should_not_exist_in_redis_set(self.fake_redis, "fruit", "apple")

    def test_item_should_not_exist_in_redis_set_failed(self):
        self.redis.add_set_data_to_redis_set(self.fake_redis, "fruit", "banana", "apple", "orage")
        self.redis.item_should_not_exist_in_redis_set(self.fake_redis, "fruit", "mongo")

    def test_get_length_of_redis_set(self):
        self.redis.add_set_data_to_redis_set(self.fake_redis, "fruit", "banana", "apple", "orage")
        self.assertEqual(self.redis.get_length_of_redis_set(self.fake_redis, 'fruit'), 3)

    def test_delete_set_data_in_redis_set(self):
        self.redis.add_set_data_to_redis_set(self.fake_redis, "fruit", "banana", "apple", "orage", "mongo")
        self.redis.delete_set_data_in_redis_set(self.fake_redis, "fruit", "banana", "orage")
        self.assertEqual(self.redis.get_set_from_redis_set(self.fake_redis, 'fruit'), {b'apple', b'mongo'})

    def tearDown(self):
        self.fake_redis.flushall()
