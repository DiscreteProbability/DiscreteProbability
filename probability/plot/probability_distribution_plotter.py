import matplotlib.pyplot as plt


class ProbabilityDistributionPlotter(object):

    def __init__(self, probability_distribution):
        self.P = probability_distribution

    def plot(self):
        if len(self.P.data.keys()) == 2:
            return self.plot_line()

    def plot_line(self):
        df = self.P.data

        labels = df[df.columns[0]]
        y = self.P.values

        x = range(len(y))
        plt.stem(x, y)
        plt.xticks(x, labels)
        plt.axis([-1, len(df), 0, y.max() * 1.125])

        return plt
