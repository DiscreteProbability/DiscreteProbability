import pandas as pd
import unittest

from probability.sample_space import SampleSpace
from probability.random_variable import RandomVariable


class ProbabilityTestCase(unittest.TestCase):

    @property
    def sample_space(self):
        data = [
            ['a1', 'b1', 'c1', 1/8],
            ['a1', 'b1', 'c2', 1/8],
            ['a1', 'b2', 'c1', 1/8],
            ['a1', 'b2', 'c2', 1/8],
            ['a2', 'b1', 'c1', 1/8],
            ['a2', 'b1', 'c2', 1/8],
            ['a2', 'b2', 'c1', 1/8],
            ['a2', 'b2', 'c2', 1/8],
        ]

        return SampleSpace(pd.DataFrame(data, columns=['A', 'B', 'C', 'value']))

    def test_P_at_X(self):
        expected = pd.DataFrame([
            ['a1', 0.5],
            ['a2', 0.5]
        ], columns=['A', 'value'])
        expected = expected.set_index('A')

        P = self.sample_space.P
        A = RandomVariable('A')

        self.assertTrue(P(A).equals(expected))

    def test_P_at_X_equals(self):
        P = self.sample_space.P
        A = RandomVariable('A')

        self.assertEqual(0.5, P(A=='a1'))

    def test_P_at_X_and_Y(self):
        expected = pd.DataFrame([
            ['a1', 'b1', 0.25],
            ['a1', 'b2', 0.25],
            ['a2', 'b1', 0.25],
            ['a2', 'b2', 0.25]
        ], columns=['A', 'B', 'value'])
        expected = expected.set_index(['A', 'B'])

        P = self.sample_space.P
        A = RandomVariable('A')
        B = RandomVariable('B')

        self.assertTrue(P(A, B).equals(expected))
