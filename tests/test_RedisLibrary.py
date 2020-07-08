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

    def test_delete_from_redis_no_key(self):
        self.redis.delete_from_redis(self.fake_redis, 'no_key')

    def test_append_to_redis(self):
        detail_address = {'city': 'Bangkok', 'country': 'Thailand'}
        self.redis.append_to_redis(self.fake_redis, 'detail_address', str(detail_address))
        data = self.redis.get_from_redis(self.fake_redis, 'detail_address').decode('UTF-8')
        self.assertDictEqual(ast.literal_eval(data), detail_address)

    def test_set_to_redis(self):
        self.redis.set_to_redis(self.fake_redis, 'home_address', '2222')
        data = self.redis.get_from_redis(self.fake_redis, 'home_address').decode('UTF-8')
        self.assertEqual(data, '2222')

    def test_get_from_redis(self):
        self.assertEqual(self.redis.get_from_redis(self.fake_redis, 'home_address'), b'1111')

    def test_get_from_redis_key_not_exists(self):
        self.assertEqual(self.redis.get_from_redis(self.fake_redis, 'key_not_exists'), None)

    def test_expire_data_from_redis(self):
        self.redis.expire_data_from_redis(self.fake_redis, 'home_address', expire_time=0)
        home_address = self.redis.get_from_redis(self.fake_redis, 'home_address')
        self.assertIsNone(home_address)

    def test_get_time_to_live_in_redis(self):
        ttl = self.redis.get_time_to_live_in_redis(self.fake_redis, 'name')
        self.assertEqual(ttl, 5)

    def test_get_time_to_live_in_redis_key_not_exists(self):
        self.assertEqual(self.redis.get_time_to_live_in_redis(self.fake_redis, 'no_key'), -2)

    def test_get_time_to_live_in_redis_second(self):
        self.fake_redis.set('year', '2020', 3600)
        ttl = self.redis.get_time_to_live_in_redis_second(self.fake_redis, 'name')
        self.assertEqual(ttl, 300)

    def test_get_time_to_live_in_redis_second_key_not_exists(self):
        self.assertEqual(self.redis.get_time_to_live_in_redis_second(self.fake_redis, 'no_key'), -2)

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

    def test_get_dict_from_redis_hash_key_not_exists(self):
        self.assertEqual(self.redis.get_dict_from_redis_hash(self.fake_redis, '7498d0b2'), {})

    def test_get_from_redis_hash(self):
        self.redis.add_hash_map_to_redis(self.fake_redis, '7498d0b2', {'star_01':'Pluto', 'star_02':'Mars'})
        self.assertEqual(self.redis.get_from_redis_hash(self.fake_redis, '7498d0b2', 'star_01'), b'Pluto')
        self.assertEqual(self.redis.get_from_redis_hash(self.fake_redis, '7498d0b2', 'star_02'), b'Mars')

    def test_get_from_redis_hash_no_key(self):
        self.redis.add_hash_map_to_redis(self.fake_redis, '7498d0b2', {'star_01':'Pluto', 'star_02':'Mars'})
        self.assertEqual(self.redis.get_from_redis_hash(self.fake_redis, '7498d0b2', 'star_03'), None)

    def test_get_from_redis_hash_no_hash(self):
        self.assertEqual(self.redis.get_from_redis_hash(self.fake_redis, '7498d0b2', 'star_03'), None)

    def test_set_to_redis_hash(self):
        self.redis.set_to_redis_hash(self.fake_redis, '7498d0b2', 'star_01', 'Pluto')
        self.assertEqual(self.redis.get_from_redis_hash(self.fake_redis, '7498d0b2', 'star_01'), b'Pluto')

    def test_add_hash_map_to_redis(self):
        self.redis.add_hash_map_to_redis(self.fake_redis, '7498d0b2', {'star_01':'Saturn','star_02':'Jupiter'})
        self.assertEqual(self.redis.get_dict_from_redis_hash(self.fake_redis, '7498d0b2'), {b'star_01': b'Saturn', b'star_02': b'Jupiter'})

    def test_delete_from_redis_hash(self):
        self.redis.add_hash_map_to_redis(self.fake_redis, '7498d0b2', {'star_01':'Saturn','star_02':'Jupiter'})
        self.redis.delete_from_redis_hash(self.fake_redis, '7498d0b2', 'star_01')
        self.assertEqual(self.redis.get_dict_from_redis_hash(self.fake_redis, '7498d0b2'), {b'star_02': b'Jupiter'})

    def test_delete_from_redis_hash_no_key(self):
        self.redis.add_hash_map_to_redis(self.fake_redis, '7498d0b2', {'star_01':'Saturn','star_02':'Jupiter'})
        self.redis.delete_from_redis_hash(self.fake_redis, '7498d0b2', 'star_03')
        self.assertEqual(self.redis.get_dict_from_redis_hash(self.fake_redis, '7498d0b2'), {b'star_01': b'Saturn', b'star_02': b'Jupiter'})

    def test_delete_from_redis_hash_no_hash(self):
        self.redis.delete_from_redis_hash(self.fake_redis, 'no_hash', 'star_01')

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

    def test_get_set_from_redis_set_key_not_exists(self):
        self.assertEqual(self.redis.get_set_from_redis_set(self.fake_redis, 'fruit'), set())

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

    def test_get_length_of_redis_set_key_not_exists(self):
        self.assertEqual(self.redis.get_length_of_redis_set(self.fake_redis, 'fruit'), 0)

    def test_delete_set_data_in_redis_set(self):
        self.redis.add_set_data_to_redis_set(self.fake_redis, "fruit", "banana", "apple", "orage", "mongo")
        self.redis.delete_set_data_in_redis_set(self.fake_redis, "fruit", "banana", "orage")
        self.assertEqual(self.redis.get_set_from_redis_set(self.fake_redis, 'fruit'), {b'apple', b'mongo'})

    def test_delete_set_data_in_redis_set_key_not_exists(self):
        self.redis.delete_set_data_in_redis_set(self.fake_redis, "fruit", "banana", "orage")

    def test_push_item_to_first_index_in_list_redis(self):
        self.redis.push_item_to_first_index_in_list_redis(self.fake_redis, 'Country', 'Germany')
        self.redis.push_item_to_first_index_in_list_redis(self.fake_redis, 'Country', 'Italy', 'France', 'Spain')
        self.assertEqual(self.redis.get_all_item_from_list_redis(self.fake_redis, 'Country'),
            [b'Spain', b'France', b'Italy', b'Germany'])

    def test_push_item_to_last_index_in_list_redis(self):
        self.redis.push_item_to_last_index_in_list_redis(self.fake_redis, 'Country', 'Germany')
        self.redis.push_item_to_last_index_in_list_redis(self.fake_redis, 'Country', 'Italy', 'France', 'Spain')
        self.assertEqual(self.redis.get_all_item_from_list_redis(self.fake_redis, 'Country'),
            [b'Germany', b'Italy', b'France', b'Spain'])

    def test_update_item_in_list_redis(self):
        self.redis.push_item_to_first_index_in_list_redis(self.fake_redis, 'Country', 'Germany', 'Italy', 'France', 'Spain')
        self.redis.update_item_in_list_redis(self.fake_redis, 'Country', 0, 'France')
        self.redis.update_item_in_list_redis(self.fake_redis, 'Country', 2, 'France')
        self.assertEqual(self.redis.get_all_item_from_list_redis(self.fake_redis, 'Country'),
            [b'France', b'France', b'France', b'Germany'])

    def test_get_item_from_list_redis(self):
        self.redis.push_item_to_first_index_in_list_redis(self.fake_redis, 'Country', 'Germany', 'Italy', 'France', 'Spain')
        self.assertEqual(self.redis.get_item_from_list_redis(self.fake_redis, 'Country', 0),
            b'Spain')
        self.assertEqual(self.redis.get_item_from_list_redis(self.fake_redis, 'Country', 2),
            b'Italy')

    def test_get_item_from_list_redis_no_index(self):
        self.redis.push_item_to_first_index_in_list_redis(self.fake_redis, 'Country', 'Germany', 'Italy', 'France', 'Spain')
        self.assertEqual(self.redis.get_item_from_list_redis(self.fake_redis, 'Country', 5), None)

    def test_get_item_from_list_redis_no_list(self):
        self.assertEqual(self.redis.get_item_from_list_redis(self.fake_redis, 'Country', 5), None)

    def test_get_all_item_from_list_redis(self):
        self.redis.push_item_to_first_index_in_list_redis(self.fake_redis, 'Country', 'Germany', 'Italy', 'France', 'Spain')
        self.assertEqual(self.redis.get_all_item_from_list_redis(self.fake_redis, 'Country'),
            [b'Spain', b'France', b'Italy', b'Germany'])

    def test_get_all_item_from_list_redis_empty_list(self):
        self.redis.push_item_to_last_index_in_list_redis(self.fake_redis, 'Country', 'Germany')
        self.fake_redis.lrem('Country', 1, 'Germany')
        self.assertEqual(self.redis.get_all_item_from_list_redis(self.fake_redis, 'Country'), [])

    def test_get_all_item_from_list_redis_no_list(self):
        self.assertEqual(self.redis.get_all_item_from_list_redis(self.fake_redis, 'Country'), [])

    def test_get_length_from_list_redis(self):
        self.redis.push_item_to_first_index_in_list_redis(self.fake_redis, 'Country', 'Germany', 'Italy', 'France', 'Spain')
        self.assertEqual(self.redis.get_length_from_list_redis(self.fake_redis, 'Country'), 4)

    def test_get_length_from_list_redis_empty_list(self):
        self.redis.push_item_to_last_index_in_list_redis(self.fake_redis, 'Country', 'Germany')
        self.fake_redis.lrem('Country', 1, 'Germany')
        self.assertEqual(self.redis.get_length_from_list_redis(self.fake_redis, 'Country'), 0)

    def test_get_length_from_list_redis_no_list(self):
        self.assertEqual(self.redis.get_length_from_list_redis(self.fake_redis, 'Country'), 0)

    def test_get_index_of_item_from_list_redis(self):
        self.redis.push_item_to_first_index_in_list_redis(self.fake_redis, 'Country',
            'Germany', 'Italy', 'France', 'Spain', 'Germany', 'Germany')
        self.assertEqual(self.redis.get_index_of_item_from_list_redis(self.fake_redis, 'Country', 'Germany'),
            [0, 1, 5])

    def test_get_index_of_item_from_list_redis_no_item(self):
        self.redis.push_item_to_first_index_in_list_redis(self.fake_redis, 'Country',
            'Germany', 'Italy', 'France', 'Spain', 'Germany', 'Germany')
        self.assertEqual(self.redis.get_index_of_item_from_list_redis(self.fake_redis, 'Country', 'England'), [])

    def test_get_index_of_item_from_list_redis_empty_list(self):
        self.redis.push_item_to_last_index_in_list_redis(self.fake_redis, 'Country', 'Germany')
        self.fake_redis.lrem('Country', 1, 'Germany')
        self.assertEqual(self.redis.get_index_of_item_from_list_redis(self.fake_redis, 'Country', 'Germany'), [])

    def test_get_index_of_item_from_list_redis_no_list(self):
        self.assertEqual(self.redis.get_index_of_item_from_list_redis(self.fake_redis, 'Country', 'Germany'), [])

    def test_get_all_match_keys(self):
        self.fake_redis.set('CountryAsia', 'Thailand', px=300000)
        self.fake_redis.set('CountryEurope', 'Germany', px=300000)
        self.assertEqual(self.redis.get_all_match_keys(self.fake_redis, '*'), [b'name', b'home_address', b'CountryAsia', b'CountryEurope'])

    def test_get_all_match_keys_with_empty_key(self):
        self.fake_redis.set('CountryAsia', 'Thailand', px=300000)
        self.fake_redis.set('CountryEurope', 'Germany', px=300000)
        self.assertEqual(self.redis.get_all_match_keys(self.fake_redis, ''), [b'name', b'home_address', b'CountryAsia', b'CountryEurope'])

    def test_get_all_match_keys_with_wildcard(self):
        self.fake_redis.set('CountryAsia', 'Thailand', px=300000)
        self.fake_redis.set('CountryEurope', 'Germany', px=300000)
        self.assertEqual(self.redis.get_all_match_keys(self.fake_redis, 'Country*'), [b'CountryAsia', b'CountryEurope'])

    def test_get_all_match_keys_without_wildcard(self):
        self.fake_redis.set('CountryAsia', 'Thailand', px=300000)
        self.fake_redis.set('CountryEurope', 'Germany', px=300000)
        self.fake_redis.set('CountryAsiaAndEurope', 'Germany', px=300000)
        self.assertEqual(self.redis.get_all_match_keys(self.fake_redis, 'CountryAsia'), [b'CountryAsia'])

    def test_get_all_match_keys_empty_list(self):
        self.assertEqual(self.redis.get_all_match_keys(self.fake_redis, 'Country*'), [])

    def test_delete_item_from_list_redis(self):
        self.redis.push_item_to_first_index_in_list_redis(self.fake_redis, 'Country', 'Germany', 'Italy', 'France', 'Spain')
        self.redis.delete_item_from_list_redis(self.fake_redis, 'Country', 2, 'Italy')
        self.assertEqual(self.redis.get_all_item_from_list_redis(self.fake_redis, 'Country'),
            [b'Spain', b'France', b'Germany'])

    def test_delete_item_from_list_redis_item_is_null(self):
        self.redis.push_item_to_first_index_in_list_redis(self.fake_redis, 'Country', 'Germany', 'Italy', 'France', 'Spain')
        self.redis.delete_item_from_list_redis(self.fake_redis, 'Country', 2)
        self.assertEqual(self.redis.get_all_item_from_list_redis(self.fake_redis, 'Country'),
            [b'Spain', b'France', b'Germany'])

    def test_delete_item_from_list_redis_item_not_matched(self):
        self.redis.push_item_to_first_index_in_list_redis(self.fake_redis, 'Country', 'Germany', 'Italy', 'France', 'Spain')
        with self.assertRaises(AssertionError):
            self.redis.delete_item_from_list_redis(self.fake_redis, 'Country', 2, 'Spain')

    def tearDown(self):
        self.fake_redis.flushall()
