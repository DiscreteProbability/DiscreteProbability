import unittest
import pandas as pd
from collections import Counter

from probability.probability_distribution import ProbabilityDistribution
from probability.experiment import Experiment, Ocurrence


class ExperimentTestCase(unittest.TestCase):

    def test_from_counter(self):
        expected = pd.DataFrame([
            ['dog', 3/8],
            ['cat', 5/8]
        ], columns=['animal', 'probability'])

        counter = Counter(dog=3, cat=5)
        experiment = Experiment.from_counter(counter, column='animal')

        self.assertEqual(ProbabilityDistribution(expected), experiment.calcule())

    def test_register(self):
        expected = [
            ['a1', 'b1', 'c1', 1],
            ['a1', 'b1', 'c2', 3],
            ['a1', 'b2', 'c1', 1],
        ]

        experiment = Experiment('A', 'B', 'C')
        experiment.register(Ocurrence(['a1', 'b1', 'c1']))
        experiment.register(Ocurrence(['a1', 'b1', 'c2'], 3))
        experiment.register(Ocurrence(['a1', 'b2', 'c1']))

        self.assertEqual(expected, experiment.data)

    def test_calcule(self):
        expected = pd.DataFrame([
            ['a1', 'b1', 'c1', 1/5],
            ['a1', 'b1', 'c2', 3/5],
            ['a1', 'b2', 'c1', 1/5],
        ], columns=['A', 'B', 'C', 'probability'])

        experiment = Experiment('A', 'B', 'C')
        experiment.register(Ocurrence(['a1', 'b1', 'c1']))
        experiment.register(Ocurrence(['a1', 'b1', 'c2'], 3))
        experiment.register(Ocurrence(['a1', 'b2', 'c1']))

        self.assertEqual(ProbabilityDistribution(expected), experiment.calcule())
