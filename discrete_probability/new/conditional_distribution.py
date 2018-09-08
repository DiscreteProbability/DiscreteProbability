import seaborn as sns

from probability.new.probability_distribution import ProbabilityDistribution
from probability.concept.assignment import Assignment
from probability.concept.random_variable import Conditional


class ConditionalDistribution(ProbabilityDistribution):

    def __init__(self, probability_distribution, conditional: Conditional):
        self.P = probability_distribution
        self.conditional = conditional
        self._distribution = self._calcule_distribution()

    def _calcule_distribution(self):
        query = self.conditional.query_variables
        evidences = self.conditional.evidences

        intersection = set(query) | set(evidences)
        P = self.P

        distribution = P(*intersection) / P(*evidences.to_tuple())
        distribution.series.rename('P({})'.format(self.conditional), inplace=True)

        return distribution

    @property
    def distribution(self):
        return self._distribution

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
