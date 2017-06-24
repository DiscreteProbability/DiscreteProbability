import numpy as np
import pandas as pd
from fractions import Fraction

from probability.plot.probability_distribution_plotter import ProbabilityDistributionPlotter
from probability.random_variable import RandomVariable, UnionRandomVariable, ConditionalRandomVariable, RandomVariableEvent
from probability.expectation import Expectation


class ProbabilityDistribution(object):

    @staticmethod
    def from_joint_distribution(distribution):
        if type(distribution) == pd.Series:
            return ProbabilityDistribution(distribution)
        elif type(distribution) == pd.DataFrame:
            columns = list(distribution.columns)
            series_columns = columns[:-1]
            series_value = columns[-1]
            series = distribution.groupby(series_columns).sum()[series_value]

            return ProbabilityDistribution(series)

        raise Exception('Expected pandas.Series or pandas.DataFrame')

    @staticmethod
    def from_experiment(experiment):
        return experiment.calcule()

    def __init__(self, series=None):
        self.series = series

    @property
    def variables(self):
        index = self.series.index
        names = [index.name] if type(index) == pd.Index else index.names

        return [RandomVariable(column) for column in names]

    def __call__(self, *args, **kwargs):
        if len(args) == 0:
            return 0

        variable = args[0]

        if type(variable) == set:
            return self(*[X == x for X, x in zip(self.variables, args)])

        elif type(variable) == RandomVariable:
            return self.joint_distribution(*args)
        elif type(variable) == UnionRandomVariable:
            return self._union_probability(*args)
        elif type(variable) == ConditionalRandomVariable:
            return self._conditional_probability(variable)
        elif type(variable) == RandomVariableEvent:
            return self._intersection_probability(*args)
        else:
            return self(*[X==x for X, x in zip(self.variables, args)])

    def _intersection_probability(self, *args):
        variables, events = [], []
        for arg in args:
            variables.append(arg.variable)
            events.append(arg.event if type(arg.event) != set else list(arg.event))

        P = self

        events = tuple(events)
        return P(*variables).series.loc[events].sum()

    def _union_probability(self, union_random_variable):
        X = union_random_variable.X
        Y = union_random_variable.Y
        P = self

        return P(X) + P(Y) - P(X, Y)

    def _conditional_probability(self, conditional):
        X = conditional.of
        Y = conditional.given
        P = self

        return P(X, Y) / P(Y)

    def __eq__(self, other):
        if type(other) != ProbabilityDistribution:
            return False
        return np.isclose(self.series, other.series).all()

    def normalize(self):
        normalized = self.series / self.series.sum()
        return ProbabilityDistribution.from_joint_distribution(normalized)

    def __repr__(self):
        return self.series.map(lambda x: Fraction(x).limit_denominator()).__repr__()

    def __add__(self, other):
        other = other.series if type(other) == ProbabilityDistribution else other
        return ProbabilityDistribution(self.series + other)

    def __sub__(self, other):
        # ProbabilityDistribution(self.data - other.data)
        return self.series - other.series

    def __truediv__(self, other):
        other_data = other.series if type(other) == ProbabilityDistribution else other

        series = self.series / other_data
        return ProbabilityDistribution.from_joint_distribution(series)

    @property
    def plot(self):
        return ProbabilityDistributionPlotter(self)

    def marginal(self, X):
        P = self
        return P(X)

    def joint_distribution(self, *variables):
        variables = [variable.name for variable in variables]
        series = self.series

        return ProbabilityDistribution(series.groupby(level=variables).sum())

    def exists_independence(self, X, Y):
        self = P
        return P((Intelligence == 'high') | (Grade == 'A')) == P(Intelligence == 'high') or P(Grade == 'A') == 0

    def to_dataframe(self):
        return self.series.unstack().fillna(0)

    @property
    def E(self):
        return Expectation(self)
