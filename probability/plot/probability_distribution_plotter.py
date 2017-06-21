import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class ProbabilityDistributionPlotter(object):

    def __init__(self, probability_distribution):
        self.P = probability_distribution

    def plot(self):
        if type(self.P.series.index) == pd.Index:
            return self.plot_line()

        elif type(self.P.series.index) == pd.MultiIndex:
            return self.plot_heartmap()

        return None

    def plot_line(self):
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

        return plt

    def plot_heartmap(self):
        return sns.heatmap(self.P.to_dataframe(), linewidths=.5, cmap="YlGnBu")
