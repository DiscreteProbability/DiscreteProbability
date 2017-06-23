from numbers import Number


class Expectation(object):

    def __init__(self, P):
        self.P = P

    def __getitem__(self, item):
        if isinstance(item, Number):
            return item

        P = self.P(item)

        series = P.series
        return (series * series.index).sum()


class Variance(object):

    def σ(self):
        pass