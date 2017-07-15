import seaborn as sns

from probability.distribution.probability_distribution import AbstractProbabilityDistribution
from probability.concept.assignment import Assignment


class ConditionalDistribution(AbstractProbabilityDistribution):

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

        #print(P(*intersection))
        distribution = P(*intersection) / P(*evidences.subset)
        distribution.series.rename('P({})'.format(self.conditional_random_variable), inplace=True)

        return distribution

    @property
    def series(self):
        return self.distribution.series

    def to_dataframe(self):
        query_variables = self.conditional_random_variable.query_variables
        return self.series.unstack(query_variables.names).fillna(0)

    def plot(self):
        plot = sns.heatmap(self.to_dataframe(), linewidths=.5, cmap="YlGnBu")

        name = self.series.name
        name = name.replace(' ', '\ ')
        name = name.replace('{', '\{')
        name = name.replace('}', '\}')

        plot.set_title('${}$'.format(name))

        return plot

    def reduction(self, *assignments):
        Val = self.P.Val

        events = []
        for element in assignments:
            values = Val(element) if type(element) != Assignment else element.event.elements
            events.append(list(values))

        events = tuple(events)
        reduction = self.series.loc[events]
        print(reduction)
        return reduction

        #return P.from_joint_distribution(reduction)