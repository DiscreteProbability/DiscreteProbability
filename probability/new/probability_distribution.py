from fractions import Fraction

import operator
import pandas as pd
import numpy as np

from abc import ABCMeta, abstractmethod
from probability.concept.random_variable import RandomVariable, SetOfRandomVariable
from typing import Callable


def joint_distribution(series_or_dataframe):
    from probability.probability_distribution import ProbabilityDistribution

    return ProbabilityDistribution.from_joint_distribution(series_or_dataframe)


class ProbabilityDistribution(metaclass=ABCMeta):

    @property
    def variables(self) -> SetOfRandomVariable:
        index = self.series.index
        names = [index.name] if type(index) == pd.Index else index.names

        return SetOfRandomVariable(tuple(RandomVariable(column) for column in names))

    @property
    @abstractmethod
    def series(self) -> pd.Series:
        return None

    def argmax(self, *variables):
        """
        Arguments of the maxima (or argmax) returns the assignments that causes the maximum
        value in probability distribution.
        :return:
        """
        if not variables:
            variables = self.variables

        method = lambda assignment: assignment.random_variable in variables

        maximum = self.series.argmax()
        argmax = (variable == value for variable, value in zip(self.variables, maximum))

        return tuple(filter(method, argmax))

    def sum(self):
        return self.series.sum()

    def __eq__(self, other) -> bool:
        if self.variables != other.variables:
            return False
            #common_variables = set(self.variables) & set(other.variables)
            #common_variables = tuple(common_variables)

            #this = self(*common_variables)
            #other = other(*common_variables)

        # Sort columns
        variables = self.variables

        if len(variables.to_tuple()) > 1:
            series = other.series.reorder_levels(self.variables.names)
            series.sort_index(inplace=True)

            other = joint_distribution(series)

        return np.isclose(self.series, other.series).all()

    def __mul__(self, other: 'ProbabilityDistribution') -> 'ProbabilityDistribution':
        name = self.series.name + ' ' + other.series.name
        operation = operator.mul

        return self._calcule(other, operation, name)

    def __truediv__(self, other: 'ProbabilityDistribution') -> 'ProbabilityDistribution':
        name = self.series.name + ' / ' + other.series.name
        operation = operator.truediv

        return self._calcule(other, operation, name)

    def _calcule(self, other: 'ProbabilityDistribution', operation: Callable, new_name: str) -> 'ProbabilityDistribution':
        """
        Based in: https://github.com/pandas-dev/pandas/issues/9368
        """
        X = self.series
        Y = other.series

        on = tuple(set(X.index.names) & set(Y.index.names))
        result = pd.merge(X.reset_index(), Y.reset_index(), on=on, how='outer')

        result[new_name] = operation(result[X.name], result[Y.name])
        result = result.drop([X.name, Y.name], axis=1)

        variables = set(self.variables.names) | set(other.variables.names)
        result.set_index(list(variables))

        return joint_distribution(result)

    def __repr__(self):
        return self.series.map(lambda x: Fraction(x).limit_denominator()).__repr__()
