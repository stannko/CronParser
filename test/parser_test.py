import unittest
from parameterized import parameterized

from utils.parser import explain, malformed_message, labels


class TestExpressionParser(unittest.TestCase):

    @parameterized.expand([
        ('*/15 0 1,15 * 1-5 /usr/bin/find',
         ['0 15 30 45', '0', '1 15', '1 2 3 4 5 6 7 8 9 10 11 12', '1 2 3 4 5', '/usr/bin/find']
         ),
    ])
    def test_correct_data(self, expression: str, expected: list):
        expected = [label + line for label, line in zip(labels, expected)]
        expected = "\n".join(expected)
        result = explain(expression)
        self.assertEqual(expected, result)

    def test_asterisk(self):
        expression = "* * * * * /usr/bin/find"

        # Build ranges of int.
        expected = [
            list(range(60)),
            list(range(24)),
            list(range(1, 31 + 1)),
            list(range(1, 12 + 1)),
            list(range(0, 7)),
        ]

        # change type to string.
        expected = [list(map(str, lst)) for lst in expected]
        # join strings
        expected = [" ".join(lst) for lst in expected]
        # append command
        expected.append('/usr/bin/find')
        # zip with labels.
        expected = [label + line for label, line in zip(labels, expected)]
        # join to single multiline string.
        expected = "\n".join(expected)

        result = explain(expression)
        self.assertEqual(expected, result)

    @parameterized.expand([
        ('*/15 -1 1,15 * 1-5 /usr/bin/find', malformed_message),
        ('*/15 1,15 * 1-5 /usr/bin/find', malformed_message),
    ])
    def test_incorrect_data(self, expression: str, expected: str):
        result = explain(expression)
        self.assertEqual(expected, result)
