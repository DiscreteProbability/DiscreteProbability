import pandas as pd

from typing import List, Iterable
from probability.experiment import Experiment
from probability.concept.random_variable import RandomVariable, SetOfRandomVariable
from probability.probability_distribution import ProbabilityDistribution


class JointDistribution(object):
    # * reduction
    # * marginalization

    @staticmethod
    def from_list(distribution: List[List[any]], variables_names: Iterable[str]) -> 'ProbabilityDistribution':
        name = JointDistribution._make_name(SetOfRandomVariable(variables_names))

        dataframe = pd.DataFrame(distribution, columns=variables_names + (name, ))

        return ProbabilityDistribution.from_joint_distribution(dataframe).normalize()  # FIXME

    @staticmethod
    def _make_name(variables: SetOfRandomVariable) -> str:
        return 'P({})'.format(variables.__repr__())

    @staticmethod
    def from_experiment(experiment: Experiment):
        series = experiment.count()
        return JointDistribution.from_series(series)

    @staticmethod
    def from_series(series: pd.Series):
        series = series.copy()
        variables = tuple(RandomVariable(variable_name) for variable_name in series.index.names)

        series.name = JointDistribution._make_name(SetOfRandomVariable(variables))

        return ProbabilityDistribution.from_joint_distribution(series).normalize()  # FIXME

    def renormalize(self):
        """
        P(I, D, g¹) -renormalize-> P(I, D | g¹)
        :return:
        """
        pass
