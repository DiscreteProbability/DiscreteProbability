
class Expectation(object):

    def __init__(self, P):
        self.P = P

    def __getitem__(self, item):
        P = self.P(item)

        series = P.series
        return (series * series.index).sum()
