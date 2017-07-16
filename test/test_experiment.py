import unittest
import pandas as pd
from collections import Counter

from probability.probability_distribution import ProbabilityDistribution
from probability.experiment import Experiment, Occurrence


class ExperimentTestCase(unittest.TestCase):

    def test_from_counter(self):
        # Expected
        expected = Experiment('Coin')

        expected.register(Occurrence('head', 3))
        expected.register(Occurrence('tail', 5))

        # Test
        counter = Counter(head=3, tail=5)
        experiment = Experiment.from_counter(counter, column='Coin')

        self.assertEqual(expected, experiment)

    def test_to_series(self):
        column = 'Coin'
        expected = Occurrence('head', 3).to_series(column)
        expected = expected.append(Occurrence('tail', 5).to_series(column))

        counter = Counter(head=3, tail=5)
        experiment = Experiment.from_counter(counter, column=column)

        self.assertTrue(expected.equals(experiment.to_series()))

    def test_to_series_multiindex(self):
        experiment = Experiment('Coin', 'Die')
        experiment.register(Occurrence(['head', 'four'], 3))
        experiment.register(Occurrence(['tail', 'two'], 5))
        experiment.register(Occurrence(['tail', 'three'], 8))

        self.assertTrue(False)

    def test_register(self):
        expected = [
            Occurrence(['Carlos', 'yellow', 'computer']),
            Occurrence(['Carlos', 'yellow', 'smartphone'], 3),
            Occurrence(['Paulo', 'blue', 'computer']),
        ]

        experiment = Experiment('People', 'House', 'Computer')

        for occurrence in expected:
            experiment.register(occurrence)

        self.assertEqual(expected, experiment.occurrences)

    def test_calcule(self):
        expected = pd.DataFrame([
            ['a1', 'b1', 'c1', 1/5],
            ['a1', 'b1', 'c2', 3/5],
            ['a1', 'b2', 'c1', 1/5],
        ], columns=['A', 'B', 'C', 'probability'])

        experiment = Experiment('A', 'B', 'C')

        experiment.register(Occurrence(['a1', 'b1', 'c1']))
        experiment.register(Occurrence(['a1', 'b1', 'c2'], 3))
        experiment.register(Occurrence(['a1', 'b2', 'c1']))

        self.assertEqual(ProbabilityDistribution.from_joint_distribution(expected), experiment.calcule())
