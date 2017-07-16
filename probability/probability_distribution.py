import pandas as pd

from probability.concept.random_variable import RandomVariable, SetOfRandomVariable
from probability.conditional_distribution import ConditionalDistribution
from probability.distribution.probability_distribution import AbstractProbabilityDistribution
from probability.expectation import Expectation
from probability.other.elements_list import ElementsList
from probability.other.utils import Parser
from probability.plot.probability_distribution_plotter import ProbabilityDistributionPlotter


class ProbabilityDistribution(AbstractProbabilityDistribution):

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
        self._series = series

    @property
    def series(self):
        return self._series

    def __call__(self, *args, **kwargs):
        return self.parse(ElementsList(self, *args))

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

    def reduction(self, *variables):
        """
        :param list/tuple variables:
        """
        P = self
        random_variables = [var.random_variable for var in variables]

        events = []
        for variable in variables:
            values = P.Val(variable) if variable.assigned else variable.event.elements

            values = tuple(values)
            if len(values) == 1:
                values = values[0]

            events.append(values)

        events = tuple(events)
        reduction = P(*random_variables).series.loc[events]

        if not isinstance(reduction, pd.Series):
            names = list(variable.name for variable in random_variables)
            index = pd.MultiIndex.from_arrays(events, names=names)

            reduction = pd.Series([reduction], index=index)
            reduction.name = 'names'  # FIXME

        return P.from_joint_distribution(reduction)

    def random_variables_series(self, P, random_variables, value):
        names = random_variables.names
        assignments = []
        index = pd.MultiIndex.from_arrays(assignments, names=names)

        series = pd.Series([value], index=index)
        series.name = 'names'  # FIXME

        return series

    def joint_distribution(self, *variables: 'RandomVariable'):
        variables = Parser.lazy_notation(self.variables, subset=variables)

        variables_names = [variable.name for variable in variables]
        series = self.series

        new_probability = ProbabilityDistribution(series.groupby(level=variables_names).sum())
        new_probability.series.rename('P({})'.format(SetOfRandomVariable(tuple(variables))), inplace=True)

        return new_probability

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

    def normalize(self):
        normalized = self.series / self.series.sum()
        return ProbabilityDistribution.from_joint_distribution(normalized)

    def __add__(self, other):
        other = other.series if type(other) == ProbabilityDistribution else other
        return ProbabilityDistribution(self.series + other)

    def __sub__(self, other):
        # ProbabilityDistribution(self.data - other.data)
        return self.series - other.series

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

    def Val(self, random_variable):
        """
        Val(X) = subset for all possible values for random variable X

        :param RandomVariable random_variable:
        :return: subset for all possible values for random variable X
        """
        multiindex = self.series.index

        position = multiindex.names.index(random_variable.name)

        return multiindex.levels[position]
