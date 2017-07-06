import seaborn as sns


class ConditionalDistribution(object):

    def __init__(self, probability_distribution, conditional_random_variable):
        """
        :param probability_distribution:
        """
        self.P = probability_distribution
        self.conditional_random_variable = conditional_random_variable

    @property
    def distribution(self):
        query = self.conditional_random_variable.query_variables
        evidences = self.conditional_random_variable.evidences

        intersection = query.as_set | evidences.as_set
        P = self.P

        distribution = P(*intersection) / P(*evidences.subset)
        distribution.series = distribution.series.rename('P({})'.format(self.conditional_random_variable))

        return distribution

    @property
    def series(self):
        return self.distribution.series

    def __repr__(self):
        return self.series.__repr__()

    def to_dataframe(self):
        query_variables = self.conditional_random_variable.query_variables
        return self.series.unstack(query_variables.names)

    def plot(self):
        plot = sns.heatmap(self.to_dataframe(), linewidths=.5, cmap="YlGnBu")
        plot.set_title('${}$'.format(self.series.name.replace(' ', '\ ')))

        return plot
