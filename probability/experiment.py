import pandas as pd
from functools import reduce

from probability.probability_distribution import ProbabilityDistribution


class Occurrence(object):
    def __init__(self, keys, total=1):
        self.keys = keys
        self.total = total

    def to_series(self, *columns):
        if len(columns) == 1:
            index = pd.Index([self.keys], name=columns[0])
        else:
            index = pd.MultiIndex.from_arrays(self.keys, names=columns)

        return pd.Series(self.total, index=index)

    def __eq__(self, other):
        return self.keys == other.keys \
           and self.total == other.total

    def __repr__(self):
        return '<Occurrence {} at {} time(s):'.format(self.keys, self.total)


class Experiment(object):

    @staticmethod
    def from_counter(counter, column):
        experiment = Experiment(column)
        for key in sorted(counter):
            experiment.register(Occurrence(key, counter[key]))

        return experiment

    def __init__(self, *columns):
        self.columns = columns
        self.occurrences = []

    def register(self, occurrence):
        self.occurrences.append(occurrence)

    def calcule(self):
        series = self.to_series()
        level = series.index.names if len(series.index.names) > 1 else series.index.name
        series = series.groupby(level=level).sum()

        return ProbabilityDistribution.from_joint_distribution(series).normalize()

    def to_series(self):
        if not self.occurrences:
            return pd.Series()

        to_series = lambda occurrence: occurrence.to_series(*self.columns)
        first_occurrence = to_series(self.occurrences[0])

        return reduce(lambda a, b: a.append(to_series(b)), self.occurrences[1:], first_occurrence)

    def __repr__(self):
        return self.to_series().__repr__()

    def __eq__(self, other):
        return self.columns == other.columns \
           and self.occurrences == other.occurrences
