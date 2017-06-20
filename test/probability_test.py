import pandas as pd
import unittest

from probability.probability_distribution import ProbabilityDistribution
from probability.random_variable import RandomVariable


class ProbabilityDistributionTestCase(unittest.TestCase):

    @property
    def P(self):
        distribution = [
            ['low',  'A', 0.07],
            ['low',  'B', 0.28],
            ['low',  'C', 0.35],
            ['high', 'A', 0.18],
            ['high', 'B', 0.09],
            ['high', 'C', 0.03],
        ]

        variables = ['Intelligence', 'Grade', 'probability']
        return ProbabilityDistribution.from_joint_distribution(pd.DataFrame(distribution, columns=variables))

    def test_empty(self):
        P = self.P

        self.assertEqual(0, P())

    def test_variables(self):
        P = self.P
        expected = [RandomVariable('Intelligence'), RandomVariable('Grade')]

        self.assertListEqual(expected, P.variables)

    def test_marginal(self):
        expected_intelligence = pd.DataFrame([
            ['low', 0.7],
            ['high', 0.3],
        ], columns=['Intelligence', 'probability'])

        expected_grade = pd.DataFrame([
            ['A', 0.25],
            ['B', 0.37],
            ['C', 0.38],
        ], columns=['Grade', 'probability'])

        P = self.P
        Intelligence, Grade = P.variables

        self.assertEqual(ProbabilityDistribution(expected_intelligence), P(Intelligence))
        self.assertEqual(ProbabilityDistribution(expected_grade), P(Grade))

        self.assertEqual(ProbabilityDistribution(expected_intelligence), P.marginal(Intelligence))
        self.assertEqual(ProbabilityDistribution(expected_grade), P.marginal(Grade))

    def test_P_at_X_equals(self):
        expected = pd.DataFrame([
            ['a1', 'b1', 'c1', 1/8],
            ['a1', 'b1', 'c2', 1/8],
            ['a1', 'b2', 'c1', 1/8],
            ['a1', 'b2', 'c2', 1/8],
        ], columns=['A', 'B', 'C', 'event'])

        P = self.P
        A = RandomVariable('A')

        self.assertEqual(ProbabilityDistribution(expected), P(A == 'a1'))

    def test_joint_distribution(self):
        expected = pd.DataFrame([
            ['low', 'A', 0.07],
            ['low', 'B', 0.28],
            ['low', 'C', 0.35],
            ['high', 'A', 0.18],
            ['high', 'B', 0.09],
            ['high', 'C', 0.03],
        ], columns=['Intelligence', 'Grade', 'probability'])

        P = self.P
        Intelligence, Grade = P.variables

        self.assertEqual(ProbabilityDistribution(expected), P(Intelligence, Grade))

    def test_P_at_X_and_Y_equal(self):
        expected = pd.DataFrame([
            ['a1', 'b2', 'c1', 1/8],
            ['a1', 'b2', 'c2', 1/8],
        ], columns=['A', 'B', 'C', 'event'])

        P = self.P
        A = RandomVariable('A')
        B = RandomVariable('B')

        self.assertEqual(ProbabilityDistribution(expected), P(A == 'a1', B == 'b2'))

    def test_normalize(self):
        expected = pd.DataFrame([
            ['a1', 'b2', 'c1', 1/2],
            ['a1', 'b2', 'c2', 1/2],
        ], columns=['A', 'B', 'C', 'event'])

        P = self.P
        A = RandomVariable('A')
        B = RandomVariable('B')

        self.assertEqual(ProbabilityDistribution(expected), P(A == 'a1', B == 'b2').normalize())

    def test_calcule_union(self):
        expected = pd.DataFrame([
            ['a1', 'b2', 'c1', 1/2],
            ['a1', 'b2', 'c2', 1/2],
        ], columns=['A', 'B', 'C', 'event'])

        P = self.P
        A = RandomVariable('A')
        B = RandomVariable('B')

        self.assertEqual(ProbabilityDistribution(expected), P(B.union(A)))

    def test_conditional_simple(self):
        P = self.P
        Intelligence, Grade = P.variables

        print(P(Intelligence | Grade))
