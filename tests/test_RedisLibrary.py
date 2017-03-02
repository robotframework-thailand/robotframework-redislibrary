# -*- coding: utf-8 -*-

__author__ = 'Traitanit Huangsri'
__email__ = 'traitanit.hua@ascendcorp.com'

from RedisLibrary import RedisLibrary
import unittest


class RedisLibraryTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_addition(self):
        test = RedisLibrary()
        result = test.add(-10,20,30)
        self.assertEqual(result, 40)

    def test_subtraction(self):
        test = RedisLibrary()
        result = test.subtract(50, 33)
        self.assertEqual(result, 17)

    def test_mutiplication(self):
        test = RedisLibrary()
        result = test.multiply(32, 33)
        self.assertEqual(result, 1056)

    def test_division_success(self):
        test = RedisLibrary()
        result = test.divide(1000, 200)
        self.assertEqual(result, 5)

    def test_division_divisor_equal_to_zero(self):
        test = RedisLibrary()
        self.assertRaises(AssertionError, test.divide, 1000, 0)

    def test_modulo_success(self):
        test = RedisLibrary()
        result = test.mod(1000, 22)
        self.assertEqual(result, 10)

    def test_modulo_divisor_equal_to_zero(self):
        test = RedisLibrary()
        self.assertRaises(AssertionError, test.mod, 1000, 0)

    def tearDown(self):
        pass
