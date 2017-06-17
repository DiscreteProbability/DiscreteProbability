import unittest

from probability.random_variable import RandomVariable


class RandomVariableTestCase(unittest.TestCase):

    def test___eq__(self):
        self.assertEqual(RandomVariable('A'), RandomVariable('A'))
        self.assertNotEqual(RandomVariable('A'), RandomVariable('B'))
