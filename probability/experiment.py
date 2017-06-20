import pandas as pd

from probability.probability_distribution import ProbabilityDistribution


class Ocurrence(object):
    def __init__(self, keys, total=1):
        self.keys = [keys] if type(keys) != list else keys

        self.total = total


class Experiment(object):

    @staticmethod
    def from_counter(counter, column):
        experiment = Experiment(column)
        experiment.data = [[key, counter[key]] for key in counter]

        return experiment

    def __init__(self, *columns):
        self.columns = columns
        self.data = []

    def register(self, occurrence):
        self.data.append(occurrence.keys + [occurrence.total])

    def calcule(self):
        df = pd.DataFrame(self.data, columns=list(self.columns) + ['probability'])

        return ProbabilityDistribution(df).normalize()
