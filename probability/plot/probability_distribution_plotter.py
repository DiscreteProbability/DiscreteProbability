import matplotlib.pyplot as plt
import pandas as pd


class ProbabilityDistributionPlotter(object):

    def __init__(self, probability_distribution):
        self.P = probability_distribution

    def plot(self):
        if type(self.P.series.index) == pd.Index:
            return self.plot_line()

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
