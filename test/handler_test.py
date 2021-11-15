import unittest
from parameterized import parameterized

from utils.parser import handle, Bounds


class TestHandlerParser(unittest.TestCase):

    @parameterized.expand([
        ('*/15', [0, 15, 30, 45], Bounds.Minute),
        ('*/60', [0], Bounds.Minute),
        ('0', [0], Bounds.Hour),
        ('23', [23], Bounds.Hour),
        ('1,15', [1, 15], Bounds.DayOfMonth),
        ('1,31', [1, 31], Bounds.DayOfMonth),
        ('*', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], Bounds.Month),
        ('1-5', [1, 2, 3, 4, 5], Bounds.DayOfWeek),
        ('0-6', [0, 1, 2, 3, 4, 5, 6], Bounds.DayOfWeek),
        ('2-6/2', [2, 4, 6], Bounds.DayOfWeek),
    ])
    def test_correct_data(self, expression: str, expected: str, corner):
        min_v, max_v = corner
        result = handle(expression, min_v, max_v)
        self.assertEqual(expected, result)

    @parameterized.expand([
        ('1*/15', [], Bounds.Minute),
        ('24', [], Bounds.Hour),
        ('1,15,32', [], Bounds.DayOfMonth),
        ('**', [], Bounds.Month),
        ('1-8', [], Bounds.DayOfWeek),
        ('boom', [], Bounds.DayOfWeek),
        ('-1', [], Bounds.DayOfWeek),
    ])
    def test_malformed_data(self, expression: str, expected: str, corner):
        min_v, max_v = corner
        result = handle(expression, min_v, max_v)
        self.assertEqual(expected, result)
