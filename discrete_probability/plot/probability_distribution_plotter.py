import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class ProbabilityDistributionPlotter(object):

    def __init__(self, probability_distribution):
        self.P = probability_distribution

    def __call__(self, *args, **kwargs):
        if type(self.P.series.index) == pd.Index:
            return self.stem()

        elif type(self.P.series.index) == pd.MultiIndex:
            return self.heartmap()

        return None

    def stem(self):
        series = self.P.series

        labels = series.index.values
        y = series

        x = range(len(y))
        plt.stem(x, y)
        plt.xticks(x, labels)
        plt.axis([-1, len(series), 0, y.max() * 1.125])

        plt.xlabel(series.index.name)
        plt.ylabel('Probability')

        plt.title('$P({})$'.format(series.index.name))

        plt.xticks(rotation=90)

        return plt

    def heartmap(self):
        return sns.heatmap(self.P.to_dataframe(), linewidths=.5, cmap="YlGnBu")

    @property
    def pie(self):
        return self.P.series.plot.pie

    @property
    def bar(self):
        return self.P.series.plot.bar

    def stacked_bar(self, **kwargs):
        return self.P.series.unstack().plot(kind='bar', stacked=True, **kwargs)
