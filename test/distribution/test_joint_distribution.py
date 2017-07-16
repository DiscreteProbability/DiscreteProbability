import pandas as pd
import unittest

from probability.probability_distribution import ProbabilityDistribution
from probability.concept.random_variable import RandomVariable, SetOfRandomVariable
from probability.experiment import Experiment, Occurrence
from probability.new.joint_distribution import JointDistribution

class JointDistributionTestCase(unittest.TestCase):

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

        variables = ('Intelligence', 'Grade')
        return JointDistribution.from_list(distribution, variables)

    def to_series(self, index, names, values, name=None):
        index = pd.MultiIndex.from_tuples(index, names=names)
        return pd.Series(values, index=index, name=name)

    def test_empty(self):
        P = self.P

        self.assertEqual(0, P())

    def test_variables(self):
        P = self.P
        expected = SetOfRandomVariable((RandomVariable('Intelligence'), RandomVariable('Grade')))

        self.assertEqual(expected, P.variables)

    def test_marginalize_out(self):
        distribution = [
            ['low', 0.7],
            ['high', 0.3]
        ]
        P = self.P
        Grade = P.variables.Grade

        result = JointDistribution.from_list(distribution, ('Intelligence',))
        self.assertEqual(result, P.marginalize_out(Grade))

    def test_reduction(self):
        table = (
            ('low', 'A'),
            ('low', 'B'),
            ('low', 'C'),
        )
        values = (0.07, 0.28, 0.35)
        variables = ('Intelligence', 'Grade')
        series = self.to_series(table, variables, values, name="P((Intelligence, Grade))")


        P = self.P
        Intelligence, Grade = P.variables

        print(series)
        print(P(Intelligence=='low', Grade).series)
        self.assertTrue(series.equals(P(Intelligence=='low', Grade).series))

    def test_conditional(self):
        table = (
            ('low', 'A'),
            ('low', 'B'),
            ('low', 'C'),
        )
        values = (0.07, 0.28, 0.35)
        variables = ('Intelligence', 'Grade')
        series = self.to_series(table, variables, values)

        P = self.P
        Intelligence, Grade = P.variables

        self.assertTrue(series.equals(P(Intelligence | Grade)))
        self.assertTrue(series.equals(P(Intelligence.given(Grade))))

    '''
    def test_P_at_X_equals(self):
        P = self.P
        Grade = RandomVariable('Grade')

        self.assertEqual(0.37, P(Grade=='B'))

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

        self.assertEqual(ProbabilityDistribution.from_joint_distribution(expected), P(Intelligence, Grade))

    def test_P_at_X_and_Y_equal(self):
        P = self.P
        Intelligence, Grade = P.variables

        self.assertEqual(0.18, P(Intelligence=='high', Grade=='A'))

    def test_normalize(self):
        expected = pd.DataFrame([
            ['a1', 'b2', 'c1', 1/2],
            ['a1', 'b2', 'c2', 1/2],
        ], columns=['A', 'B', 'C', 'event'])

        P = self.P
        A = RandomVariable('A')
        B = RandomVariable('B')

        self.assertEqual(ProbabilityDistribution.from_joint_distribution(expected), P(A == 'a1', B == 'b2').normalize())

    def test_calcule_union(self):
        expected = pd.DataFrame([
            ['a1', 'b2', 'c1', 1/2],
            ['a1', 'b2', 'c2', 1/2],
        ], columns=['A', 'B', 'C', 'event'])

        P = self.P
        A = RandomVariable('A')
        B = RandomVariable('B')

        self.assertEqual(ProbabilityDistribution.from_joint_distribution(expected), P(B.union(A)))

    def test_conditional_simple(self):
        P = self.P
        Intelligence, Grade = P.variables

        print(P(Intelligence | Grade))

    def test_anything(self):
        P = self.P
        Intelligence, Grade = P.variables

        P(Intelligence | (Grade == 'A'))
'''