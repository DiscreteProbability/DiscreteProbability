import unittest
import pandas as pd

from probability.sample_space import SampleSpace
from probability.random_variable import RandomVariable


class SampleSpaceTestCase(unittest.TestCase):

    @property
    def data(self):
        data = [
            ['a1', 'b1', 'c1', 1/6],
            ['a1', 'b1', 'c2', 1/6],
            ['a1', 'b2', 'c1', 1/6],
            ['a1', 'b2', 'c2', 1/6],
            ['a2', 'b1', 'c1', 1/6],
            ['a2', 'b1', 'c2', 1/6],
            ['a2', 'b2', 'c1', 1/6],
            ['a2', 'b2', 'c2', 1/6],
        ]

        return pd.DataFrame(data, columns=['A', 'B', 'C', 'value'])

    def test_variables(self):
        space = SampleSpace(self.data)
        expected = [RandomVariable('A'), RandomVariable('B'), RandomVariable('C')]

        self.assertListEqual(expected, space.variables)
