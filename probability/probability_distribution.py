import operator
from functools import reduce

from probability.random_variable import RandomVariable, UnionRandomVariable, ConditionalRandomVariable, RandomVariableEvent
from probability.plot.probability_distribution_plotter import ProbabilityDistributionPlotter


class ProbabilityDistribution(object):

    @staticmethod
    def from_joint_distribution(data_frame):
        return ProbabilityDistribution(data_frame)

    @staticmethod
    def from_experiment(experiment):
        return experiment.calcule()

    def __init__(self, joint_distribution=None):
        self.series = joint_distribution

    @property
    def variables(self):
        return [RandomVariable(column) for column in self.data.columns[0:-1]]

    @property
    def values(self):
        return self.data[self.values_column]

    @property
    def values_column(self):
        return self.data.columns[-1]

    def __call__(self, *args, **kwargs):
        if len(args) == 0:
            return 0

        variable = args[0]

        if type(variable) == RandomVariable:
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
        df = self.data
        variables = reduce(operator.and_, map(lambda v: df[v.variable.name] == v.event, args))

        return ProbabilityDistribution(self.data[variables])

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

        current = self.data
        other_data = other.data

        if len(current.columns) > 1:
            columns = list(current.columns[:-1])
            current = current.sort_values(columns)
            current = current.set_index(columns)

        if len(other_data.columns) > 1:
            columns = list(other_data.columns[:-1])
            other_data = other_data.sort_values(columns)
            other_data = other_data.set_index(columns)

        return current.equals(other_data)

    def normalize(self):
        normalized = self.series / self.series.sum()
        return ProbabilityDistribution.from_joint_distribution(normalized)

    def __repr__(self):
        return self.series.__repr__()

    def __add__(self, other):
        return ProbabilityDistribution(self.data + other.data)

    def __sub__(self, other):
        # ProbabilityDistribution(self.data - other.data)
        return self.values - other.values

    def __truediv__(self, other):
        df = self.data / other.data
        return ProbabilityDistribution.from_joint_distribution(df)

    def plot(self):
        return ProbabilityDistributionPlotter(self).plot()

    def marginal(self, X):
        P = self
        return P(X)

    def joint_distribution(self, *variables):
        variables = [variable.name for variable in variables]
        df = self.data

        return ProbabilityDistribution(df.groupby(variables).sum())

    def exists_independence(self, X, Y):
        self = P
        return P((Intelligence == 'high') | (Grade == 'A')) == P(Intelligence == 'high') or P(Grade == 'A') == 0
