import numpy as np
import pandas as pd
from fractions import Fraction

from probability.plot.probability_distribution_plotter import ProbabilityDistributionPlotter
from probability.concept.assignment import Assignment
from probability.concept.conditional import ConditionalRandomVariable
from probability.concept.random_variable import RandomVariable, UnionRandomVariable
from probability.other.elements_list import ElementsList
from probability.expectation import Expectation
from probability.conditional_distribution import ConditionalDistribution


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

        raise Exception('Expected `pandas.Series` or `pandas.DataFrame`')

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
        return self.parse(ElementsList(*args))

    def parse(self, elements_list):
        """
        :param ElementsList elements_list:
        """
        if not elements_list:
            return 0

        if elements_list.is_conditional_random_variable():
            return ConditionalDistribution(self, elements_list[0])
        elif elements_list.contains_conditional_distribution():
            return ConditionalDistribution(self, elements_list.to_conditional_random_variable())

        if elements_list.is_only_values():
            return self.reduction(*[X == x for X, x in zip(self.variables, elements_list.elements)])

        if elements_list.contains_assignment():
            return self.reduction(*elements_list.elements)

        #elif type(variable) == UnionRandomVariable:
        #    return self._union_probability(*args)
        #raise Exception("I don't know how work with elements: {}".format(elements_list.elements))

        return self.joint_distribution(*elements_list.elements)

    def reduction(self, *args):
        P = self
        variables = [var.random_variable for var in args]

        events = []
        for element in args:
            values = P.Val(element) if type(element) != Assignment else element.event.elements
            events.append(list(values))

        events = tuple(events)
        reduction = P(*variables).series.loc[events]

        return P.from_joint_distribution(reduction)

    def joint_distribution(self, *variables):
        variables = [variable.name for variable in variables]
        series = self.series

        return ProbabilityDistribution(series.groupby(level=variables).sum())

    def marginalize_out(self, *variables):
        """
        Marginalize out the variables from this joint distribution
        :param RandomVariable variables:
        """
        P = self
        variables_new_joint_distribution = set(self.variables) - set(variables)
        return P(*variables_new_joint_distribution)

    def _union_probability(self, union_random_variable):
        X = union_random_variable.X
        Y = union_random_variable.Y
        P = self

        return P(X) + P(Y) - P(X, Y)

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
        """
        Based in: https://github.com/pandas-dev/pandas/issues/9368
        """
        X = self.series
        Y = other.series

        on = list(set(X.index.names) & set(Y.index.names))
        result = pd.merge(X.reset_index(), Y.reset_index(), on=on)

        probability_x, probability_y = result.columns[-2], result.columns[-1]
        result = result[probability_x] / result[probability_y]
        result.index = X.index

        return ProbabilityDistribution.from_joint_distribution(result)

    @property
    def plot(self):
        return ProbabilityDistributionPlotter(self)

    def exists_independence(self, X, Y):
        self = P
        return P((Intelligence == 'high') | (Grade == 'A')) == P(Intelligence == 'high') or P(Grade == 'A') == 0

    def to_dataframe(self):
        return self.series.unstack().fillna(0)

    @property
    def E(self):
        return Expectation(self)

    def sum(self):
        return self.series.sum()

    def Val(self, random_variable):
        """
        Val(X) = subset for all possible values for random variable X

        :param RandomVariable random_variable:
        :return: subset for all possible values for random variable X
        """
        multiindex = self.series.index

        position = multiindex.names.index(random_variable.name)

        return multiindex.levels[position]
