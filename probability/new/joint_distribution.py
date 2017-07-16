from typing import List, Tuple, Union

import pandas as pd
from pandas import Series

from probability.concept.random_variable import RandomVariable, SetOfRandomVariable, Conditional
from probability.experiment import Experiment, Occurrence
from probability.new.probability_distribution import ProbabilityDistribution

from probability.other.elements_list import ElementsList
from probability.other.utils import Parser


class JointDistribution(ProbabilityDistribution):
    # * reduction
    # * marginalization

    @staticmethod
    def from_list(distribution: List[List[any]], variables_names: Tuple[str, ...]) -> 'JointDistribution':
        return Builder.from_list(distribution, variables_names)

    @staticmethod
    def from_experiment(experiment: Experiment) -> 'JointDistribution':
        return Builder.from_experiment(experiment)

    @staticmethod
    def from_series(distribution: Series) -> 'JointDistribution':
        return Builder.from_series(distribution)

    def __init__(self, series: Series):
        self._series = series

    def __call__(self, *args: Union[RandomVariable, Conditional]):
        return ElementsListParser.parse(self, ElementsList(self, *args))

    @property
    def series(self) -> Series:
        return self._series

    def normalize(self) -> 'JointDistribution':
        normalized = self.series / self.series.sum()
        return JointDistribution(normalized)

    def reduction(self, *variables: RandomVariable) -> ProbabilityDistribution:
        """
        :param list/tuple variables:
        """
        variables = SetOfRandomVariable(variables)
        P = self

        events = Utils.extract_events(self, variables)
        marginalized = P(*variables.only_random_variables())
        reduction = marginalized.series.loc[events]

        # FIXME Extract
        if not isinstance(reduction, pd.Series):
            names = list(variable.name for variable in variables)
            index = pd.MultiIndex.from_arrays(events, names=names)

            reduction = pd.Series([reduction], index=index)
            reduction.name = 'names'  # FIXME

        # FIXME Returns a ProbabilityDistribution, not a Joint distribuion
        return JointDistribution(reduction)

    def joint_distribution(self, *variables: RandomVariable):
        variables = Parser.lazy_notation(self.variables, subset=variables)

        series = self.series
        series = series.groupby(level=variables.names).sum()

        new_probability = JointDistribution(series)
        new_probability.series.rename('P({})'.format(SetOfRandomVariable(tuple(variables))), inplace=True)

        return new_probability

    def marginalize_out(self, *variables: RandomVariable):
        """
        Marginalize out the variables from this joint distribution
        """
        P = self
        variables_new_joint_distribution = set(self.variables) - set(variables)
        return P(*variables_new_joint_distribution)

    def Val(self, random_variable: RandomVariable) -> set:
        """
        Val(X) = subset for all possible values for random variable X

        :param RandomVariable random_variable:
        :return: subset for all possible values for random variable X
        """
        multi_index = self.series.index
        position = multi_index.names.index(random_variable.name)

        return multi_index.levels[position]

    def renormalize(self) -> 'JointDistribution':
        """
        P(I, D, g¹) -renormalize-> P(I, D | g¹)
        :return:
        """
        pass


class ElementsListParser(object):
    @staticmethod
    def parse(P: JointDistribution,
              elements_list: ElementsList):  # -> Union[JointDistribution, ConditionalDistribution]:
        if not elements_list:
            return 0

        if elements_list.is_conditional_random_variable():
            return ConditionalDistribution(P, elements_list[0])
        elif elements_list.contains_conditional_distribution():
            return ConditionalDistribution(P, elements_list.to_conditional_random_variable())

        if elements_list.is_only_values():
            return P.reduction(*[X == x for X, x in zip(P.variables, elements_list.elements)])

        if elements_list.contains_assignment():
            return P.reduction(*elements_list.elements)

        # raise Exception("I don't know how work with elements: {}".format(elements_list.elements))

        # Marginalization elements out of elements
        return P.joint_distribution(*elements_list.elements)


class Builder(object):
    @staticmethod
    def _make_name(variables: SetOfRandomVariable) -> str:
        return 'P({})'.format(variables.__repr__())

    @staticmethod
    def from_list(distribution: List[List[any]], variables_names: Tuple[str, ...]) -> 'JointDistribution':
        experiment = Experiment(*variables_names)

        for occurrence in distribution:
            keys, total = occurrence[:-1], occurrence[-1]
            experiment.register(Occurrence(keys, total))

        return Builder.from_experiment(experiment)

    @staticmethod
    def from_experiment(experiment: Experiment) -> 'JointDistribution':
        series = experiment.count()
        return Builder.from_series(series)

    @staticmethod
    def from_series(series: Series) -> 'JointDistribution':
        series = series.copy()
        variables = tuple(RandomVariable(variable_name) for variable_name in series.index.names)

        series.name = Builder._make_name(SetOfRandomVariable(variables))

        return JointDistribution(series).normalize()  # FIXME


class Utils(object):

    @staticmethod
    def extract_events(P: JointDistribution, variables: SetOfRandomVariable) -> tuple:
        events = []
        for variable in variables:
            values = P.Val(variable) if not variable.assigned else variable.assignment.elements

            values = tuple(values)
            if len(values) == 1:
                values = values[0]

            events.append(values)

        return tuple(events)
