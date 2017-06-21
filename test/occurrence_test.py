import pandas as pd
import unittest

from probability.experiment import Occurrence


class OccurrenceTestCase(unittest.TestCase):

    def test_to_series_index(self):
        expected = pd.Series([3], index=pd.Index(['tail'], name='Coin'))
        current = Occurrence('tail', 3).to_series('Coin')

        self.assertTrue(expected.equals(current))

    def test_to_series_multiindex(self):
        columns = ('Coin', 'Die')
        keys = ('tail', 'three')
        occurrences = 3

        index = pd.MultiIndex.from_tuples([keys], names=columns)
        expected = pd.Series(occurrences, index=index)

        current = Occurrence(keys, occurrences).to_series(*columns)

        self.assertTrue(expected.equals(current))
