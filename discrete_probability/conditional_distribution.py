import seaborn as sns

from discrete_probability.distribution.probability_distribution import AbstractProbabilityDistribution
from discrete_probability.concept.assignment import Assignment
from discrete_probability.concept.random_variable import Conditional


class ConditionalDistribution(AbstractProbabilityDistribution):

    def __init__(self, probability_distribution, conditional: Conditional):
        self.P = probability_distribution
        self.conditional = conditional

    @property
    def distribution(self):
        query = self.conditional.query_variables
        evidences = self.conditional.evidences

        intersection = set(query) | set(evidences)
        P = self.P

        distribution = P(*intersection) / P(*evidences.to_tuple())
        distribution.series.rename('P({})'.format(self.conditional), inplace=True)

        return distribution

    @property
    def series(self):
        return self.distribution.series

    def to_dataframe(self):
        query_variables = self.conditional.query_variables
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
        return reduction

        #return P.from_joint_distribution(reduction)