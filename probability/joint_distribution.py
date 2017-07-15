import pandas as pd
from probability.concept.random_variable import RandomVariable, RandomVariables
from probability.probability_distribution import ProbabilityDistribution


class JointDistribution(object):
    # * reduction
    # * marginalization

    @staticmethod
    def from_list(distribution, variables_names):
        """
        :param list[list] distribution:
        :param tuple variables_names:

        :return: JointDistribution
        """
        name = 'P({})'.format(RandomVariables(variables_names).__repr__())

        dataframe = pd.DataFrame(distribution, columns=variables_names + (name, ))

        return ProbabilityDistribution.from_joint_distribution(dataframe).normalize()  # FIXME

    @staticmethod
    def from_experiment(experiment):
        series = experiment.count()
        return JointDistribution.from_series(series)

    @staticmethod
    def from_series(series):
        variables = tuple(RandomVariable(variable_name) for variable_name in series.index.names)

        variables = RandomVariables(variables)
        series.name = 'P({})'.format(variables.__repr__())

        return ProbabilityDistribution.from_joint_distribution(series).normalize()  # FIXME

    def renormalize(self):
        """
        P(I, D, g¹) -renormalize-> P(I, D | g¹)
        :return:
        """
        pass
